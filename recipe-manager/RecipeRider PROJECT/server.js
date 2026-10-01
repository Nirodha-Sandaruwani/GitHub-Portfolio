require('dotenv').config(); // Load environment variables from .env
const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use('/uploads', express.static('uploads')); // Serve uploaded images
app.use(express.static(path.join(__dirname, 'public'))); // Serve static files from "public" folder
app.use(express.static(path.join(__dirname, 'cards'))); // Serve static files from "cards" folder

// MongoDB connection
mongoose
    .connect(process.env.MONGO_URI)
    .then(() => console.log('MongoDB connected'))
    .catch((err) => console.error('MongoDB connection error:', err));

// Schemas and Models
const IngredientSchema = new mongoose.Schema({
    id: { type: String, unique: true }, // Ensure `id` is consistently a string
    image: String,
    name: String,
    meal: String,
    mainType: String,
    dietary: String,
    wholeTime: String,
    description: String,
    ingredient: String, // Comma-separated ingredients
    recipe: String,
});

const IngredientCategorySchema = new mongoose.Schema({
    category: String,
    ingredients: [String],
});

const Ingredient = mongoose.model('Ingredient', IngredientSchema);
const IngredientCategory = mongoose.model('IngredientCategory', IngredientCategorySchema);

// File upload configuration
const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, 'uploads'),
    filename: (req, file, cb) => cb(null, Date.now() + '-' + file.originalname),
});
const upload = multer({ storage });

// Initialize Database with JSON Data
async function initializeDatabase() {
    try {
        const ingredientsFilePath = path.join(__dirname, 'cards', 'ingredients.json');
        const categoriesFilePath = path.join(__dirname, 'cards', 'ingredientCategories.json');

        // Fix older recipes: Convert all `id` fields to strings
        await Ingredient.updateMany({}, [
            { $set: { id: { $toString: "$id" } } }
        ]);
        console.log("Fixed older recipes: Converted all `id` fields to strings.");

        // Ensure unique `id` values by removing duplicates
        const allIngredients = await Ingredient.find({});
        const uniqueIds = new Set();
        for (const ingredient of allIngredients) {
            if (uniqueIds.has(ingredient.id)) {
                await Ingredient.deleteOne({ _id: ingredient._id }); // Remove duplicate
            } else {
                uniqueIds.add(ingredient.id);
            }
        }
        console.log("Removed duplicate recipes from the database.");

        // Initialize ingredients
        if (fs.existsSync(ingredientsFilePath)) {
            const ingredientsData = JSON.parse(fs.readFileSync(ingredientsFilePath, 'utf-8'));
            const ingredientCount = await Ingredient.countDocuments();

            if (ingredientCount === 0) {
                await Ingredient.insertMany(
                    ingredientsData.map((item) => ({
                        id: item.id,
                        image: item.image,
                        name: item.name,
                        meal: item.meal || '',
                        mainType: item['main type'] || '',
                        dietary: item.dietary || '',
                        wholeTime: item['Whole Time'] || '',
                        description: item.description || '',
                        ingredient: item.Ingridient || '',
                        recipe: item.recipe || '',
                    }))
                );
                console.log('Ingredients initialized in the database.');
            } else {
                console.log('Ingredients already exist in the database.');
            }
        } else {
            console.error('ingredients.json file not found');
        }

        // Initialize categories
        if (fs.existsSync(categoriesFilePath)) {
            const categoriesData = JSON.parse(fs.readFileSync(categoriesFilePath, 'utf-8'));
            const categoryCount = await IngredientCategory.countDocuments();

            if (categoryCount === 0) {
                await IngredientCategory.insertMany(categoriesData);
                console.log('Ingredient categories initialized in the database.');
            } else {
                console.log('Ingredient categories already exist in the database.');
            }
        } else {
            console.error('ingredientCategories.json file not found');
        }
    } catch (error) {
        console.error('Error initializing database:', error);
    }
}

// Call the initialization function
initializeDatabase();

// Get the next sequential recipe ID
async function getNextRecipeId() {
    const allIds = (await Ingredient.find({}, { id: 1 })).map((doc) => parseInt(doc.id, 10));
    const maxId = Math.max(...allIds, 0); // Get the highest `id` or 0 if none exist
    return (maxId + 1).toString(); // Return new `id` as a string
}

// Get all ingredients
app.get('/api/ingredients', async (req, res) => {
    try {
        const ingredients = await Ingredient.find();
        res.json(ingredients);
    } catch (error) {
        console.error('Error fetching ingredients:', error);
        res.status(500).json({ message: 'Failed to fetch ingredients.' });
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});


// Get a single ingredient/recipe by ID
app.get('/api/ingredients/:id', async (req, res) => {
    try {
        const id = req.params.id;
        const ingredient = await Ingredient.findOne({ id: id });

        if (!ingredient) {
            return res.status(404).json({ message: 'Ingredient/Recipe not found.' });
        }

        res.json(ingredient);
    } catch (error) {
        console.error('Error fetching ingredient/recipe by ID:', error);
        res.status(500).json({ message: 'Failed to fetch the ingredient/recipe.' });
    }
});

// Get all ingredient categories
app.get('/api/ingredient-categories', async (req, res) => {
    try {
        const categories = await IngredientCategory.find();
        res.json(categories);
    } catch (error) {
        console.error('Error fetching ingredient categories:', error);
        res.status(500).json({ message: 'Failed to fetch ingredient categories.' });
    }
});

// Add a new recipe
app.post('/add-recipe', upload.single('image'), async (req, res) => {
    const { name, description, ingredients, dietType, mainType, recipe, meal, wholeTime } = req.body;
    const image = req.file ? `/uploads/${req.file.filename}` : null;

    try {
        const categorizedIngredients = JSON.parse(ingredients);
        const newId = await getNextRecipeId();
        const allIngredients = categorizedIngredients.map((i) => i.value).join(', ');

        const newRecipe = await Ingredient.create({
            id: newId,
            name,
            meal: meal || 'Not Specified',
            mainType,
            dietary: dietType,
            wholeTime,
            description,
            ingredient: allIngredients,
            recipe,
            image,
        });

        for (const { category, value } of categorizedIngredients) {
            const normalizedCategory = category.trim();
            await IngredientCategory.findOneAndUpdate(
                { category: { $regex: `^${normalizedCategory}$`, $options: 'i' } },
                { $addToSet: { ingredients: value } },
                { upsert: true, new: true }
            );
        }

        res.json(newRecipe);
    } catch (error) {
        console.error('Error adding recipe:', error);
        res.status(500).json({ message: 'Failed to add recipe.' });
    }
});

// Edit a recipe
app.put('/edit-recipe/:id', upload.single('image'), async (req, res) => {
    const { name, description, ingredients, dietType, mainType, recipe, meal, wholeTime } = req.body;
    const image = req.file ? `/uploads/${req.file.filename}` : null;
    const id = req.params.id;

    try {
        const categorizedIngredients = JSON.parse(ingredients);
        const allIngredients = categorizedIngredients.map((i) => i.value).join(', ');

        const updatedRecipe = await Ingredient.findOneAndUpdate(
            { id },
            {
                name,
                meal: meal || 'Not Specified',
                mainType,
                dietary: dietType,
                wholeTime,
                description,
                ingredient: JSON.stringify(categorizedIngredients),
                recipe,
                ...(image && { image }),
            },
            { new: true }
        );

        if (!updatedRecipe) {
            return res.status(404).json({ message: 'Recipe not found for editing.' });
        }

        for (const { category, value } of categorizedIngredients) {
            const normalizedCategory = category.trim();
            await IngredientCategory.findOneAndUpdate(
                { category: { $regex: `^${normalizedCategory}$`, $options: 'i' } },
                { $addToSet: { ingredients: value } },
                { upsert: true, new: true }
            );
        }

        res.json(updatedRecipe);
    } catch (error) {
        console.error('Error editing recipe:', error);
        res.status(500).json({ message: 'Failed to edit recipe.' });
    }
});

// Delete a recipe
app.delete('/recipes/:id', async (req, res) => {
    try {
        const id = req.params.id;
        const deletedRecipe = await Ingredient.findOneAndDelete({ id });

        if (deletedRecipe) {
            res.json({ message: 'Recipe deleted successfully.' });
        } else {
            res.status(404).json({ message: 'Recipe not found.' });
        }
    } catch (error) {
        console.error('Error deleting recipe:', error);
        res.status(500).json({ message: 'Failed to delete recipe.' });
    }
});

// Get recipes by ingredient
app.get('/api/recipes/by-ingredient/:ingredient', async (req, res) => {
    try {
        const ingredient = req.params.ingredient;
        const recipes = await Ingredient.find({ ingredient: { $regex: `\\b${ingredient}\\b`, $options: 'i' } });
        res.json(recipes);
    } catch (error) {
        console.error('Error fetching recipes by ingredient:', error);
        res.status(500).json({ message: 'Failed to fetch recipes for the ingredient.' });
    }
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));