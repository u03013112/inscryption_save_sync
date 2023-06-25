from flask import Flask, request, send_file
import os

app = Flask(__name__)
save_file_path = '/app/SaveFile.gwsave'

@app.route('/upload', methods=['POST'])
def upload_save():
    if 'file' not in request.files:
        return 'No file found', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    file.save(save_file_path)
    return 'File uploaded successfully', 200

@app.route('/download', methods=['GET'])
def download_save():
    if not os.path.exists(save_file_path):
        return 'No save file found', 404

    return send_file(save_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
