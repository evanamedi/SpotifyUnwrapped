from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import threading
import webbrowser
from werkzeug.utils import secure_filename
import pandas as pd
from data_processing import load_data, clean_data, save_clean_data
from plotting import plot_top_artists, plot_top_tracks, plot_listening_trends

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
IMAGE_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        files = request.files.getlist('files[]')
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'status': 'Files uploaded successfully'})
    except Exception as e:
        print(f"Error uploading files: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/process_files', methods=['POST'])
def process_files_route():
    try:
        files = [os.path.join(UPLOAD_FOLDER, file) for file in os.listdir(UPLOAD_FOLDER)]
        df = load_data(UPLOAD_FOLDER)
        df = clean_data(df)
        save_clean_data(df, 'cleaned_data.csv')
        return jsonify({'status': 'Files processed successfully'})
    except Exception as e:
        print(f"Error processing files: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/plot', methods=['POST'])
def plot_route():
    plot_type = request.json.get('plot_type')
    output_file = f'{IMAGE_FOLDER}/{plot_type}.png'
    
    try:
        df = pd.read_csv('cleaned_data.csv', parse_dates=['ts'], low_memory=False)
        
        if plot_type == 'top_artists':
            plot_top_artists(df, output_file)
        elif plot_type == 'top_tracks':
            plot_top_tracks(df, output_file)
        elif plot_type == 'listening_trends':
            plot_listening_trends(df, output_file)
        else:
            return jsonify({'error': 'Unknown plot type'}), 400
        
        return jsonify({'image_path': '/' + output_file})
    except Exception as e:
        print(f"Error generating plot: {e}")
        return jsonify({'error': str(e)}), 500

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)