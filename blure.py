import cv2

def apply_gaussian_blur(image_path):
    """
    Loads an image, applies a Gaussian blur, and displays both images.

    Args:
        image_path (str): The path to the image file.
    """
    # Load the image from the specified path
    image = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return

    # Apply Gaussian blur to the image
    # The second argument (15, 15) is the kernel size (width, height)
    # The third argument (0) is the standard deviation in X and Y direction (or 0 for automatic calculation)
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)

    # Display the original image
    cv2.imshow("Original Image", image)

    # Display the blurred image
    cv2.imshow("Blurred Image", blurred_image)

    # Wait indefinitely for a key press (0 means wait forever)
    # This keeps the windows open until a key is pressed
    cv2.waitKey(0)

    # Destroy all OpenCV windows opened by the program
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Specify the path to your image file
    # Replace "your_image.jpg" with the actual path to an image on your system
    image_file = "image.png"
    apply_gaussian_blur(image_file)