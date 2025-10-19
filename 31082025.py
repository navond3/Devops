import os
import cv2
from PIL import Image
import glob

import requests
from bs4 import BeautifulSoup
import os


def find_and_download_jpgs(url, download_dir="D\:downloaded5"):
    """
    Scans a webpage for .jpg image URLs and downloads them to a specified directory.
    """
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created directory: {download_dir}")

    try:
        # Fetch the HTML content, ignoring SSL certificate issues
        print(f"Fetching content from: {url}")
        response = requests.get(url, verify=False, timeout=10)
        response.raise_for_status()

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')

        jpg_urls = []
        for img in img_tags:
            src = img.get('src')
            if src and src.lower().endswith('.jpg'):
                full_url = requests.compat.urljoin(url, src)
                jpg_urls.append(full_url)

        if not jpg_urls:
            print("No .jpg images found on the page.")
            return

        print(f"Found {len(jpg_urls)} .jpg image(s). Starting download...")

        # Download each image found
        for i, img_url in enumerate(jpg_urls, 1):
            try:
                # Use a specific user-agent to avoid being blocked
                headers = {"User-Agent": "Mozilla/5.0"}

                # Use a unique filename for each image
                filename = f"image_{i}_{os.path.basename(img_url).split('?')[0]}"
                file_path = os.path.join(download_dir, filename)

                print(f"Downloading {i}/{len(jpg_urls)}: {img_url}")
                img_response = requests.get(img_url, headers=headers, stream=True, verify=False, timeout=10)
                img_response.raise_for_status()

                with open(file_path, 'wb') as file:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        file.write(chunk)

                print(f"Successfully downloaded to: {file_path}")

            except requests.exceptions.RequestException as e:
                print(f"  Error downloading {img_url}: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Error accessing the webpage: {e}")

def images_to_video(image_folder, video_name='output_video.mp4', fps=10):
    """
    Converts the first 15 JPG images in a folder to a video file.

    Args:
        image_folder (str): The path to the folder containing the images.
        video_name (str): The name of the output video file.
        fps (int): Frames per second for the output video.
    """

    # Check if the folder exists
    if not os.path.isdir(image_folder):
        print(f"Error: The folder '{image_folder}' does not exist.")
        return

    # Get a list of all jpg files and sort them
    images = sorted(glob.glob(os.path.join(image_folder, "*.jpg")))

    # Check if there are any images found
    if not images:
        print(f"Error: No .jpg images found in '{image_folder}'.")
        return

    # Take only the first 15 images
    images_to_process = images[:15]

    # Get the dimensions of the first image to set video resolution
    try:
        frame = cv2.imread(images_to_process[0])
        height, width, layers = frame.shape
        size = (width, height)
    except IndexError:
        print("Error: Could not read the first image. Check if it's corrupted.")
        return

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for .mp4 format
    out = cv2.VideoWriter(os.path.join(image_folder, video_name), fourcc, fps, size)

    print(f"Processing {len(images_to_process)} images...")

    for image in images_to_process:
        frame = cv2.imread(image)
        if frame is not None:
            out.write(frame)
            print(f"Added frame: {os.path.basename(image)}")
        else:
            print(f"Warning: Could not read image '{os.path.basename(image)}'. Skipping.")

    out.release()
    cv2.destroyAllWindows()
    print(f"\nVideo '{video_name}' created successfully in '{image_folder}'.")

#image_folder_path = r'D:\downloaded5'

# Define the output video file path
# The video will be saved in the same location as your Python script
output_video_file = r'D:\downloaded5\my_vacation_video.mp4'

# Call the function to create the video
#create_video_from_images(image_folder_path, output_video_file)
url_to_scan = "https://sports.walla.co.il/item/3776973"

image_folder_path = r'D:\downloaded5'
# Run the function
find_and_download_jpgs(url_to_scan)
# Run the function
images_to_video(image_folder_path, output_video_file, 10)

