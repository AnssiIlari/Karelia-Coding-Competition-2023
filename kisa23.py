import csv
from PIL import Image
import numpy as np

# Load the pixel coordinates from the CSV file
csv_file_path = 'data.csv'
pixel_coordinates = []

#Getting information from the csv in correct form
with open(csv_file_path, newline='') as csvfile:
    pixel_reader = csv.reader(csvfile, delimiter=';')
    for row in pixel_reader:
        # Each row contains coordinates in the form 'x,y'
        for coordinate in row:
            if coordinate:  # Check if the coordinate is not empty
                x, y = map(int, coordinate.split(','))
                # Add to the list
                pixel_coordinates.append((x, y))

# Load the scrambled image
scrambled_image = Image.open('mixed.png')

# Get the size of the image to create a new image of the same size
img_width, img_height = scrambled_image.size

# Create a new image with the same mode and size as the scrambled image
unscrambled_image = Image.new(scrambled_image.mode, (img_width, img_height))

# Create a numpy array of the scrambled image for pixel access
scrambled_pixels = np.array(scrambled_image)

# Function to get pixel value from scrambled image
def get_pixel_value(x, y):
    # Get pixel value at the specified coordinates
    return scrambled_pixels[y, x]

# For loop for building the new image
for idx, (x, y) in enumerate(pixel_coordinates):
    # Calculate the new x, y coordinates in the unscrambled image
    new_y, new_x = divmod(idx, img_width)
    # Get the pixel value from the scrambled image
    pixel_value = get_pixel_value(x, y)
    # Place the pixel in the new image
    unscrambled_image.putpixel((new_x, new_y), tuple(pixel_value))

# Save the solved image
unscrambled_image.save('unmixed.png')


def extract_secret_from_alpha(image):
    # Get the pixel data from the image
    pixels = list(image.getdata())

    # Extract the alpha value from each pixel and convert it to a character
    message = ''.join(chr(p[3]) for p in pixels if p[3] != 255)

    return message

# Extract the secret message
secret_message = extract_secret_from_alpha(unscrambled_image)

print(secret_message)

