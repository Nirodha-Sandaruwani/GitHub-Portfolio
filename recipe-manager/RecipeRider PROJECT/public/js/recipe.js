document.addEventListener("DOMContentLoaded", function () {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const recipeId = urlParams.get("recipeId"); // Get the recipeId from the query parameter

    const recipeNameElement = document.getElementById("recipe-name");
    const ingredientsListElement = document.getElementById("header-ingredients-list");
    const recipeImageElement = document.getElementById("recipe-image-left");
    const recipeDescriptionElement = document.getElementById("recipe-description");
    const dietaryInfoElement = document.getElementById("dietary-info");
    const wholeTimeInfoElement = document.getElementById("whole-time-info");
    const recipeInstructionsElement = document.getElementById("recipe-instructions");
    const introductionTitleElement = document.querySelector(".method h2"); // The "Let's make..." title

    // Fetch the recipe data from the backend
    async function fetchRecipeData() {
        try {
            const response = await fetch(`http://localhost:5000/api/ingredients/${recipeId}`);
            const recipe = await response.json();

            if (!response.ok || !recipe) {
                recipeNameElement.textContent = "Recipe Not Found";
                console.error("Error fetching recipe:", recipe.message || "No recipe found.");
                return;
            }

            // Populate the recipe data
            recipeNameElement.textContent = recipe.name || "Recipe Name";
            dietaryInfoElement.textContent = recipe.dietary || "Dietary Info";
            wholeTimeInfoElement.textContent = recipe["Whole Time"] || "Preparation Time";
            recipeDescriptionElement.textContent = recipe.description || "No description available.";

            // Update the "Let's make..." title dynamically
            introductionTitleElement.textContent = `Let's make a ${recipe.name || "recipe"} - Enjoy!`;

            // Ingredients List
            ingredientsListElement.innerHTML = "";
            recipe.ingredient.split(",").forEach((ingredient) => {
                const li = document.createElement("li");
                li.textContent = ingredient.trim();
                ingredientsListElement.appendChild(li);
            });

            // Recipe Image
            recipeImageElement.src = recipe.image || "/public/image/placeholder.png"; // Default image
            recipeImageElement.alt = recipe.name || "Recipe Image";

            // Instructions
            recipeInstructionsElement.innerHTML = "";
            recipe.recipe.split(".").forEach((step) => {
                if (step.trim() !== "") {
                    const li = document.createElement("li");

                    const numberContainer = document.createElement("span");
                    numberContainer.classList.add("step-number");
                    numberContainer.textContent = `${recipeInstructionsElement.childElementCount + 1}.`;

                    const textContainer = document.createElement("span");
                    textContainer.classList.add("step-text");
                    textContainer.textContent = step.trim();

                    li.appendChild(numberContainer);
                    li.appendChild(textContainer);
                    recipeInstructionsElement.appendChild(li);
                }
            });

            // Adjust the vertical line after rendering the instructions
            adjustVerticalLine();

            // Add event listener to update the vertical line on window resize
            window.addEventListener("resize", adjustVerticalLine);
        } catch (error) {
            console.error("Error fetching recipe data:", error);
            recipeNameElement.textContent = "Error Loading Recipe";
        }
    }

    // Function to adjust the vertical line height
    function adjustVerticalLine() {
        const methodSection = document.querySelector(".method");
        const firstStep = methodSection.querySelector("li:first-child");
        const lastStep = methodSection.querySelector("li:last-child");

        if (firstStep && lastStep) {
            let line = document.querySelector(".vertical-line");
            if (!line) {
                line = document.createElement("div");
                line.classList.add("vertical-line");
                methodSection.appendChild(line);
            }

            // Calculate the vertical distance between the first and last step
            const firstStepTop = firstStep.getBoundingClientRect().top + window.scrollY;
            const lastStepBottom = lastStep.getBoundingClientRect().bottom + window.scrollY;
            const lineHeight = lastStepBottom - firstStepTop;

            line.style.top = `${firstStep.offsetTop}px`; // Position at the top of the first step
            line.style.height = `${lineHeight}px`; // Set height to cover all steps
        }
    }

    // Load the recipe data
    fetchRecipeData();
});
