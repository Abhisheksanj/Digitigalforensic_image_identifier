from flask import Flask, render_template, request, redirect, url_for, flash
from PIL import Image
from PIL.ExifTags import TAGS

app = Flask(__name__)

def extract_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data is not None:
                exif_info = {}
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    exif_info[tag_name] = value
                return exif_info
            else:
                return None
    except Exception as e:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = file.filename
            file_path = f"CyberSecurityForensic/static/{filename}"  # Set the path to the image in the "static" folder
            file.save(file_path)

            exif_data = extract_image_metadata(file_path)

            return render_template('results.html',filename=filename, exif_data=exif_data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
