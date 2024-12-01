const express = require('express');
const multer = require('multer');
const path = require('path');
const mysql = require('mysql2/promise');
const cors = require('cors');
const { error } = require('console');
const { SELECT } = require('sequelize/lib/query-types');

// Initialize express app
const app = express();
const PORT = process.env.PORT || 3000;

// MySQL Database connection
const connection = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'mouli',
  database: 'mydb'
});

app.use(express.json());
app.use(cors());

const startServer = async () => {
  try {
    await connection.getConnection(); 
    console.log('Database connected successfully.');

    app.listen(PORT, () => {
      console.log(`Server is running on port ${PORT}`);
    });
  } catch (error) {
    console.error('Error connecting to the database:', error);
  }
};

startServer();


// Multer setup for file uploads
const storage = multer.memoryStorage();
const upload = multer({ storage: storage, limits: { fileSize: 50 * 1024 * 1024 } }); // 50MB limit

// POST route to upload a file
app.post('/upload', upload.single('file'), async (req, res) => {
  const { title } = req.body;
  const file = req.file;

  if (!file) return res.status(400).send({ message: 'No file uploaded' });

  try {
    // Use connection.execute() to insert data into MySQL using a connection pool
    const [rows] = await connection.execute(
      'INSERT INTO media_query (title, size, file_data) VALUES (?, ?, ?)',
      [title, file.size, file.buffer]
    );

    // Get the ID of the inserted file
    const fileId = rows.insertId;

    res.status(200).send({
      status: 'success',
      message: `File uploaded successfully: ${fileId}`,
      data: fileId,
    });
  } catch (err) {
    res.status(500).send({ status: 'failed', message: 'Failed to upload file', error: err.message });
  }
});

// GET route to download a file
app.get('/download/:id', async (req, res) => {
  const { id } = req.params;

  try {
    // Retrieve the file from MySQL using a query
    const [rows] = await connection.execute('SELECT * FROM media_query WHERE id = ?', [id]);

    if (rows.length === 0) {
      return res.status(404).send({ message: 'File not found' });
    }

    const mediaFile = rows[0];
    const fileExtension = path.extname(mediaFile.title).toLowerCase();
    const contentTypes = {
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.png': 'image/png',
      '.pdf': 'application/pdf',
      '.mp4': 'video/mp4',
    };

    res.setHeader('Content-Type', contentTypes[fileExtension] || 'application/octet-stream');
    res.setHeader('Content-Disposition', `attachment; filename=${mediaFile.title}`);
    res.setHeader('Content-Length', mediaFile.size);
    res.send(mediaFile.file_data); // Send the file content as response
  } catch (err) {
    res.status(500).send({ message: 'Failed to download file', error: err.message });
  }
});