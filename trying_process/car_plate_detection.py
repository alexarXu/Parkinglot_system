'''================================================================================================
This script is a trying process to detect license plate from an image. The process is as follows:
1. Preprocess the image by converting it to grayscale, applying Gaussian blur, and adaptive thresholding.
2. Find contours that could represent a license plate based on size, aspect ratio, and rectangularity.
3. Extract characters from the license plate region by thresholding, morphological operations, and contour detection.

But unfortunately, the process is not working well. The license plate region is not detected properly.
So I will use another package to detect the license plate region, which is HyperLPR3.
================================================================================================
'''



import cv2
import numpy as np
import hyperlpr3 as lpr3


def preprocess_image(image_path):
    """Load and preprocess the image."""
    # Load image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use adaptive thresholding for better segmentation of white license plates
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)

    # Invert the binary image (white background, black text)
    binary = cv2.bitwise_not(binary)

    return image, gray, binary

def find_license_plate_contours(binary):
    """Find contours that could represent a license plate."""
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours by size, aspect ratio, and rectangularity
    potential_plates = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        area = cv2.contourArea(contour)
        rect_area = w * h
        extent = area / rect_area if rect_area > 0 else 0

        # Conditions for a license plate
        if 2 < aspect_ratio < 6 and 1000 < area < 50000 and 0.5 < extent < 0.9:
            potential_plates.append((x, y, w, h))

    return potential_plates

def extract_characters(plate_image):
    """Extract characters from the license plate region."""
    # Convert to grayscale
    gray_plate = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)

    # Thresholding
    _, binary_plate = cv2.threshold(gray_plate, 127, 255, cv2.THRESH_BINARY_INV)

    # Morphological operations to clean noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    binary_plate = cv2.morphologyEx(binary_plate, cv2.MORPH_CLOSE, kernel)

    # Find contours for characters
    contours, _ = cv2.findContours(binary_plate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    characters = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Filter small contours (noise) by size and aspect ratio
        if 0.3 < w / h < 1.5 and h > 15:
            char_image = binary_plate[y:y+h, x:x+w]
            characters.append((x, char_image))

    # Sort characters by x-coordinate (left to right)
    characters = sorted(characters, key=lambda x: x[0])

    return [char[1] for char in characters]

def main(image_path):
    # Step 1: Preprocess the image
    image, gray, binary = preprocess_image(image_path)

    # Step 2: Find potential license plate contours
    plate_contours = find_license_plate_contours(binary)

    # Step 3: Process each detected license plate
    for x, y, w, h in plate_contours:
        plate_image = image[y:y+h, x:x+w]

        # Verify the detected region has text-like properties
        if w > 100 and h > 30:  # Additional size constraints

            # Extract characters from the license plate
            characters = extract_characters(plate_image)

            # Display detected characters
            for idx, char in enumerate(characters):
                cv2.imshow(f'Character {idx+1}', char)

            cv2.imshow('License Plate', plate_image)
            cv2.waitKey(0)

    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    main(r"C:\Users\administer\Downloads\ALPR_IndonesiaPlateNumber_ComputerVision-main\test images\1111.jpg")
