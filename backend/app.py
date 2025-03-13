from flask import Flask, request, jsonify, send_from_directory
from model import generate_caption, classify_context, detect_objects, generate_detailed_description, generate_medical_description, detect_anatomy, generate_hashtags, generate_engagement_tips
from PIL import Image
import io

app = Flask(__name__)

# Serve the frontend files
@app.route("/")
def serve_frontend():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("../frontend", path)

# API endpoint for general image captioning
@app.route("/caption", methods=["POST"])
def caption_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    try:
        # Get the uploaded file
        image_file = request.files["image"]
        image = Image.open(io.BytesIO(image_file.read()))

        # Generate caption
        caption = generate_caption(image)

        # Detect objects
        objects = detect_objects(image)

        # Classify context
        context = classify_context(image, objects)

        # Generate detailed description
        detailed_description = generate_detailed_description(image)

        return jsonify({
            "caption": caption,
            "objects": objects,
            "context": context,
            "detailed_description": detailed_description
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for medical image analysis
@app.route("/medical-analysis", methods=["POST"])
def medical_analysis():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    try:
        image_file = request.files["image"]
        image = Image.open(io.BytesIO(image_file.read()))

        # Generate medical-specific analysis
        medical_description = generate_medical_description(image)
        detected_anatomy = detect_anatomy(image)

        return jsonify({
            "medical_description": medical_description,
            "detected_anatomy": detected_anatomy
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for social media analysis
@app.route("/social-media-analysis", methods=["POST"])
def social_media_analysis():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    try:
        image_file = request.files["image"]
        image = Image.open(io.BytesIO(image_file.read()))

        # Generate social media-specific analysis
        caption = generate_caption(image)
        hashtags = generate_hashtags(image)
        engagement_tips = generate_engagement_tips(image)

        return jsonify({
            "caption": caption,
            "hashtags": hashtags,
            "engagement_tips": engagement_tips
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for quick analysis
@app.route("/quick-analysis", methods=["POST"])
def quick_analysis():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    try:
        image_file = request.files["image"]
        image = Image.open(io.BytesIO(image_file.read()))

        # Generate quick analysis
        caption = generate_caption(image)
        objects = detect_objects(image)

        return jsonify({
            "caption": caption,
            "objects": objects
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)