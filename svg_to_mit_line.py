from transformers import AutoTokenizer, AutoModelForImageClassification, pipeline

# Load tokenizer and model with authentication token
tokenizer = AutoTokenizer.from_pretrained("carolineec/informativedrawings", use_auth_token=True)
model = AutoModelForImageClassification.from_pretrained("carolineec/informativedrawings", use_auth_token=True)

# Define a function to generate informative drawings
def generate_informative_drawing(image_path):
    # Initialize pipeline
    img_to_text = pipeline("image-classification", model=model, tokenizer=tokenizer)
    
    # Generate informative drawing
    drawing = img_to_text(image_path)
    
    return drawing

# Example usage with the provided image path
image_path = "Drawing/Erik Pedersen.jpg"
drawing = generate_informative_drawing(image_path)
print(drawing)
