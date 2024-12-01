const db = require('./connection');

// Create a `users` table (example)
const createUsersTable = () => {
    const query = `
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    `;
    db.query(query, (err, results) => {
        if (err) {
            console.error('Failed to create table: ', err.message);
        } else {
            console.log('Users table ready.');
        }
    });
};

module.exports = { createUsersTable };
