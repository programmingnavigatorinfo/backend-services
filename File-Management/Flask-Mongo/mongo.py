from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
from flask_cors import CORS
from bson import ObjectId
import base64
import io

app = Flask(__name__)
CORS(app)

# MongoDB connection
username = "programmingnavigatorinfo"
password = "ProgrammingNavigator@1234"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

mongo_url = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.2hthl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(mongo_url)
    db = client.BACKEND_PORTFOLIO  # Replace with your database name
    media_collection = db.media_files  # Collection for media files
    client.admin.command('ping')
    print("MongoDB connection successful.")
except ConnectionFailure as err:
    print(f"MongoDB connection failed: {err}")



# Allowed file extensions for validation
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov'}
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'doc'}

def allowed_file(filename, allowed_extensions):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/upload', methods=['POST'])
def upload_file():
    #print('I am in Upload Function')
    files = request.files
    errors = []

    # Validate and upload files
    for file_key, allowed_extensions in [
        ('image', ALLOWED_IMAGE_EXTENSIONS),
        ('video', ALLOWED_VIDEO_EXTENSIONS),
        ('document', ALLOWED_DOCUMENT_EXTENSIONS),
    ]:
        file = files.get(file_key)
        if file:
            # Validate file type
            if not allowed_file(file.filename, allowed_extensions):
                errors.append(f"Invalid file type for {file_key}. Allowed types: {', '.join(allowed_extensions)}.")
                continue

            # Save valid files to MongoDB
            file_name = file.filename
            file_type = file.content_type
            file_data = file.read()  # Read file as binary

            media_document = {
                "file_name": file_name,
                "file_type": file_type,
                "file_data": file_data
            }

            media_collection.insert_one(media_document)

    if errors:
        return jsonify({"status": "error", "message": " | ".join(errors)}), 400

    return jsonify({"status": "success", "message": "Files uploaded successfully!"})

@app.route('/display', methods=['GET'])
def display_files():
    #print('I am in Display Function')
    files = media_collection.find()  # Retrieve all files from MongoDB

    media_data = []
    for file in files:
        file_id = str(file["_id"])
        file_name = file["file_name"]
        file_type = file["file_type"]
        file_data = file["file_data"]

        media_item = {}
        if 'image' in file_type:
            # Convert image binary data to base64 for display
            img_base64 = base64.b64encode(file_data).decode('utf-8')
            media_item = {'type': 'image', 'src': f"data:{file_type};base64,{img_base64}"}
        elif 'video' in file_type:
            # Convert video binary data to base64 for display
            video_base64 = base64.b64encode(file_data).decode('utf-8')
            media_item = {'type': 'video', 'src': f"data:{file_type};base64,{video_base64}"}
        else:  # Document
            # Provide link for documents
            media_item = {'type': 'document', 'name': file_name, 'src': f"/download/{file_id}"}
        
        media_data.append(media_item)

    return jsonify({"status": "success", "media": media_data})

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    file = media_collection.find_one({"_id": ObjectId(file_id)})
    if file:
        file_name = file["file_name"]
        file_data = file["file_data"]
        if file_name.endswith('.pdf'):
            return send_file(io.BytesIO(file_data), mimetype='application/pdf', as_attachment=False, download_name=file_name)
        return send_file(io.BytesIO(file_data), as_attachment=True, download_name=file_name)
    else:
        return jsonify({'message': 'File not found'}), 404




if __name__ == '__main__':
    app.run(debug=True)
