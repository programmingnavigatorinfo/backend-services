
require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");
const app = express();
const port = 3000;

// Use the Mongo URI from the .env file
const mongoURI = process.env.MONGO_URI;

// Connect to MongoDB Atlas
mongoose
  .connect(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => {
    console.log("MongoDB connected");
  })
  .catch((err) => {
    console.error("MongoDB connection error:", err);
  });

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});