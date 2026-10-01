# RecipeRider — Recipe Manager

A full-stack recipe management prototype for browsing, searching, adding, editing, and managing recipes and their ingredients.

## Features

- Browse and search recipes
- Filter recipes using ingredients and categories
- Add, edit, and delete recipes
- Upload recipe images
- Store recipe and ingredient data in MongoDB
- REST-style backend endpoints for recipe operations

## Tech Stack

`JavaScript` · `HTML` · `CSS` · `Node.js` · `Express` · `MongoDB` · `Mongoose` · `Multer`

## Run Locally

Create a `.env` file with your MongoDB connection string:

```env
MONGO_URI=your_mongodb_connection_string
```

Then install the dependencies and start the server:

```bash
npm install
node server.js
```

The server runs on `http://localhost:5000` by default.