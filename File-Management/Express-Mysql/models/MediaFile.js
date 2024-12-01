const connection = require('../config/db');

// Function to insert a media file
async function createMediaFile(title, size, file_data) {
  const query = 'INSERT INTO media_query (title, size, file_data) VALUES (?, ?, ?)';
  const [result] = await (await connection).execute(query, [title, size, file_data]);
  return result.insertId;
}

// Function to find a media file by ID
async function findMediaFileById(id) {
  const query = 'SELECT * FROM media_query WHERE id = ?';
  const [rows] = await (await connection).execute(query, [id]);
  return rows[0];
}

module.exports = { createMediaFile, findMediaFileById };
