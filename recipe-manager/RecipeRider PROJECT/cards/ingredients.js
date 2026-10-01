document.addEventListener('DOMContentLoaded', function () {
    const contentBody = document.querySelector('.content-body');
    const ingredientSearchInput = document.querySelector('.search-bar input');
    const recipeSearchInput = document.querySelector('.search-bar2 input');
    const searchResults = document.getElementById('search-results');

    let selectedIngredients = new Set();
    let currentFoodItems = [];
    let currentFocus = -1;

    // Mapping of ingredient section IDs
    const ingredientSections = {
        "Core Essentials": document.getElementById('core-essentials'),
        "Vegetables": document.getElementById('vegetables'),
        "Fruits": document.getElementById('fruits'),
        "Fish and Meats": document.getElementById('meats'),
        "Spices": document.getElementById('spices'),
        "Sweets": document.getElementById('sweets')
    };

    // Function to show popup message with overlay
    function showPopupMessage(message) {
        const overlay = document.createElement('div');
        overlay.classList.add('popup-overlay');
        
        const popup = document.createElement('div');
        popup.classList.add('popup-message');

        const title = document.createElement('h2');
        title.textContent = 'Woops!';
        popup.appendChild(title);

        const messageText = document.createElement('p');
        messageText.textContent = message;
        popup.appendChild(messageText);

        const closeButton = document.createElement('button');
        closeButton.textContent = 'OK';
        closeButton.addEventListener('click', () => {
            document.body.removeChild(overlay);
        });

        popup.appendChild(closeButton);
        overlay.appendChild(popup);
        document.body.appendChild(overlay);
    }

    // Load selected ingredients from localStorage (if any)
    function loadSelectedIngredients() {
        const storedIngredients = localStorage.getItem('selectedIngredients');
        if (storedIngredients) {
            selectedIngredients = new Set(JSON.parse(storedIngredients));
        }
    }

    // Save selected ingredients to localStorage
    function saveSelectedIngredients() {
        localStorage.setItem('selectedIngredients', JSON.stringify([...selectedIngredients]));
    }

    // Fetch ingredient categories from the server
    function loadIngredients() {
        fetch('http://localhost:5000/api/ingredient-categories')
            .then(response => response.json())
            .then(data => {
                data.forEach(categoryData => {
                    const section = ingredientSections[categoryData.category];
                    if (section) {
                        categoryData.ingredients.forEach(ingredient => {
                            const button = document.createElement('button');
                            button.textContent = ingredient;
                            button.addEventListener('click', () => toggleIngredient(ingredient, button));
                            section.appendChild(button);

                            // Restore button style if it was previously selected
                            if (selectedIngredients.has(ingredient)) {
                                button.style.backgroundColor = 'red';
                            }
                        });
                    }
                });
                displayFoodItems();
            })
            .catch(error => console.error('Error loading ingredients data:', error));
    }

    // Toggle ingredient selection and display food items
    function toggleIngredient(ingredient, button) {
        if (selectedIngredients.has(ingredient)) {
            selectedIngredients.delete(ingredient);
            button.style.backgroundColor = '';
        } else {
            selectedIngredients.add(ingredient);
            button.style.backgroundColor = 'red';
        }
        saveSelectedIngredients();
        displayFoodItems();
    }

    // Fetch food items from the server
    function fetchFoodData(callback) {
        fetch('http://localhost:5000/api/ingredients')
            .then(response => response.json())
            .then(data => callback(data))
            .catch(error => console.error('Error loading ingredients:', error));
    }

    // Function to show food items based on selected ingredients
    function displayFoodItems(filteredRecipes = null) {
        contentBody.innerHTML = '';

        if (selectedIngredients.size === 0 && !recipeSearchInput.value) {
            contentBody.classList.remove('has-content');
            return;
        }

        const foodItemBackground = document.createElement('div');
        foodItemBackground.classList.add('food-item-background');

        fetchFoodData(function (foodItems) {
            const filteredItems = filteredRecipes || foodItems.filter(food =>
                [...selectedIngredients].every(ingredient =>
                    food.ingredient && food.ingredient.toLowerCase().includes(ingredient.toLowerCase())
                )
            );

            currentFoodItems = filteredItems;

            if (filteredItems.length > 0) {
                filteredItems.forEach(item => {
                    const foodItemDiv = document.createElement('div');
                    foodItemDiv.classList.add('food-item');

                    const foodImage = document.createElement('img');
                    foodImage.src = item.image;
                    foodImage.alt = item.name;
                    foodImage.classList.add('food-image');

                    const foodDetails = document.createElement('div');
                    foodDetails.classList.add('food-details');

                    const foodName = document.createElement('h3');
                    foodName.textContent = item.name;

                    const dietary = document.createElement('p');
                    const wholeTime = document.createElement('p');

                    // Updated logic to handle A story and B story recipes
                    if (item.dietary) {
                        // A story recipes
                        dietary.textContent = item.dietary;
                        wholeTime.textContent = item['Whole Time'] || '';
                    } else {
                        // B story recipes
                        dietary.textContent = `${item.mainType} Dish` || '';
                        wholeTime.textContent = `Preparation time: ${item.wholeTime || ''}`;
                    }

                    const foodLink = document.createElement('a');
                    foodLink.href = "#";
                    foodLink.textContent = "View Recipe";
                    foodLink.classList.add('food-link');

                    foodDetails.appendChild(foodName);
                    foodDetails.appendChild(dietary);
                    foodDetails.appendChild(wholeTime);
                    foodDetails.appendChild(foodLink);

                    foodItemDiv.appendChild(foodImage);
                    foodItemDiv.appendChild(foodDetails);
                    foodItemBackground.appendChild(foodItemDiv);

                    foodLink.addEventListener('click', function (event) {
                        event.preventDefault();
                        showRecipeWindow(item);
                    });
                });

                contentBody.appendChild(foodItemBackground);
                contentBody.classList.add('has-content');
            } else {
                contentBody.classList.remove('has-content');
            }
        });
    }

    // Function to open recipe in a separate window
    function showRecipeWindow(foodItem) {
        const recipeId = foodItem.id;
        window.open(`recipe.html?recipeId=${recipeId}`, '_blank');
    }

    // Ingredient search with suggestion list
    ingredientSearchInput.addEventListener('input', function () {
        const searchQuery = ingredientSearchInput.value.toLowerCase();
        searchResults.innerHTML = '';
        currentFocus = -1;

        if (searchQuery) {
            const ingredientButtons = document.querySelectorAll('.ingredient-list button');
            ingredientButtons.forEach(button => {
                if (!button.textContent.toLowerCase().includes(searchQuery)) {
                    button.style.backgroundColor = '';
                    selectedIngredients.delete(button.textContent.trim());
                }

                if (button.textContent.toLowerCase().includes(searchQuery)) {
                    const resultItem = document.createElement('div');
                    resultItem.classList.add('search-result-item');

                    const plusIcon = document.createElement('span');
                    plusIcon.classList.add('plus-icon');
                    plusIcon.textContent = '+';

                    const ingredientName = document.createElement('span');
                    ingredientName.classList.add('ingredient-name');
                    ingredientName.textContent = button.textContent;

                    const addText = document.createElement('span');
                    addText.classList.add('add-text');
                    addText.textContent = 'add';

                    resultItem.appendChild(plusIcon);
                    resultItem.appendChild(ingredientName);
                    resultItem.appendChild(addText);

                    searchResults.appendChild(resultItem);

                    resultItem.addEventListener('click', function () {
                        if (!selectedIngredients.has(ingredientName.textContent)) {
                            selectedIngredients.add(ingredientName.textContent);
                            button.style.backgroundColor = 'red';
                            displayFoodItems();
                            saveSelectedIngredients();
                        }
                        searchResults.innerHTML = '';
                        ingredientSearchInput.value = '';
                    });
                }
            });
        } else {
            selectedIngredients.clear();
            displayFoodItems();
        }
    });

    // Arrow navigation and enter key in suggestion list
    ingredientSearchInput.addEventListener('keydown', function (event) {
        const items = searchResults.getElementsByClassName('search-result-item');
        if (event.key === 'ArrowDown') {
            currentFocus++;
            addActive(items);
            event.preventDefault();
        } else if (event.key === 'ArrowUp') {
            currentFocus--;
            addActive(items);
            event.preventDefault();
        } else if (event.key === 'Enter') {
            event.preventDefault();
            if (currentFocus > -1 && items[currentFocus]) {
                items[currentFocus].click();
            } else if (ingredientSearchInput.value.trim()) {
                showPopupMessage("No ingredients were recognized in your search.");
                searchResults.innerHTML = ''; // Clear suggestions
            }
        }
    });

    // Add active class for suggestion items
    function addActive(items) {
        if (!items) return;
        removeActive(items);
        if (currentFocus >= items.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = items.length - 1;
        items[currentFocus].classList.add('active');
    }

    // Remove active class
    function removeActive(items) {
        Array.from(items).forEach(item => item.classList.remove('active'));
    }

    // Hide suggestion list on click outside
    document.addEventListener('click', function (event) {
        if (!ingredientSearchInput.contains(event.target) && !searchResults.contains(event.target)) {
            searchResults.innerHTML = '';
        }
    });

    // Recipe search functionality
    recipeSearchInput.addEventListener('input', function () {
        const searchQuery = recipeSearchInput.value.toLowerCase();
        localStorage.setItem('recipeSearchQuery', searchQuery);

        if (!searchQuery) {
            contentBody.innerHTML = '';
            contentBody.classList.remove('has-content');
        } else {
            fetchFoodData(function (foodItems) {
                const filteredRecipes = foodItems.filter(item =>
                    item.name.toLowerCase().includes(searchQuery)
                );
                displayFoodItems(filteredRecipes);
            });
        }
    });

    // Restore search queries and results on page load
    function restoreRecipeSearch() {
        const savedQuery = localStorage.getItem('recipeSearchQuery');
        if (savedQuery) {
            recipeSearchInput.value = savedQuery;
            fetchFoodData(function (foodItems) {
                const filteredRecipes = foodItems.filter(item =>
                    item.name.toLowerCase().includes(savedQuery)
                );
                displayFoodItems(filteredRecipes);
            });
        }
    }

    restoreRecipeSearch();
    loadSelectedIngredients();
    loadIngredients();
});
