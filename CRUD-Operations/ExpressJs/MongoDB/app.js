
require('dotenv').config()

const express = require('express');
const mongoose = require('./db/connection');
const bodyParser = require('body-parser');
const cors = require('cors');
const userRoutes = require('./routes/users');
const app = express();
const port = process.env.PORT || 4000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Routes
app.use('/api/users', userRoutes);

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
