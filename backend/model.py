from transformers import BlipProcessor, BlipForConditionalGeneration, CLIPProcessor, CLIPModel, DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import torch
import requests
import base64
from io import BytesIO

# COCO class labels (DETR is trained on COCO dataset)
COCO_CLASSES = [
    "N/A", "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "N/A", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "N/A", "backpack",
    "umbrella", "N/A", "N/A", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "N/A", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
    "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut",
    "cake", "chair", "couch", "potted plant", "bed", "N/A", "dining table", "N/A", "N/A",
    "toilet", "N/A", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "N/A", "book", "clock", "vase", "scissors",
    "teddy bear", "hair drier", "toothbrush"
]

# Load models from local directory
print("Loading BLIP model...")
blip_processor = BlipProcessor.from_pretrained("D:/infosys_internship/AI-agent/saved_models/blip")
blip_model = BlipForConditionalGeneration.from_pretrained("D:/infosys_internship/AI-agent/saved_models/blip")

print("Loading CLIP model...")
clip_processor = CLIPProcessor.from_pretrained("D:/infosys_internship/AI-agent/saved_models/clip")
clip_model = CLIPModel.from_pretrained("D:/infosys_internship/AI-agent/saved_models/clip")

print("Loading DETR model...")
detr_processor = DetrImageProcessor.from_pretrained("D:/infosys_internship/AI-agent/saved_models/detr")
detr_model = DetrForObjectDetection.from_pretrained("D:/infosys_internship/AI-agent/saved_models/detr")

def generate_caption(image):
    inputs = blip_processor(image, return_tensors="pt")
    out = blip_model.generate(**inputs)
    caption = blip_processor.decode(out[0], skip_special_tokens=True)
    return caption

def classify_context(image, objects):
    text = [f"a photo of a {obj}" for obj in objects]
    inputs = clip_processor(text=text, images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)
    return probs.tolist()

def detect_objects(image):
    try:
        # Preprocess the image
        inputs = detr_processor(images=image, return_tensors="pt")
        
        # Perform object detection
        with torch.no_grad():
            outputs = detr_model(**inputs)

        # Get the detected objects
        logits = outputs.logits
        prob = logits.softmax(-1)
        scores = prob[0, :, :-1].max(-1).values
        labels = prob[0, :, :-1].argmax(-1).tolist()

        # Filter out low-confidence detections
        keep = scores > 0.9  # Adjust threshold as needed
        detected_objects = [COCO_CLASSES[label] for label, keep_flag in zip(labels, keep) if keep_flag]

        return detected_objects
    except Exception as e:
        print(f"Error detecting objects: {e}")
        return []

def generate_detailed_description(image):
    # Convert image to base64
    image_base64 = image_to_base64(image)

    # Gemini API endpoint for the new model (gemini-1.5-flash)
    gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    # Headers with API key
    headers = {
        "Content-Type": "application/json"
    }

    # Payload with the image and prompt
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Describe this image in detail."
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
    }

    # Add API key as a query parameter
    params = {
        "key": "AIzaSyBc1C6HZlNnubqBtOK1QeWtz5-t0m_Wn48"  # Your Gemini API key
    }

    try:
        # Make the API request
        response = requests.post(gemini_url, headers=headers, json=payload, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response
            response_data = response.json()
            description = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No detailed description generated.")
            return description
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return "Failed to generate detailed description."
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Failed to generate detailed description."

def generate_medical_description(image):
    inputs = blip_processor(image, return_tensors="pt")
    out = blip_model.generate(**inputs, max_length=100)
    description = blip_processor.decode(out[0], skip_special_tokens=True)
    return description

def detect_anatomy(image):
    inputs = detr_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = detr_model(**inputs)
    logits = outputs.logits
    prob = logits.softmax(-1)
    labels = prob[0, :, :-1].argmax(-1).tolist()
    detected_anatomy = [COCO_CLASSES[label] for label in labels]
    return detected_anatomy

def generate_hashtags(image):
    caption = generate_caption(image)
    hashtags = ["#" + word for word in caption.split() if len(word) > 3][:5]
    return hashtags

def generate_engagement_tips(image):
    return "Post during peak hours and use relevant hashtags."

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")