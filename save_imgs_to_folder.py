import cv2
import glob
import os

def make_dir(dir_abs_path):
    try:
        os.mkdir(dir_abs_path)
    except OSError as error:
        pass  
    
def save_imgs_to_folder(imgs, imgs_names, abs_path):
    make_dir(abs_path)
    for img, img_name in zip(imgs, imgs_names):
        cv2.imwrite(os.path.join(abs_path, img_name), img)
    