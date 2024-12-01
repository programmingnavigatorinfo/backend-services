const express = require('express');
const mongoose = require('mongoose');
const multer = require('multer');
const path = require('path');
const cors = require('cors');

// Initialize express app
const app = express();
const PORT = process.env.PORT || 3000;

// MongoDB connection
mongoose.connect('mongodb+srv://programmingnavigatorinfo:ProgrammingNavigator%401234@cluster0.2hthl.mongodb.net/BACKEND_PORTFOLIO?retryWrites=true&w=majority', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => console.log('MongoDB connected'))
  .catch(err => console.log('MongoDB connection error:', err));


// Start server
app.listen(PORT, () => console.log(`Server is running on port ${PORT}`));


// Middleware to parse JSON
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());


// Define Mongoose schema and model for media
const mediaFileSchema = new mongoose.Schema({
  title: String,
  size: Number,
  fileData: Buffer,
});
const MediaFile = mongoose.model('Media_File', mediaFileSchema);


// Multer setup for file uploads

const storage = multer.memoryStorage();
const upload = multer({ storage: storage, limits: { fileSize: 50 * 1024 * 1024 } });

// POST route to upload a file
app.post('/upload', upload.single('file'), async (req, res) => {
  const { title } = req.body;
  const file = req.file;

  if (!file) return res.status(400).send({ message: 'No file uploaded' });

  try {

    const mediaFile = new MediaFile({title,size:file.size,fileData:file.buffer})
    await mediaFile.save();

    res.status(200).send({
      status: 'success',
      message: `File uploaded successfully: ${mediaFile._id}`,
      data: mediaFile._id,
    });
  } catch (err) {
    res.status(500).send({ status: 'failed', message: 'Failed to upload file', error: err.message });
  }
});

// GET route to download a file
app.get('/download/:id', async (req, res) => {
  const { id } = req.params;

  try {
    const mediaFile = await MediaFile.findById(id)
    
    if(!mediaFile) return  res.status(400).send({ message: 'No file uploaded' });

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
    res.send(mediaFile.fileData); // Send the file content as response
  } catch (err) {
    res.status(500).send({ message: 'Failed to download file', error: err.message });
  }
});