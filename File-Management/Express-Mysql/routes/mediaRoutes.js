const express = require('express');
const multer = require('multer');
const { createMediaFile, findMediaFileById } = require('../models/MediaFile');
const path = require('path');

const router = express.Router();

// Multer configuration for file uploads
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Upload endpoint
router.post('/upload', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send('No file uploaded.');
    }

    const { title } = req.body;
    const { buffer, size } = req.file;

    // Save file data in the database
    const mediaFileId = await createMediaFile(title, size, buffer);

    res.status(200).send({ status: 'success', message: `File uploaded successfully: ${mediaFileId._id}`, data: mediaFileId._id });
  } catch (error) {
    console.error(error);
    res.status(500).send('Failed to upload file.');
  }
});

// Download endpoint
router.get('/download/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const mediaFile = await findMediaFileById(id);

    if (!mediaFile) {
      return res.status(404).send('File not found.');
    }

    const fileBuffer = mediaFile.file_data;
    const fileName = mediaFile.title;

    // Infer content type based on file extension
    const contentType = inferContentType(fileName);

    res.setHeader('Content-Disposition', `attachment; filename="${fileName}"`);
    res.setHeader('Content-Type', contentType);
    res.setHeader('Content-Length', fileBuffer.length);

    res.send(fileBuffer);
  } catch (error) {
    console.error(error);
    res.status(500).send('Failed to download file.');
  }
});

// Helper function to infer content type based on file extension
function inferContentType(filename) {
  const ext = path.extname(filename).toLowerCase();
  switch (ext) {
    case '.jpg':
    case '.jpeg':
      return 'image/jpeg';
    case '.png':
      
      return 'image/png';
    case '.gif':
      return 'image/gif';
    case '.pdf':
      return 'application/pdf';
    case '.mp4':
      return 'video/mp4';
    default:
      return 'application/octet-stream';
  }
}

module.exports = router;
