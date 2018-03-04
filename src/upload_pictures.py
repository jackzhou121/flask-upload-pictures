import os
from flask import Flask, request, render_template, send_from_directory

__author__ = 'ibininja'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

    #return render_template("complete.html", image_name=filename)
    image_names = os.listdir('./images')
    print(image_names)

    return render_template("gallery.html", image_names=image_names)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)


@app.route("/process_image", methods=['POST'])
def process_image():
    print("Your pictures are being processing....")
    image_names = os.listdir('./images')
    print(image_names)
    process_image_in_ssd_neural_network(image_names)
    return render_template("complete_display_image.html", input_image_names=image_names, output_image_names=image_names)


def process_image_in_ssd_neural_network(image_list):
    for image in image_list:
        print(image)


if __name__ == "__main__":
    app.run(port=4555, debug=True)
