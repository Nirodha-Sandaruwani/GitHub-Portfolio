document.addEventListener('DOMContentLoaded', function () {
    const contentBody = document.querySelector('.content-1-body');
    const dietTypeDropdown = document.querySelector('#dietType');
    const checkboxContainer = document.querySelector('.checkbox-container');
    const recipeSearchInput = document.querySelector('.search-bar2 input'); // Search by food name input
    const foodListContainer = document.querySelector('.food-list'); // Container for category buttons
    let activeCategory = null; // Store the currently active category button

    // Function to fetch food data from ingredients.json
    async function fetchFoodData() {
        try {
            const response = await fetch('ingredients.json');
            const data = await response.json();
            console.log("Fetched Food Items:", data); // Debug fetched data
            return data;
        } catch (error) {
            console.error('Error loading ingredients.json:', error);
            return [];
        }
    }

    // Function to fetch recipes dynamically from backend API
    async function fetchRecipesFromAPI() {
        try {
            const response = await fetch('/api/recipes');
            const data = await response.json();
            console.log("Fetched Recipes from API:", data); // Debug fetched API data
            return data;
        } catch (error) {
            console.error('Error fetching recipes from API:', error);
            return [];
        }
    }

    // Function to fetch category buttons from categoryButtons.json
    async function fetchCategoryButtons() {
        try {
            const response = await fetch('categoryButtons.json');
            const data = await response.json();
            console.log("Fetched Category Buttons:", data); // Debug fetched data
            return data;
        } catch (error) {
            console.error('Error loading categoryButtons.json:', error);
            return [];
        }
    }

    // Function to create and display category buttons
    async function loadCategoryButtons() {
        const categories = await fetchCategoryButtons();

        categories.forEach(category => {
            const button = document.createElement('button');
            button.textContent = category;
            button.addEventListener('click', function () {
                handleCategoryClick(button);
            });
            foodListContainer.appendChild(button);
        });
    }

    // Function to handle category button click
    function handleCategoryClick(button) {
        const category = button.textContent.trim();

        if (activeCategory === category) {
            activeCategory = null; // Deselect the category
            button.classList.remove('active');
            button.style.backgroundColor = ''; // Reset button color
        } else {
            const categoryButtons = foodListContainer.querySelectorAll('button');
            categoryButtons.forEach(btn => {
                btn.classList.remove('active');
                btn.style.backgroundColor = '';
            });

            activeCategory = category;
            button.classList.add('active');
            button.style.backgroundColor = 'red';
        }

        saveState();
        applyFilters();
    }

    // Function to display food items
    function displayFoodItems(filteredItems) {
        contentBody.innerHTML = ''; // Clear content body

        if (filteredItems && filteredItems.length > 0) {
            // Create the food item background wrapper
            const foodItemBackground = document.createElement('div');
            foodItemBackground.classList.add('food-item-background'); // Use your CSS class for the grid layout

            filteredItems.forEach(item => {
                const foodCard = document.createElement('div');
                foodCard.classList.add('food-item');

                const foodImage = document.createElement('img');
                foodImage.src = item.image;
                foodImage.alt = item.name;
                foodImage.classList.add('food-image');

                const foodDetails = document.createElement('div');
                foodDetails.classList.add('food-details');

                const foodName = document.createElement('h3');
                foodName.textContent = item.name;
                foodDetails.appendChild(foodName);

                const dietaryInfo = document.createElement('p');
                dietaryInfo.textContent = item.dietary;
                foodDetails.appendChild(dietaryInfo);

                const wholeTime = document.createElement('p');
                wholeTime.textContent = item["Whole Time"] || ""; // Show empty space if missing
                foodDetails.appendChild(wholeTime);

                const recipeLink = document.createElement('a');
                recipeLink.href = "#"; // Placeholder
                recipeLink.textContent = "View Recipe";
                recipeLink.classList.add('food-link');
                recipeLink.addEventListener('click', function (event) {
                    event.preventDefault();
                    const recipeId = item.id;
                    window.open(`recipe.html?recipeId=${recipeId}`, '_blank');
                });

                foodDetails.appendChild(recipeLink);
                foodCard.appendChild(foodImage);
                foodCard.appendChild(foodDetails);
                foodItemBackground.appendChild(foodCard);
            });

            contentBody.appendChild(foodItemBackground);
        } else {
            contentBody.innerHTML = ''; // Clear content if no matches
        }
    }

    // Function to save the current state to localStorage
    function saveState() {
        const selectedDietType = dietTypeDropdown.value;
        const selectedCheckboxes = Array.from(
            checkboxContainer.querySelectorAll('input[type="checkbox"]:checked')
        ).map(cb => cb.id);
        const searchQuery = recipeSearchInput.value;

        const state = {
            selectedDietType,
            selectedCheckboxes,
            activeCategory,
            searchQuery,
        };

        localStorage.setItem('filterState', JSON.stringify(state));
    }

    // Function to restore the state from localStorage
    function restoreState() {
        const state = JSON.parse(localStorage.getItem('filterState'));

        if (state) {
            dietTypeDropdown.value = state.selectedDietType || 'all';
            state.selectedCheckboxes.forEach(id => {
                const checkbox = checkboxContainer.querySelector(`#${id}`);
                if (checkbox) checkbox.checked = true;
            });

            if (state.activeCategory) {
                const buttons = foodListContainer.querySelectorAll('button');
                buttons.forEach(button => {
                    if (button.textContent.trim() === state.activeCategory) {
                        activeCategory = state.activeCategory;
                        button.classList.add('active');
                        button.style.backgroundColor = 'red';
                    }
                });
            }

            if (state.searchQuery) {
                recipeSearchInput.value = state.searchQuery;
            }

            applyFilters();
        }
    }

    // Function to apply filters
    async function applyFilters() {
        let foodItems = await fetchFoodData(); // Fetch from local ingredients.json
        const apiRecipes = await fetchRecipesFromAPI(); // Fetch from backend API
        foodItems = [...foodItems, ...apiRecipes]; // Merge both data sources

        const selectedDietType = dietTypeDropdown.value.toLowerCase();
        const selectedCheckboxes = Array.from(
            checkboxContainer.querySelectorAll('input[type="checkbox"]:checked')
        ).map(cb => cb.id.toLowerCase());
        const searchQuery = recipeSearchInput.value.toLowerCase();

        let filteredItems = foodItems;

        if (selectedDietType === 'all') {
            if (selectedCheckboxes.length === 0 && !activeCategory && !searchQuery) {
                contentBody.innerHTML = '';
                return;
            }
        } else {
            filteredItems = filteredItems.filter(item =>
                item["main type"] && item["main type"].toLowerCase() === selectedDietType
            );
        }

        if (selectedCheckboxes.length > 0) {
            filteredItems = filteredItems.filter(item =>
                selectedCheckboxes.some(dietary =>
                    item.dietary.toLowerCase().includes(dietary)
                )
            );
        }

        if (activeCategory) {
            filteredItems = filteredItems.filter(item =>
                item.meal && item.meal.toLowerCase().includes(activeCategory.toLowerCase())
            );
        }

        if (searchQuery) {
            filteredItems = filteredItems.filter(item =>
                item.name.toLowerCase().includes(searchQuery)
            );
        }

        displayFoodItems(filteredItems);
    }

    // Event listeners
    dietTypeDropdown.addEventListener('change', () => {
        saveState();
        applyFilters();
    });

    checkboxContainer.addEventListener('change', () => {
        saveState();
        applyFilters();
    });

    recipeSearchInput.addEventListener('input', () => {
        saveState();
        applyFilters();
    });

    // Initialize
    loadCategoryButtons().then(restoreState);
});
