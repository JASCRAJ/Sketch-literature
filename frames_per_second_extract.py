import cv2
import os

# Set the path to your MP4 file and the folder to save frames

filename = "225053fgsdl"
folder_name= "artworks_18_04_seg_selected"
video_path = f'results/{folder_name}/{filename}-combined-sequence-brush_7-combined-output-video-polygonandcropimageR1.mp4' 
#video_path = f'results/{folder_name}/{filename}.mp4'
# Replace with your video path
output_folder = f'results/frames/{folder_name}/{filename}/'  # Folder where frames will be saved

# Specify the desired frames per second to extract
desired_fps = 6  # Change this to 5 for 5 frames/sec or 2 for 2 frames/sec

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Open the video file
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total frames
duration = frame_count / fps  # Duration in seconds
frames_to_skip = int(fps / desired_fps)  # Calculate frames to skip

print(f"Video FPS: {fps}, Duration: {duration}s, Total frames: {frame_count}, Frames to skip: {frames_to_skip}")

frame_num = 0
saved_frame_count = 0

# Loop through all frames
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Save only the desired frames
    if frame_num % frames_to_skip == 0:
        frame_filename = os.path.join(output_folder, f'frame_{saved_frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
        saved_frame_count += 1

    frame_num += 1

# Release the video capture object
cap.release()

print(f"{saved_frame_count} frames extracted to {output_folder}")
