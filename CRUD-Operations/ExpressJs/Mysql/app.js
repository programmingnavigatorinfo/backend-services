const express = require('express');
const bodyParser = require('body-parser');
const { createUsersTable } = require('./db/tables');
const userRoutes = require('./routes/users');

const mongoose = require('./db/connection');

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json());

// Initialize tables
createUsersTable();

// Routes
app.use('/api/users', userRoutes);

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
