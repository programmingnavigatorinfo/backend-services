const express = require("express");
const mysql = require("mysql2"); // Using mysql2 for promise-based functionality
const app = express();
const port = 3000;

// Create a connection to the database
const db = mysql.createConnection({
  host: "localhost", // Replace with your MySQL host
  user: "root", // Replace with your MySQL username
  password: "mouli", // Replace with your MySQL password
  database: "mydb", // Replace with your database name
});

// Connect to the database
db.connect((err) => {
  if (err) {
    console.error("Could not connect to MySQL:", err);
  } else {
    console.log("Connected to MySQL");
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

