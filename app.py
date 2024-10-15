from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
import cv2
from effects import apply_sepia, apply_bw, apply_vintage, apply_dramatic
from filters import reduce_noise, reduce_gaussian, reduce_salt_and_pepper, reduce_speckle, reduce_poisson
from video_effects import apply_bw_video

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def is_video(filename):
    return filename.lower().endswith(('.mp4', '.avi'))

@app.route('/', methods=['GET', 'POST'])
def index():
    previous_file = None
    processed_file = None
    if request.method == 'POST':
        file = request.files.get('file')
        previous_file = request.form.get('previous_file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            previous_file = filename
        elif previous_file:
            filename = previous_file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            return redirect(request.url)

        filter_type = request.form['filter_type']
        if filter_type == 'noise' and not is_video(filename):
            noise_type = request.form['noise_type']
            if noise_type == 'gaussian':
                processed_image = reduce_gaussian(filepath)
            elif noise_type == 'salt_and_pepper':
                processed_image = reduce_salt_and_pepper(filepath)
            elif noise_type == 'speckle':
                processed_image = reduce_speckle(filepath)
            elif noise_type == 'poisson':
                processed_image = reduce_poisson(filepath)
            else:
                processed_image = reduce_noise(filepath)
            processed_file = f"{filename}_{noise_type}.png"
            processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_file)
            cv2.imwrite(processed_image_path, processed_image)
        elif filter_type == 'effect':
            effect_type = request.form['effect_type']
            if effect_type == 'bw' and is_video(filename):
                processed_file = f"{filename}_bw.mp4"
                processed_video_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_file)
                apply_bw_video(filepath, processed_video_path)
            else:
                if effect_type == 'sepia':
                    processed_image = apply_sepia(filepath)
                elif effect_type == 'bw':
                    processed_image = apply_bw(filepath)
                elif effect_type == 'vintage':
                    processed_image = apply_vintage(filepath)
                elif effect_type == 'dramatic':
                    processed_image = apply_dramatic(filepath)
                processed_file = f"{filename}_{effect_type}.png"
                processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_file)
                cv2.imwrite(processed_image_path, processed_image)

    return render_template('index.html', previous_file=previous_file, processed_file=processed_file)

@app.route('/styles.css')
def css():
    return send_from_directory('.', 'styles.css')

if __name__ == "__main__":
    app.run(debug=True)
