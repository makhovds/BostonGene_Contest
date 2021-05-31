import glob
import os
import cv2

def load_images_from_folder(abs_path_parent_folder, subfolder_names, file_extension):
    imgs = [[] for i in subfolder_names] if len(subfolder_names) > 1 else []
    imgs_names = [[] for i in subfolder_names] if len(subfolder_names) > 1 else []
    for idx, subfolder_name in enumerate(subfolder_names):          
        full_path = os.path.join(abs_path_parent_folder, subfolder_name)    
        for file_path in glob.glob(os.path.join(full_path, file_extension)):            
            
            if len(subfolder_names) > 1:
                imgs_names[idx].append(os.path.basename(file_path))
                imgs[idx].append(cv2.imread(file_path, cv2.IMREAD_GRAYSCALE))
            else:
                imgs_names.append(os.path.basename(file_path))
                imgs.append(cv2.imread(file_path, cv2.IMREAD_GRAYSCALE))
    return imgs_names, imgs