from flask import Flask, request, jsonify, send_from_directory
from flask_caching import Cache
from PIL import Image
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ABC_Task2",
        user="your_username",
        password="your_password"
    )
    return conn


# Ensure upload directory exists
UPLOAD_FOLDER = 'file_repositories'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Image compression function
def compress_image(image_path):
    img = Image.open(image_path)
    img.save(image_path, optimize=True, quality=85)

# Endpoint to upload files
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        compress_image(file_path)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO files (file_name, file_path, file_size, upload_date) VALUES (%s, %s, %s, %s)",
            (file.filename, file_path, os.path.getsize(file_path), datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "File uploaded successfully"}), 201

# Endpoint to delete files
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM files WHERE file_name = %s", (filename,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "File deleted successfully"}), 200
    else:
        return jsonify({"error": "File not found"}), 404

# Endpoint on summary of stored files
@app.route('/summary', methods=['GET'])
@cache.cached(timeout=60)
def summary():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), SUM(file_size) FROM files")
    summary = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({"total_files": summary[0], "total_size": summary[1]}), 200

# Endpoint listing all stored file's metadata
@app.route('/files', methods=['GET'])
@cache.cached(timeout=60)
def list_files():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT file_name, file_path, file_size, upload_date FROM files")
    files = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(files), 200

# Security checks before file upload
@app.before_request
def before_request():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed"}), 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
