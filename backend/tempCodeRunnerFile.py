@app.route("/caption", methods=["POST"])
def caption_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    try:
        # Get the uploaded file
        image_file = request.files["image"]

        # Load image
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