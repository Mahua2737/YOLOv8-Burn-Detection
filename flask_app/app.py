import io
from flask import Flask, request, render_template, url_for, send_from_directory, jsonify
import base64
from PIL import Image
from ultralytics import YOLO
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set upload and result folders
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "runs/detect"  # Default YOLO save location for results
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed file extensions for image uploads
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


# Function to check allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def image_to_base64(image_path):
    # Open the image file
    with open(image_path, "rb") as image_file:
        # Read the image file and encode it to base64
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


model = YOLO(r"E:\\python\\VisionHack_CV_ETE\\runs\\detect\\train5\\weights\\best.pt")


# Custom route to serve images from runs/detect folder
@app.route("/runs/detect/<path:filepath>")
def serve_result_image(filepath):
    result_path = os.path.join(RESULT_FOLDER, filepath)
    if os.path.exists(result_path):
        return send_from_directory(RESULT_FOLDER, filepath)
    else:
        return "Image not found", 404


@app.route("/detect", methods=["POST"])
def detect_burn():
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image data provided"}), 400

    # Get the Base64 string
    base64_image = data["image"]

    try:
        # Decode the Base64 string
        image_data = base64.b64decode(base64_image)

        # Optionally, you can convert it to an image object using PIL
        image = Image.open(io.BytesIO(image_data))
        # You can now manipulate the image if needed

        file_path = os.path.join("uploads", "image.png")

        with open(file_path, "wb") as image_file:
            image_file.write(image_data)

        absolute_file_path = os.path.abspath(file_path)

        results = model.predict(
            source=absolute_file_path,
            save=True,
        )

        result_image_final = os.path.abspath(
            results[0].save_dir + "/" + "image" + ".jpg"
        )

        base64_string = image_to_base64(result_image_final)

        return (
            jsonify(
                {
                    "message": "Image received successfully",
                    "result_image": base64_string,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            results = model.predict(
                source=filepath,
                save=True,
            )

            result_folder = results[0].save_dir
            result_image_name = filename

            result_image_url = url_for(
                "serve_result_image",
                filepath=os.path.relpath(
                    os.path.join(result_folder, result_image_name), RESULT_FOLDER
                ),
            )

            return render_template("index.html", result_image=result_image_url)

        else:
            return render_template(
                "index.html",
                result_image=None,
                error="Invalid file type. Only images are allowed.",
            )

    return render_template("index.html", result_image=None, error=None)


os.makedirs("uploads", exist_ok=True)

if __name__ == "__main__":
    app.run(debug=True)
