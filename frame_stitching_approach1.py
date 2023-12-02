"""
In this file, I have Independently pasted the working 
code of the algorithm for which has been pasted in README.md
file.

So that in future any one can access it independently if required
"""

import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

def merge_similar_frames(frame_list):
    combined_frame_dir = './combined_frames/'
    combined_frames = []
    index = 0
    

    while index < len(frame_list) - 1:
        print(index)
        current_frame = cv2.imread(frame_list[index])
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        current_frame_bw = cv2.threshold(current_frame, 80, 255, cv2.THRESH_BINARY)[1]

        next_frame = cv2.imread(frame_list[index + 1])
        next_frame = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
        next_frame_bw = cv2.threshold(next_frame, 80, 255, cv2.THRESH_BINARY)[1]
        print(frame_list[index],frame_list[index + 1])

        
        if not are_frames_similar(current_frame_bw, next_frame_bw):
            cv2.imwrite(f'{combined_frame_dir}/unmerged_frame_{index}.png',current_frame_bw)

            index += 1

        else:
            try:
                print("else:  ",frame_list[index],frame_list[index + 1])
                merged_frame = merge_frames(current_frame_bw, next_frame_bw)
                plt.figure(figsize=(20,20),dpi=400)
                plt.imshow(merged_frame)
                plt.show()
                temp_frame = next_frame_bw
                index += 1
                next_frame = cv2.imread(frame_list[index + 1])
                next_frame = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
                next_frame_bw = cv2.threshold(next_frame, 80, 255, cv2.THRESH_BINARY)[1]


                if index < len(frame_list) - 1 and are_frames_similar(temp_frame, next_frame_bw):
                    while index < len(frame_list) - 1 and are_frames_similar(temp_frame, next_frame_bw):
                        print("else-while")

                        merged_frame = merge_frames(merged_frame, next_frame_bw)
                        index += 1
                        temp_frame = next_frame_bw
                        next_frame = cv2.imread(frame_list[index + 1])
                        next_frame = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
                        next_frame_bw = cv2.threshold(next_frame, 80, 255, cv2.THRESH_BINARY)[1]
                        plt.figure(figsize=(20,20),dpi=400)
                        plt.imshow(merged_frame)
                        plt.show()
                        print(f"frame mergeing number elseif: {index}, {index+1}  ")

                cv2.imwrite(f'{combined_frame_dir}/combined_frame_elseif_saving{index}_{index+1}.png',merged_frame)
        
            except IndexError:
                cv2.imwrite(f'{combined_frame_dir}/combined_frame_elseif_saving{index}_{index+1}.png',merged_frame)
                               
            
            combined_frames.append(merged_frame)
            print('_-'*80)
    return combined_frames

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

def merge_frames(frame1, frame2):
    diff_per,diff = calculate_difference_percentage(frame1, frame2)
#     print(diff_per)
#     print(frame1.shape)
#     print(frame2.shape)

    _, thresholded = cv2.threshold(diff, 105, 255, cv2.THRESH_BINARY)
#         _,thresholded = cv2.threshold(diff,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(frame1)
    # Draw the contours on the mask
    cv2.drawContours(mask, contours, -1, (255, 255, 255))#,thickness=cv2.FILLED)
    # Combine the frames using the mask
    result_frame = cv2.addWeighted(frame1, 1, mask, 1.0, 0)
    return result_frame
# Example usage:
image_frames_dir = './image_frames/'  # Replace with the path to your image frames directory
frame_list = os.listdir(image_frames_dir)

frame_list.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
frame_list = [file for file in frame_list if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
frame_list = [image_frames_dir+file for file in frame_list]


combined_frames = merge_similar_frames(frame_list)

# Display or save the resulting frames as needed

# for i, frame in enumerate(combined_frames):
#     cv2.imwrite(f'{combined_frame_dir}/combined_frame_{i}.png', frame)
