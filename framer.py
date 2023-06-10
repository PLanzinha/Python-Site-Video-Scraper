import os
import cv2


def extract_frames_from_videos(video_directory):
    # Count the number of videos already framed
    videos_skipped = 0

    # Iterate over the video folders in the video directory
    for folder_name in os.listdir(video_directory):
        folder_path = os.path.join(video_directory, folder_name)

        # Check if the item in the video directory is a folder
        if os.path.isdir(folder_path):
            # Iterate over the video files in the video folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)

                # Check if the file is a video file
                if os.path.isfile(file_path) and file_name.lower().endswith('.mp4'):
                    # Create a folder to store frames for each video
                    video_name = os.path.splitext(file_name)[0]
                    video_frames_directory = os.path.join(folder_path, f"{video_name}_frames")
                    os.makedirs(video_frames_directory, exist_ok=True)

                    # Open the video file
                    video = cv2.VideoCapture(file_path)

                    # Initialize frame counter
                    frame_count = 0

                    # Read frames from the video
                    while True:
                        # Read the next frame
                        ret, frame = video.read()

                        # If the frame was not read successfully, exit the loop
                        if not ret:
                            break

                        # Resize the frame
                        resized_frame = cv2.resize(frame, (300, 300))

                        # Convert the frame to grayscale
                        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

                        # Save the frame as an image file
                        frame_path = os.path.join(video_frames_directory, f"{video_name}_frame_{frame_count}.jpg")
                        cv2.imwrite(frame_path, gray_frame)

                        # Increment the frame counter
                        frame_count += 1

                    # Release the video file
                    video.release()

                    print(f"Frames extracted for {file_name}")

            videos_skipped += 1

    print(f"Total videos: {len(os.listdir(video_directory))}")
    print(f"Videos already framed: {videos_skipped}")


video_directory = "D:/videos_data"
extract_frames_from_videos(video_directory)
