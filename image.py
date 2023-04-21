from PIL import Image, ImageEnhance
import os

# Set the directory containing the images
directory = "images"

# Get a list of all the image files in the directory
image_files = [f for f in os.listdir(directory) if f.endswith(".jpg") or f.endswith(".png")]

# Calculate the average width of all the images in the directory
total_width = 0
for image_file in image_files:
    image = Image.open(os.path.join(directory, image_file))
    total_width += image.size[0]
average_width = int(total_width / len(image_files))

# Create a new blank image with the same height as all the images combined
total_height = 0
for image_file in image_files:
    image = Image.open(os.path.join(directory, image_file))
    # Calculate the new height of the image, based on the new width
    new_height = int(image.size[1] * (average_width / image.size[0]))
    # Resize the image to the new size
    resized_image = image.resize((average_width, new_height))
    total_height += new_height

# Generate a unique name for the new image based on the number of existing files
new_image_name = "combined_enhanced.png"
i = 1
while os.path.exists(new_image_name):
    new_image_name = "combined_enhanced ({})".format(i) + ".png"
    i += 1

# Create a new blank image with the appropriate size
new_image = Image.new("RGB", (average_width, total_height))

# Paste each image into the new image, vertically
current_height = 0
for image_file in image_files:
    # Open the image file
    image = Image.open(os.path.join(directory, image_file))
    # Enhance the image
    image = ImageEnhance.Brightness(image).enhance(2)
    image = ImageEnhance.Contrast(image).enhance(200)
    # Calculate the new height of the image, based on the new width
    new_height = int(image.size[1] * (average_width / image.size[0]))
    # Resize the image to the new size
    resized_image = image.resize((average_width, new_height))
    # Paste the resized image into the new image
    new_image.paste(resized_image, (0, current_height))
    # Update the current height to reflect the addition of the new image
    current_height += new_height

# Save the new image to disk
new_image.save(new_image_name)
