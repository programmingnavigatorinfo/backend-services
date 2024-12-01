from flask import Flask, request, jsonify, redirect, send_file
import mysql.connector
from flask_cors import CORS
import base64
import io


app = Flask(__name__)
CORS(app)

# Database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mouli',  # Update with your MySQL password
    'database': 'media_db'
}

def db_connection():
    conn = mysql.connector.connect(**db_config)
    print('Database Connected!!')
    return conn







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
    conn = db_connection()
    cursor = conn.cursor()
    l1=[('image', ALLOWED_IMAGE_EXTENSIONS),('video', ALLOWED_VIDEO_EXTENSIONS),('document', ALLOWED_DOCUMENT_EXTENSIONS)]
    for file_key, allowed_extensions in l1:
        file = files.get(file_key)
        if file:
            # Validate file type
            if not allowed_file(file.filename, allowed_extensions):
                errors.append(f"Invalid file type for {file_key}. Allowed types: {', '.join(allowed_extensions)}.")
                continue
            # Save valid files to the database
            file_name = file.filename
            file_type = file.content_type
            file_data = file.read()
            cursor.execute("INSERT INTO media_files (file_name, file_type, file_data) VALUES (%s, %s, %s)",(file_name, file_type, file_data) )
    conn.commit()
    cursor.close()
    conn.close()
    if errors:
        return jsonify({"status": "error", "message": " | ".join(errors)}), 400
    return jsonify({"status": "success", "message": "Files uploaded successfully!"})

@app.route('/display', methods=['GET'])
def display_files():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, file_name, file_type, file_data FROM media_files")
    files = cursor.fetchall()
    cursor.close()
    conn.close()
    media_data = []
    for file_id, file_name, file_type, file_data in files:
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

@app.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, file_data FROM media_files WHERE id = %s", (file_id,))
    file = cursor.fetchone()
    cursor.close()
    conn.close()
    if file:
        file_name, file_data = file
        if file_name.endswith('.pdf'):
            return send_file(io.BytesIO(file_data), mimetype='application/pdf', as_attachment=False, download_name=file_name)
        return send_file(io.BytesIO(file_data), as_attachment=True, download_name=file_name)
    else:
        return jsonify({'message': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
