from flask import Flask, request, jsonify
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'frames'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/split', methods=['POST'])
def split_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'}), 400

    video = request.files['video']
    filename = secure_filename(video.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    video.save(input_path)

    output_path = os.path.join(OUTPUT_FOLDER, filename.split('.')[0] + '_%03d.jpg')

    try:
        subprocess.run(['ffmpeg', '-i', input_path, '-vf', 'select=gt(scene\,0.4)', '-vsync', 'vfr', output_path], check=True)
    except subprocess.CalledProcessError:
        return jsonify({'error': 'Failed to process video'}), 500

    frames = os.listdir(OUTPUT_FOLDER)
    return jsonify({'message': 'Frames extracted successfully', 'frames': frames})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
