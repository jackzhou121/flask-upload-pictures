import os
from flask import Flask, request, render_template, send_from_directory
import ssd_test
import sys

sys.path.append('../')

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    image_names = os.listdir('./images')
    return render_template("gallery.html", image_names=image_names)


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))

    for image in request.files.getlist("file"):
        filename = image.filename
        destination = "/".join([target, filename])
        image.save(destination)

    image_names = os.listdir('./images')

    return render_template("gallery.html", image_names=image_names)


@app.route("/back", methods=["POST"])
def back():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))

    image_names = os.listdir('./output_images')
    for image in image_names:
        try:
            os.remove('./output_images/' + image)
        except:
            print("remove failed", image)

    image_names = os.listdir('./images')

    return render_template("gallery.html", image_names=image_names)


@app.route("/show", methods=["POST"])
def show():
    target = os.path.join(APP_ROOT, 'output_images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create show directory: {}".format(target))
    image_names = os.listdir('./output_images')
    return render_template("gallery.html", image_names=image_names)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/show/<filename>')
def send_output_image(filename):
    return send_from_directory("output_images", filename)


@app.route("/process_image", methods=['POST'])
def process_image():
    for image in request.form.getlist('picture_list'):
        ssd_test.bndbox_image(image)

    output_image_names = os.listdir('./output_images')
    return render_template("complete_display_image.html",
                           output_image_names=output_image_names)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4556, debug=True)
