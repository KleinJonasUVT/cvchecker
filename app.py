from flask import Flask, render_template, jsonify, request, redirect, session, url_for, make_response
from GPT_cv import get_gpt_response
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set the upload folder path and allowed extensions
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def get_cv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        gpt_response = get_gpt_response(filepath)
        return jsonify({'result': gpt_response})
    
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True, port=8080)