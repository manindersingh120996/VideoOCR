import cv2
import numpy as np
import os
import pytesseract
import re
image_frames = 'image_frames/'
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\10710548\D Drive\Tesseract-OCR\tesseract.exe'
from PIL import Image
import time

class VideoOcr():
    """
    This class contains the code to break the input video
    into the frames, then combine the similliar frames into 
    1 single frame thus reducing redudnancy of frames and 
    commands extracted.
    Then it goes through each frame after preprocessing and extract
    the command prompt commands entered in the video.

    NOTE : currently this project is limitted to extracting command prompt commands
            soon plan is to extract text from softwares like entered in excel, MS-SQL woekbench,
            and other softeares.

    INPUT : it takes video_path : path of video
    template_path : path of command prompt template to match images with
    image_storage: temporary storage to save extracted frames
    combined_frame_storage : to store the combined frames

    
    """
    def __init__(self,video_path,template_path,image_storage,combined_frame_storage):
        self.video_path = video_path
        self.template_path = template_path
        self.image_frames = image_storage
        self.combined_frame_dir = combined_frame_storage
        

    def video_break(self):
        # Uploaded video path
        video_file = self.video_path
        cap = cv2.VideoCapture(video_file)
        if not cap.isOpened():
            print("Error: Could not open video file.")
            exit()
        
        # Get the frame rate (frames per second)  
        frame_rate = cap.get(cv2.CAP_PROP_FPS)  
        frame_interval = int(frame_rate)
        
        
        # Load the template image (screenshot of command prompt or PowerShell)
        template = cv2.imread(self.template_path)
        template = cv2.resize(template, (1920, 1080))  # Replace 'width' and 'height' with the desired size
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite('todelete.jpg',template)
        
        # Initiate ORB detector
        orb = cv2.ORB_create()
        
        # Find the keypoints and descriptors with ORB
        kp1, des1 = orb.detectAndCompute(template, None)
        frame_count = 0
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                if frame_count % frame_interval == 0:
                    # Convert the frame to grayscale
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # Find the keypoints and descriptors with ORB in the frame
                    kp2, des2 = orb.detectAndCompute(gray_frame, None)
                    # BFMatcher (Brute Force Matcher) with default params
                    bf = cv2.BFMatcher()
                    matches = bf.knnMatch(des1, des2, k=2)
                    # Apply ratio test
                    good_matches = []
                    for m, n in matches:
                        if m.distance < 0.75 * n.distance:
                            good_matches.append(m)
                    # If enough good matches are found, consider the frame as a match
                    if len(good_matches) > 10:     
                        frame_filename = self.image_frames +str(int(frame_count / frame_rate)) +'.png'
                        cv2.imwrite(frame_filename, frame)
                #         cv2.waitKey(0)  # Press any key to see the next frame
                frame_count += 1
        except Exception as e:
            print(f"Facing error {e} in Breaking Video Into Frames")
        
        # Release the video capture object and close the window
        cap.release()
        cv2.destroyAllWindows()
        
    def are_frames_similar(self,frame1, frame2, threshold=0.50):
        # Implement your similarity comparison logic here
        # we might want to use techniques like structural similarity index (SSI) or others
        # For simplicity, let's assume frames are similar if absolute pixel-wise difference is below a threshold
        diff_percentage, _ = self.calculate_difference_percentage(frame1, frame2)
    
        print(f"Difference Percentage : {diff_percentage}<{threshold}:{diff_percentage<threshold}")
        return diff_percentage < threshold
    
    def calculate_difference_percentage(self,frame1, frame2):
        diff = cv2.absdiff(frame1, frame2)
        res = diff.astype(np.uint8)
        diff_percentage = (np.count_nonzero(res) * 100) / res.size
        return diff_percentage,diff

    def merge_similar_frames(self,frame_list):
        combined_frames = []
        index = 0
        # combined_frame_dir = './combined_frames/'
        
    
        while index < len(frame_list) - 1:
            print(index)
            current_frame = cv2.imread(frame_list[index])
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            current_frame_bw = cv2.threshold(current_frame, 80, 255, cv2.THRESH_BINARY)[1]
    
            next_frame = cv2.imread(frame_list[index + 1])
            next_frame = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
            next_frame_bw = cv2.threshold(next_frame, 80, 255, cv2.THRESH_BINARY)[1]
            print(frame_list[index],frame_list[index + 1])
            
            try:
            
                if not self.are_frames_similar(current_frame_bw, next_frame_bw):
                    cv2.imwrite(f'{self.combined_frame_dir}/combined_{index}.png',current_frame_bw)
                    index += 1
                else:
                    current_frame_bw = next_frame_bw
                    index += 1
                    next_frame = cv2.imread(frame_list[index + 1])
                    next_frame = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
                    next_frame_bw = cv2.threshold(next_frame, 80, 255, cv2.THRESH_BINARY)[1]
            except IndexError:
                cv2.imwrite(f'{self.combined_frame_dir}/case2_{index}.png',current_frame_bw)
            
    def break_tesseract_output_into_lines(self,tesseract_output):
        lines = tesseract_output.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return cleaned_lines
    # combined_frame_dir = './combined_frames/'



        
