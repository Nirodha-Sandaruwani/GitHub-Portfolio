const form = document.querySelector('form');
const recipeList = document.querySelector('#recipe-list');
const noRecipes = document.getElementById('no-recipes');
const searchBox = document.getElementById('search-box');
const clearFileButton = document.getElementById('clear-file'); // Clear file button
const imageInput = document.getElementById('recipe-image'); // File input

// Fetch recipes from localStorage if available
let recipes = JSON.parse(localStorage.getItem('addedRecipes')) || [];
let editingIndex = null; // Track if a recipe is being edited

// Show or hide the remove file button based on input
imageInput.addEventListener('change', () => {
    if (imageInput.files.length > 0) {
        clearFileButton.style.display = 'inline-block'; // Show the button
    } else {
        clearFileButton.style.display = 'none'; // Hide the button
    }
});

clearFileButton.addEventListener('click', () => {
    imageInput.value = ''; // Clear the file input
    clearFileButton.style.display = 'none'; // Hide the button again
});

// Meal type button logic
document.addEventListener('DOMContentLoaded', function () {
    const mealButtons = document.querySelectorAll('.meel-type button'); // Select all meal type buttons
    const mealInput = document.getElementById('meal'); // The hidden or visible input field for meal

    // Add event listeners to all meal type buttons
    mealButtons.forEach(button => {
        button.addEventListener('click', function () {
            // If the clicked button is already selected, unselect it
            if (this.style.backgroundColor === 'red') {
                this.style.backgroundColor = ''; // Reset background color
                mealInput.value = ''; // Clear the meal input value
            } else {
                // Otherwise, unselect other buttons and select this one
                mealButtons.forEach(btn => btn.style.backgroundColor = ''); // Reset all buttons
                this.style.backgroundColor = 'red'; // Highlight the clicked button
                mealInput.value = this.textContent.trim(); // Set the meal input value
            }
        });
    });
});

// Submit the recipe to backend API
async function submitRecipeToAPI(formData, recipeId = null) {
    const url = recipeId ? `http://localhost:5000/edit-recipe/${recipeId}` : 'http://localhost:5000/add-recipe';
    const method = recipeId ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            body: formData, // Send form data including the image
        });

        const data = await response.json();

        if (response.ok) {
            return data; // Return the newly added/edited recipe data
        } else {
            console.error(`Error: ${data.message || 'Failed to add/edit recipe.'}`);
            alert('Failed to add/edit the recipe. Please try again.');
        }
    } catch (error) {
        console.error('Error submitting recipe to backend:', error);
        alert('Error adding/editing recipe. Please check your connection.');
    }
}

// Handle form submission
async function handleSubmit(event) {
    event.preventDefault();

    const nameInput = document.querySelector('#recipe-name');
    const mainTypeInput = document.querySelector('#mainDietType');
    const dietTypeInput = document.querySelector('#categorizedDietType');
    const descriptionInput = document.querySelector('#recipe-description');
    const stepsInput = document.querySelector('#recipe-steps');
    const timeInput = document.querySelector('#wholeTime');
    const mealInput = document.querySelector('#meal'); // Add the meal input here
    const ingredientTextareas = document.querySelectorAll('.ingredients-container textarea');

    const name = nameInput.value.trim();
    const mainType = mainTypeInput.value.trim();
    const dietType = dietTypeInput.value.trim();
    const description = descriptionInput.value.trim();
    const steps = stepsInput.value.trim();
    const wholeTime = timeInput.value.trim();
    const meal = mealInput.value.trim(); // Get meal value from the hidden input

    // Validate input fields
    if (!name || !description || !steps || !wholeTime || !meal) {
        alert('Please fill in all required fields, including meal type.');
        return;
    }

    // Validate dropdowns: At least one dropdown should be selected
    if (!mainType && !dietType) {
        alert('Please select at least one option from Main Diet Type or Categorized Diet Type.');
        return;
    }

    // Validate ingredients: At least one ingredient box must be filled
    const isAnyIngredientFilled = Array.from(ingredientTextareas).some(
        (textarea) => textarea.value.trim() !== ''
    );

    if (!isAnyIngredientFilled) {
        alert('Please fill in at least one ingredient box.');
        return;
    }

    // Gather filled ingredient data
    const ingredients = Array.from(ingredientTextareas)
        .map((textarea) => ({
            category: textarea.id, // The category (e.g., vegetables, spices)
            value: textarea.value.trim(),
        }))
        .filter((entry) => entry.value !== ''); // Filter out empty entries

    const formData = new FormData();
    formData.append('name', name);
    formData.append('mainType', mainType || ''); // Use Main Diet Type
    formData.append('dietType', dietType || ''); // Use Categorized Diet Type or Main Type
    formData.append('meal', meal); // Add meal type here
    formData.append('ingredients', JSON.stringify(ingredients)); // Pass categorized ingredients as JSON
    formData.append('description', description);
    formData.append('recipe', steps);
    formData.append('wholeTime', wholeTime); // Pass formatted time
    if (imageInput.files[0]) {
        formData.append('image', imageInput.files[0]); // Append the uploaded image
    }

    const recipeId = editingIndex !== null ? recipes[editingIndex].id : null;

    // Submit the new/edited recipe to the backend API
    const savedRecipe = await submitRecipeToAPI(formData, recipeId);

    if (savedRecipe) {
        if (editingIndex !== null) {
            recipes[editingIndex] = savedRecipe; // Update the existing recipe
            editingIndex = null; // Reset editing state
        } else {
            recipes.push(savedRecipe); // Add the new recipe to the local array
        }
        localStorage.setItem('addedRecipes', JSON.stringify(recipes)); // Save to localStorage
        displayRecipes(); // Update the displayed recipes
        form.reset(); // Clear form inputs
        clearFileButton.style.display = 'none'; // Hide the clear button
        mealInput.value = ''; // Reset meal input
    }
}

// Handle delete recipe
async function handleDelete(event) {
    const index = event.target.getAttribute('data-index');
    const recipeToDelete = recipes[index]; // Get the recipe to delete

    if (!recipeToDelete) {
        alert('Recipe not found.');
        return;
    }

    const confirmation = confirm(`Are you sure you want to delete the recipe "${recipeToDelete.name}"?`);
    if (!confirmation) return;

    try {
        const response = await fetch(`http://localhost:5000/recipes/${recipeToDelete.id}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            recipes.splice(index, 1); // Remove from local array
            localStorage.setItem('addedRecipes', JSON.stringify(recipes));
            displayRecipes(); // Refresh the displayed list
            alert('Recipe deleted successfully.');
        } else {
            alert('Failed to delete the recipe. Please try again.');
        }
    } catch (error) {
        console.error('Error deleting recipe from backend:', error);
        alert('Error deleting recipe. Please check your connection.');
    }
}

// Handle edit recipe
function handleEdit(event) {
    const index = event.target.getAttribute('data-index');
    const recipeToEdit = recipes[index];

    if (!recipeToEdit) return;

    const nameInput = document.querySelector('#recipe-name');
    const mainTypeInput = document.querySelector('#mainDietType');
    const dietTypeInput = document.querySelector('#categorizedDietType');
    const descriptionInput = document.querySelector('#recipe-description');
    const stepsInput = document.querySelector('#recipe-steps');
    const timeInput = document.querySelector('#wholeTime');
    const mealInput = document.querySelector('#meal');
    const ingredientTextareas = document.querySelectorAll('.ingredients-container textarea');

    nameInput.value = recipeToEdit.name;
    mainTypeInput.value = recipeToEdit.mainType;
    dietTypeInput.value = recipeToEdit.dietary;
    descriptionInput.value = recipeToEdit.description;
    stepsInput.value = recipeToEdit.recipe;
    timeInput.value = recipeToEdit.wholeTime.replace('Preparation time: ', '');
    mealInput.value = recipeToEdit.meal;

    // Highlight the correct meal button
    const mealButtons = document.querySelectorAll('.meel-type button');
    mealButtons.forEach(button => {
        button.style.backgroundColor = button.textContent.trim() === recipeToEdit.meal ? 'red' : '';
    });

    // Populate ingredients
    ingredientTextareas.forEach(textarea => {
        textarea.value = ''; // Clear existing values
    });

    recipeToEdit.ingredient.split(', ').forEach(ingredient => {
        const matchingTextarea = Array.from(ingredientTextareas).find(
            textarea => textarea.id === ingredient.toLowerCase()
        );
        if (matchingTextarea) {
            matchingTextarea.value = ingredient;
        }
    });

    editingIndex = index; // Set the editing index
}

// Display all recipes
function displayRecipes(filteredRecipes = recipes) {
    recipeList.innerHTML = '';

    if (filteredRecipes.length === 0) {
        noRecipes.style.display = 'block';
    } else {
        noRecipes.style.display = 'none';
        filteredRecipes.forEach((recipe, index) => {
            const recipeEl = document.createElement('div');
            recipeEl.classList.add('food-item');

            let dietTypeText = recipe.dietary && recipe.dietary.trim()
                ? `${recipe.dietary} Dish`
                : recipe.mainType && recipe.mainType.trim()
                ? `${recipe.mainType} Dish`
                : '';

            recipeEl.innerHTML = `
                <img src="${recipe.image || '/uploads/default.jpg'}" alt="${recipe.name}" class="food-image">
                <div class="food-details">
                    <h3>${recipe.name}</h3>
                    ${dietTypeText ? `<p>${dietTypeText}</p>` : ''}
                    <p>${recipe.wholeTime}</p>
                    <a href="/recipe.html?recipeId=${recipe.id}" class="food-link">View Recipe</a>
                    <button class="delete-button" data-index="${index}">Delete</button>
                    <button class="edit-button" data-index="${index}">Edit</button>
                </div>
            `;

            recipeList.appendChild(recipeEl);
        });

        const deleteButtons = document.querySelectorAll('.delete-button');
        deleteButtons.forEach(button => button.addEventListener('click', handleDelete));

        const editButtons = document.querySelectorAll('.edit-button');
        editButtons.forEach(button => button.addEventListener('click', handleEdit));
    }
}

// Event listeners
searchBox.addEventListener('input', event => {
    const query = event.target.value.toLowerCase();
    const filteredRecipes = recipes.filter(recipe =>
        recipe.name.toLowerCase().includes(query)
    );
    displayRecipes(filteredRecipes);
});

form.addEventListener('submit', handleSubmit);

// Initialize
displayRecipes();
