import torch
import torchvision.transforms as transforms
from PIL import Image
import requests
from io import BytesIO

# Load Pre-trained Model (ResNet)
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.eval()

# Define Image Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Function to Classify Waste Image
def classify_waste(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)

    categories = ["Recyclable", "Compostable", "Landfill"]  # Dummy classes
    return categories[predicted.item() % 3]  # Simulate waste classification

# Test Classification
image_url = "'/Users/aran/Desktop/waste classifier/paper cup.webp'"
result = classify_waste(image_url)
print(f"Predicted Waste Category: {result}")
