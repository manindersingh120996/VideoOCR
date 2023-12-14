"""
In this file, I have Independently pasted the 2nd effective working 
code of the algorithm.

After Developing first algorithm, i realised that particular task can be
done fatter and effectively in following manner so i develop this particular algorithm.

It is faster,cleaner and smaller also.
As well as there is no need  for seperate temperory variable.
"""


import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

def merge_similar_frames(frame_list):
    combined_frames = []
    index = 0
    combined_frame_dir = './combined_frames/'
    

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
        
            if not are_frames_similar(current_frame_bw, next_frame_bw):
                cv2.imwrite(f'{combined_frame_dir}/case2_{index}.png',current_frame_bw)
                index += 1
            else:
                current_frame_bw = next_frame_bw
                index += 1
                next_frame = cv2.imread(frame_list[index + 1])
                next_frame = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
                next_frame_bw = cv2.threshold(next_frame, 80, 255, cv2.THRESH_BINARY)[1]
        except IndexError:
            cv2.imwrite(f'{combined_frame_dir}/case2_{index}.png',current_frame_bw)
            

            
def are_frames_similar(frame1, frame2, threshold=0.50):
    # Implement your similarity comparison logic here
    # You might want to use techniques like structural similarity index (SSI) or others
    # For simplicity, let's assume frames are similar if absolute pixel-wise difference is below a threshold
    diff_percentage, _ = calculate_difference_percentage(frame1, frame2)

    print(f"Difference Percentage : {diff_percentage}<{threshold}:{diff_percentage<threshold}")
    return diff_percentage < threshold

def calculate_difference_percentage(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)
    res = diff.astype(np.uint8)
    diff_percentage = (np.count_nonzero(res) * 100) / res.size
    return diff_percentage,diff

        
# Example usage:
image_frames_dir = './image_frames/'  # Replace with the path to your image frames directory
frame_list = os.listdir(image_frames_dir)

frame_list.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
frame_list = [file for file in frame_list if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
frame_list = [image_frames_dir+file for file in frame_list]
# print(frame_list)
# frame_list = sorted([os.path.join(image_frames_dir, frame) for frame in os.listdir(image_frames_dir)])
# print(frame_list)

# combined_frames = merge_similar_frames(frame_list)