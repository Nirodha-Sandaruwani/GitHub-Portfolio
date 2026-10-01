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

async function handleSubmit(event) {
    event.preventDefault();

    const nameInput = document.querySelector('#recipe-name');
    const mainTypeInput = document.querySelector('#mainDietType');
    const dietTypeInput = document.querySelector('#categorizedDietType');
    const descriptionInput = document.querySelector('#recipe-description');
    const stepsInput = document.querySelector('#recipe-steps');
    const timeInput = document.querySelector('#wholeTime');
    const mealInput = document.getElementById('meal');
    const ingredientTextareas = document.querySelectorAll('.ingredients-container textarea');

    const name = nameInput.value.trim();
    const mainType = mainTypeInput.value.trim();
    const dietType = dietTypeInput.value.trim();
    const description = descriptionInput.value.trim();
    const steps = stepsInput.value.trim();
    const wholeTime = timeInput.value.trim();
    const meal = mealInput.value.trim();

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
        textarea => textarea.value.trim() !== ''
    );

    if (!isAnyIngredientFilled) {
        alert('Please fill in at least one ingredient box.');
        return;
    }

    // Gather filled ingredient data
    const ingredients = Array.from(ingredientTextareas)
        .map(textarea => ({
            category: textarea.id,
            value: textarea.value.trim(),
        }))
        .filter(entry => entry.value !== ''); // Filter out empty entries

    const formData = new FormData();
    formData.append('name', name);
    formData.append('mainType', mainType || '');
    formData.append('dietType', dietType || '');
    formData.append('meal', meal);
    formData.append('ingredients', JSON.stringify(ingredients));
    formData.append('description', description);
    formData.append('recipe', steps);
    formData.append('wholeTime', wholeTime);
    if (imageInput.files[0]) {
        formData.append('image', imageInput.files[0]); // Append the uploaded image
    }

    const recipeId = editingIndex !== null ? recipes[editingIndex].id : null;

    // Submit the new/edited recipe to the backend API
    const savedRecipe = await submitRecipeToAPI(formData, recipeId);

    if (savedRecipe) {
        // Check for duplicates based on ID before adding
        const exists = recipes.some(recipe => recipe.id === savedRecipe.id);

        if (editingIndex !== null) {
            // Update the existing recipe
            recipes[editingIndex] = savedRecipe;
            editingIndex = null; // Reset editing state
        } else if (!exists) {
            // Add the new recipe to the local array
            recipes.push(savedRecipe);
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
    const recipeToDelete = recipes[index];

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
    const mealInput = document.getElementById('meal');
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

    // Populate ingredients in their correct fields
    ingredientTextareas.forEach(textarea => {
        textarea.value = ''; // Clear existing values
    });

    const parsedIngredients = JSON.parse(recipeToEdit.ingredient || '[]');
    parsedIngredients.forEach(({ category, value }) => {
        const matchingTextarea = Array.from(ingredientTextareas).find(
            textarea => textarea.id === category.toLowerCase()
        );
        if (matchingTextarea) {
            matchingTextarea.value = value;
        }
    });

    editingIndex = index; // Set the current index for editing
}

// Display the recipes
function displayRecipes(filteredRecipes = recipes) {
    recipeList.innerHTML = ''; // Clear previous list
    if (filteredRecipes.length === 0) {
        noRecipes.style.display = 'block'; // Show message if no recipes
    } else {
        noRecipes.style.display = 'none'; // Hide message if there are recipes

        filteredRecipes.forEach((recipe, index) => {
            const recipeEl = document.createElement('div');
            recipeEl.classList.add('food-item');

            const dietTypeText = recipe.dietary
                ? `${recipe.dietary} Dish`
                : recipe.mainType
                ? `${recipe.mainType} Dish`
                : '';

                recipeEl.innerHTML = `
                <img src="${recipe.image || '/uploads/default.jpg'}" alt="${recipe.name}" class="food-image">
    <div class="food-details">
        <h3>${recipe.name}</h3>
        ${dietTypeText ? `<p>${dietTypeText}</p>` : ''}
        <p>Preparation time: ${recipe.wholeTime}</p>
        <a href="/recipe.html?recipeId=${recipe.id}" class="food-link">View Recipe</a>
        <div class="button-row">
            <img src="http://localhost:5000/image/edit.png" class="edit-button" data-index="${index}" alt="Edit">
            <button class="delete-button" data-index="${index}">Delete</button>
        </div>
    </div>            
            `;

            recipeList.appendChild(recipeEl); // Append the recipe element

            // Add event listeners for edit and delete buttons
            document.querySelectorAll('.delete-button').forEach(button =>
                button.addEventListener('click', handleDelete)
            );
            document.querySelectorAll('.edit-button').forEach(button =>
                button.addEventListener('click', handleEdit)
            );
        });
    }
}

// Handle search functionality
searchBox.addEventListener('input', () => {
    const searchTerm = searchBox.value.trim().toLowerCase();
    const filteredRecipes = recipes.filter(recipe =>
        recipe.name.toLowerCase().includes(searchTerm)
    );
    displayRecipes(filteredRecipes); // Re-render with filtered recipes
});

document.addEventListener('DOMContentLoaded', () => {
    displayRecipes(); // Display recipes on page load
    form.addEventListener('submit', handleSubmit); // Bind submit event
});
