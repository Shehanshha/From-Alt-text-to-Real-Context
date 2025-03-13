from transformers import BlipProcessor, BlipForConditionalGeneration, CLIPProcessor, CLIPModel, DetrImageProcessor, DetrForObjectDetection
import os

# Create a directory to save the models
os.makedirs("saved_models", exist_ok=True)

# Download and save BLIP model
print("Downloading and saving BLIP model...")
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
blip_processor.save_pretrained("saved_models/blip")
blip_model.save_pretrained("saved_models/blip")

# Download and save CLIP model
print("Downloading and saving CLIP model...")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor.save_pretrained("saved_models/clip")
clip_model.save_pretrained("saved_models/clip")

# Download and save DETR model
print("Downloading and saving DETR model...")
detr_processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
detr_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
detr_processor.save_pretrained("saved_models/detr")
detr_model.save_pretrained("saved_models/detr")

print("All models saved successfully!")