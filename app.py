# from matplotlib.colors import hex2color
from werkzeug.utils import secure_filename
# from importlib.metadata import requires
from flask import Flask, url_for, render_template, request, flash, redirect
# from markupsafe import escape
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from colorthief import ColorThief
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # production
# app.config['SECRET_KEY']=''

UPLOAD_FOLDER = "c:/top10color"  # '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def get_dominant_color(img_file):
    image = Image.open(img_file)
    img_arr = np.array(image)

    color_thief = ColorThief(img_file)
    dominant_color = color_thief.get_palette(color_count=11)
    hex_colors = []
    for c in dominant_color:
        # print(c)
        hex_colors.append('#%02x%02x%02x' % c)
    # print(dominant_color)
    # print(hex_colors)
    return hex_colors
    # print(img_arr)
    # print(img_arr.shape)


def find_dominant_color(filename):
    # Resizing parameters
    width, height = 1000, 665  # 150, 150
    image = Image.open(filename)
    image = image.resize((width, height), resample=0)
    # Get colors from image object
    pixels = image.getcolors(width * height)

    # Sort them by count number(first element of tuple)
    sorted_pixels = sorted(pixels, key=lambda t: t[0], reverse=True)
    # print(sorted_pixels)
    # Get the most frequent color
    dominant_colors = sorted_pixels[:10]
    # print(dominant_colors)
    return dominant_colors


# get_dominant_color('480.jpg')
# find_dominant_color('480.jpg')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    img = None
    color_dict = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('Please select image to extract the colors.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # print(filename)
            # print(app.config['UPLOAD_FOLDER'])
            file.save(f"./static/uploaded_images/{filename}")
            colors = get_dominant_color(
                f"./static/uploaded_images/{filename}")
            # return redirect(url_for('download_file', name=filename))
            return render_template('index.html', colors=colors, img=f"../static/uploaded_images/{filename}")
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)  # testing stage
    # app.run(host='0.0.0.0') # production, externally visible server
