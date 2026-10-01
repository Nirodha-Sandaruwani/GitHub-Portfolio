# RecipeRider Project Report  

**Nirodha Sandaruwani Meneripitiyage Dona** - AD9906  
**Madee Uththara Deegoda Gamage** - AD9947  
**Course**: TTC2080 - Full Stack Programming, Autumn 2024  
**Date**: 03-12-2024  

---

## 1. Instruction  

The focus of this part is mainly on the background of developing the application called **RecipeRider**, which is designed to be a platform where people can search recipes for ingredients they have, organize, and display both user- and owner-generated recipes.  

The idea for the web application stemmed from making recipe platforms accessible to everyone who loves food, enjoys cooking, or simply wants to learn something new. Our ultimate goal was to make our users' lives easier by solving common problems with popular recipe platforms, such as difficulties in locating specific recipes, endless ingredient lists, or disorganized user accounts.  

To achieve this, RecipeRider integrates a simple and visually appealing UI with advanced functionalities such as intelligent ingredient filtering, convenient recipe lookups, and efficient recipe management. Built using modern tools like Node.js, Express.js, and MongoDB, the platform is highly functional and ready for future upgrades.  

Below, we describe the process of developing RecipeRider, including the design, software development lifecycle, and the functionality of its components, along with the teamwork that made it possible.  

---

## 2. Project Overview  

### 2.1 Frontend  

**Technologies Used**  
- HTML, CSS, JavaScript  

**Purpose**  
The frontend manages the application’s functionality, presents data to users in an appealing way, and utilizes REST APIs to communicate with the backend for data retrieval and updates.  

**Files and Their Roles**  

#### HTML Files  
- **ingredients.html**:  
  Displays a list of ingredients and recipes. Users can search and filter recipes based on selected ingredients or keywords.  

- **addRecipe.html**:  
  Provides a form for users to add new recipes or edit existing ones, ensuring all necessary details are captured.  

- **recipe.html**:  
  Showcases the details of a single recipe, including its image, ingredients, and preparation steps.  

#### CSS Files  
- Defines styles for various components like cards, buttons, and modals.  
- Ensures the application looks visually appealing and user-friendly.  
- Makes the platform responsive across different devices.  

#### JavaScript Files  
- **addRecipe.js**:  
  Handles actions like adding, editing, and deleting recipes. It communicates with the backend API to update the database and dynamically refreshes the UI.  

- **ingredients.js**:  
  Manages filtering and searching for recipes. Updates the displayed content dynamically based on user input and selection.  

- **recipe.js**:  
  Fetches the details of a specific recipe from the backend and displays them on the `recipe.html` page.  

By integrating these files and technologies, the frontend ensures a smooth and interactive user experience.  

---

### 2.2 Backend  

**Technologies**  
- Node.js, Express.js  

**Purpose**  
The backend handles API requests, manages data flow, facilitates file uploads, and interacts with the database.  

**Key Features**  
- REST API endpoints for CRUD operations on recipes and ingredients.  
- Middleware for handling CORS, JSON payloads, and static files.  
- **Multer**: Handles image upload functionality.  

**File**  
- **server.js**:  
  The main server file that contains all API routes, initializes the database, and manages backend logic.  

---

### 2.3 Database  

**Technology**  
- MongoDB  

**Purpose**  
- Stores recipes and ingredient data.  
- Provides query capabilities for efficient data retrieval.  
- Ensures data consistency and reliability.  

**Schemas**  
- **Ingredient Schema**:  
  Represents individual recipes with fields like `name`, `mainType`, `dietary`, `wholeTime`, and more.  

- **IngredientCategory Schema**:  
  Represents ingredient categories (e.g., Vegetables, Fruits) along with their associated ingredient lists.  

---

## 3. Relationships Between Components  

### addRecipe.js  

**Purpose**: Handles the addition, editing, and deletion of recipes.  

**Key Functions**:  
- **submitRecipeToAPI(formData, recipeId)**: Sends POST or PUT requests to the backend to add or edit recipes.  
- **handleSubmit(event)**: Validates form inputs, prepares data, and submits it to the backend.  
- **displayRecipes(filteredRecipes)**: Dynamically displays recipes as cards in the UI.  
- **handleDelete(event)**: Deletes a recipe by sending a DELETE request to the backend.  
- **handleEdit(event)**: Pre-fills the form for editing an existing recipe.  

### ingredients.js  

**Purpose**: Manages the ingredient and recipe filtering UI.  

**Key Functions**:  
- **loadIngredients()**: Fetches ingredient categories from the backend and populates the UI.  
- **toggleIngredient(ingredient, button)**: Toggles ingredient selection and updates the displayed recipes.  
- **displayFoodItems(filteredRecipes)**: Dynamically displays recipes matching selected ingredients or search criteria.  
- **showRecipeWindow(foodItem)**: Opens the selected recipe in a new window.  

### recipe.js  

**Purpose**: Displays the details of a single recipe.  

**Key Functions**:  
- **loadRecipe(recipeId)**: Fetches and displays recipe details based on the `recipeId` in the query string.  

### Relationships Between Functions  

- **Frontend & Backend**:  
  JavaScript functions (e.g., `submitRecipeToAPI`) make HTTP requests to the backend REST endpoints (e.g., `/add-recipe`, `/edit-recipe`) to fetch or update data.  

- **UI Updates**:  
  Functions like `displayRecipes` and `displayFoodItems` ensure the UI reflects the latest data after any updates, such as adding or removing ingredients.  

---

## 4. UI Mockups  

### 4.1 Ingredients Page (ingredients.html)  

#### Components:  
  - Ingredient categories (e.g., Vegetables, Fruits) with toggleable buttons.  
  - Recipe search bar for filtering recipes by name.  
  - Recipe cards displaying:  
    - Image  
    - Name  
    - Dietary type  
    - Preparation time (e.g., Whole Time)  
    - "View Recipe" link with `wholeTime` appended.  

#### Features:  
  - Dynamic recipe filtering by selected ingredients or search keywords.  
  - Context menu for additional actions (e.g., View Details).  

---

### 4.2 Add Recipe Page (addRecipe.html)  

#### Components:  
  - Form with fields for recipe name, description, dietary type, main type, ingredients, preparation steps, and image upload.  
  - Buttons for meal type selection.  

#### Features:  
  - Input validation to ensure all required fields are filled.  
  - Dynamically updates recipe cards upon addition or editing.  

---

## 5. Project Tracking - RecipeRider

### Madee Uththara Deegoda Gamage

| Day        | Task Information                                               | Time Spent |  
|------------|-----------------------------------------------------------------|------------|  
| **12 Nov** | Initial project planning, deciding on technologies and tools    | 2 hours    |  
| **13 Nov** | Researching UI/UX design for RecipeRider                        | 2 hours    |  
| **14 Nov** | Designing wireframes for Ingredients page                       | 3 hours    |  
| **17 Nov** | Developing frontend: ingredients page HTML, CSS, and JS         | 5 hours    |  
| **18 Nov** | Developing addRecipe page UI and form functionality             | 4 hours    |  
| **19 Nov** | Integrating backend API with frontend (add/edit recipes)        | 3 hours    |  
| **20 Nov** | Testing and fixing bugs in recipe filtering and searching       | 3 hours    |  
| **21 Nov** | Enhancing UI design for better responsiveness                   | 3 hours    |  
| **22 Nov** | Implementing recipe detail page (view recipe)                   | 4 hours    |  
| **23 Nov** | Implementing image upload functionality (Multer)                | 3 hours    |  
| **24 Nov** | User interface testing and improving performance                | 3 hours    |  
| **25 Nov** | Testing and bug fixing across all pages                         | 3 hours    |  
| **29 Nov** | Final integration of frontend and backend                       | 4 hours    |  
| **30 Nov** | Documentation and writing project report                        | 5 hours    |  
| **01 Dec** |Project review and last-minute improvements    | 3 hours    |  
| **02 Dec** | Preparing project report and final review                 | 4 hours    |  
| **03 Dec** | Finalizing project and submitting                               | 2 hours    |  

**Total Hours: 55 hours**  

---

### Nirodha Sandaruwani Meneripitiyage Dona

| Day        | Task Information                                               | Time Spent |  
|------------|-----------------------------------------------------------------|------------|  
| **12 Nov** | Initial project planning, deciding on technologies and tools    | 1 hour     |  
| **14 Nov** | Setting up backend server (Node.js, Express)                    | 4 hours    |  
| **15 Nov** | Implementing database schema for recipes and ingredients        | 4 hours    |  
| **16 Nov** | Developing backend logic for recipe management                 | 4 hours    |  
| **19 Nov** | Implementing recipe CRUD operations                             | 3 hours    |  
| **20 Nov** | Testing and fixing bugs in backend functionality                | 3 hours    |  
| **22 Nov** | Finalizing backend API (CRUD operations)                       | 4 hours    |  
| **23 Nov** | Testing and improving image upload functionality (Multer)       | 4 hours    |  
| **24 Nov** | Backend integration with frontend                               | 3 hours    |  
| **25 Nov** | Testing and bug fixing across all pages                         | 3 hours    |  
| **26 Nov** | Finalizing backend functionality (CRUD operations)             | 4 hours    |  
| **27 Nov** | Final testing of backend with frontend                         | 4 hours    |  
| **28 Nov** | Final integration of frontend and backend                       | 3 hours    |  
| **29 Nov** | Final testing and ensuring all features are working as expected| 3 hours    |  
| **30 Nov** | Documentation and writing project report                        | 5 hours    |  
| **01 Dec** | Project review and last-minute improvements    | 5 hours    |  
| **02 Dec** | Preparing project presentation and final review                 | 4 hours    |  
| **03 Dec** | Finalizing project and submitting                               | 2 hours    |  

**Total Hours: 60 hours**  

--- 

## 6. Strengths of the RecipeRider Project

1. **User-Friendly Interface**  
   The application boasts a clean and intuitive design, making it easy for users to search, add, and view recipes. The ingredient filtering and search features provide a seamless experience, ensuring that users can easily find what they are looking for.

2. **Robust Backend Functionality**  
   Built with Node.js and Express.js, the backend handles all CRUD operations for recipes and ingredients efficiently. This ensures smooth data management and interaction with the frontend. The API is structured in a way that makes it scalable for future improvements.

3. **Seamless Frontend-Backend Integration**  
   The integration between the frontend and backend is smooth, allowing users to interact with the app without any disruptions. Changes like adding or editing recipes are reflected in real-time on the user interface, enhancing the experience.

4. **Efficient Recipe Management**  
   Recipe addition, editing, and deletion are handled effectively within the app. Real-time updates ensure the UI stays synchronized with the backend, and the ability to upload images makes recipes more engaging and visually appealing.

5. **Smart Ingredient Filtering System**  
   One of the standout features is the intelligent ingredient filtering system. It allows users to easily find recipes that match specific ingredients, which is perfect for those looking to cook with what they already have at home.

6. **Scalable Database Structure**  
   Using MongoDB for the database gives the project a flexible and scalable data storage solution. The database structure is easy to extend, allowing for future enhancements such as user authentication, ratings, or even social sharing features.

7. **Great Team Collaboration**  
   Throughout the development of the project, Madee and Nirodha worked effectively together. Tasks were divided based on each team member’s strengths, which ensured that the project progressed smoothly and was completed successfully.

8. **Modern and Efficient Technology Stack**  
   The use of modern technologies like Node.js, Express.js, and MongoDB ensures the app is fast, efficient, and scalable. This technology stack also makes the app easy to maintain and upgrade as needed.

9. **Cross-Device Compatibility**  
   The platform is fully responsive, ensuring that users can access it on desktops, tablets, and mobile phones with the same great experience. The design adapts to different screen sizes, making it accessible on any device.

10. **Well-Documented Code and Features**  
    The project is thoroughly documented, making it easy for anyone to understand the code, the app’s features, and the development process. This is crucial for maintaining the project or making future contributions.

These strengths have all contributed to the success of the RecipeRider project, making it a functional, scalable, and user-friendly recipe management platform that delivers real value to users.

---

## 7. Weaknesses of the RecipeRider Project

1. **Limited User Authentication**  
   Currently, there is no user authentication system in place. Users cannot create personalized accounts or save their favorite recipes. Adding a user authentication feature would enhance user engagement and provide a more personalized experience, allowing users to store and access their preferences.

2. **No Recipe Rating or Feedback System**  
   The platform lacks a system for users to rate or provide feedback on recipes. Introducing a rating system would encourage users to engage with the content, help them discover the most popular recipes, and create a sense of community through reviews and comments.

3. **Limited Ingredient Information**  
   Ingredient information is relatively basic and does not include essential details like nutritional values, allergen information, or suggestions for substitutions. Expanding ingredient data would make the platform more useful, especially for users with dietary restrictions or those who need specific alternatives for certain ingredients.

These weaknesses, while present, can be addressed with future improvements and enhancements. Implementing solutions to these areas would further strengthen the RecipeRider project and contribute to a more robust platform for its users.

---

## 8. Reflection and Grade Proposal

As a team, we are proud of the work we've accomplished with **RecipeRider**. Over the past three weeks, we’ve tackled a wide range of challenges, from designing a user-friendly interface to implementing the backend functionality. Our project has evolved significantly, and we feel that it meets the core objectives we set out to achieve.

Throughout the development process, we focused on delivering a functional, efficient, and easy-to-use platform for managing recipes. We worked well together, combining our individual strengths and learning from each other. From coding the front end and backend to testing features and fixing bugs, we demonstrated strong teamwork and problem-solving skills.

Although there were areas for improvement, such as adding user authentication and expanding the search functionality, we believe these weaknesses are manageable and do not undermine the overall effectiveness of the platform.

Considering the amount of time and effort we dedicated to the project, the quality of the work we've produced, and our successful implementation of essential features, we propose a grade of **5** for our practice work. We feel that we have met the expectations for this project and have demonstrated the skills required for the course. We are confident that we have created a solid foundation for future development and improvements.

In conclusion, this project has been a valuable learning experience, and we are excited to submit it to our lecturer. We hope to continue developing **RecipeRider** in the future, adding more features and refining the platform based on user feedback and new ideas.
