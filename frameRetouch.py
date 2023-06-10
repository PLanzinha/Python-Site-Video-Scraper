import os
import cv2


def process_frames(frames_directory):
    # Iterate over the frames folders in the frames directory
    for folder_name in os.listdir(frames_directory):
        folder_path = os.path.join(frames_directory, folder_name)

        # Check if the item in the frames directory is a folder
        if os.path.isdir(folder_path):
            # Iterate over the frame files in the frames folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)

                # Check if the file is an image file
                if os.path.isfile(file_path) and file_name.lower().endswith('.jpg'):
                    # Read the image file
                    image = cv2.imread(file_path)

                    # Crop the image (example: crop 100 pixels from the top and bottom)
                    cropped_image = image[100:-100, :]

                    # Resize the image to a specific width and height (example: resize to 300x300)
                    resized_image = cv2.resize(cropped_image, (300, 300))

                    # Convert the image to grayscale
                    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

                    # Save the processed image
                    processed_file_path = os.path.join(folder_path, f"processed_{file_name}")
                    cv2.imwrite(processed_file_path, gray_image)


frames_directory = "path/to/frames_directory"
process_frames(frames_directory)
