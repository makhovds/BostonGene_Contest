import numpy as np
from skimage.transform import resize

def make_imgs_one_size(func_imgs):
    assert isinstance(func_imgs, list), 'Необходимо передать список'
    row_nums = np.zeros((len(func_imgs),), dtype=np.uint16)
    col_nums = np.zeros((len(func_imgs),), dtype=np.uint16)
    for i, img in enumerate(func_imgs):
        row_nums[i], col_nums[i] = img.shape
    mean_row_num = np.floor(np.mean(row_nums))
    mean_col_num = np.floor(np.mean(col_nums))
    for i in range(len(func_imgs)):
        func_imgs[i] = np.uint8(resize(func_imgs[i], (mean_row_num, mean_col_num)) * 255) # resize преобразует в float, игнорирует preserve_range=True
    return func_imgs