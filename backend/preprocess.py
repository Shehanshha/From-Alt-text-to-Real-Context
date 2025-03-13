from PIL import Image
import io

def load_image_from_file(file):
    image = Image.open(file.stream)
    return image