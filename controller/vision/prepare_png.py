from PIL import Image

def resize_image_without_empty_space(image_path, output_path, padding=0):
    # Open the image
    image = Image.open(image_path)

    # Convert the image to RGBA mode to ensure it has an alpha channel
    image = image.convert("RGBA")

    # Find the bounding box of the non-empty region in the image
    bbox = image.getbbox()

    # Crop the image to the bounding box
    cropped_image = image.crop(bbox)

    # Calculate the new dimensions with optional padding
    new_width = cropped_image.width + 2 * padding
    new_height = cropped_image.height + 2 * padding

    # Create a new blank RGBA image with the new dimensions
    resized_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

    # Paste the cropped image into the center of the new image
    x_offset = (new_width - cropped_image.width) // 2
    y_offset = (new_height - cropped_image.height) // 2
    resized_image.paste(cropped_image, (x_offset, y_offset))

    # Save the resized image without empty space
    resized_image.save(output_path)

def crop_image_square(image_path, output_path, size):
    """Crops an image to a square at the center of the original image.
    args:
        image_path: The path to the image to edit.
        output_path: The path to save the cropped image.
        size: The size to crop the image to a square (width = height)."""
    
    # Open the image
    original_image = Image.open(image_path)
    
    # Get the original image dimensions
    original_width, original_height = original_image.size
    
    # Calculate the cropping box
    left = (original_width - size) // 2
    top = (original_height - size) // 2
    right = (original_width + size) // 2
    bottom = (original_height + size) // 2
    
    # Crop the image
    cropped_image = original_image.crop((left, top, right, bottom))
    
    # Save the cropped image
    cropped_image.save(output_path)

def crop_image_vertical(image_path, output_path, size):
    """Crops an image to a rectangle at the center of the original image. The longest side of the rectangle is the image height while the shorter side is the size argument in pixels.
    args:
        image_path: The path to the image to edit.
        output_path: The path to save the cropped image.
        size: The size to crop the image to a rectangle (shorter side)."""
    
    # Open the image
    original_image = Image.open(image_path)
    
    # Get the original image dimensions
    original_width, original_height = original_image.size
    
    # Calculate the cropping box
    left = (original_width - size) // 2
    top = 0
    right = (original_width + size) // 2
    bottom = original_height
    
    # Crop the image
    cropped_image = original_image.crop((left, top, right, bottom))
    
    # Save the cropped image
    cropped_image.save(output_path)
    

# Example usage:
input_image_path = "test2_crop.png"
output_image_path = "test2_empty_space.png"
resize_image_without_empty_space(input_image_path, output_image_path, padding=0)
# crop_image_square(input_image_path, output_image_path, size=512)
# crop_image_vertical(input_image_path, output_image_path, size=512)