const mysql = require('mysql2');

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'mouli',
    database: 'mydb',
});

db.connect((err) => {
    if (err) {
        console.error('Database connection failed: ', err.message);
    } else {
        console.log('Connected to the MySQL database.');
    }
});

module.exports = db;
