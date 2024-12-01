const mysql = require('mysql2/promise');

// MySQL Database connection
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'mouli',
  database: 'mydb'
});

module.exports = connection;
