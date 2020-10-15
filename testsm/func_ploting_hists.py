import matplotlib.pyplot as plt
import numpy as np
import os
from skimage.io import imread

def read_proc_plot(imgname):
    path_main = "D:\\Circa\\Dane do sieci segmentacji\\dataset_v2\\train_big\\1"
    path_enh = "D:\\Circa\\Dane do sieci segmentacji\\dataset_v2_enhanced\\train_big\\1"

    pth_img = os.path.join(path_main, imgname+".png")
    pth_img_enh = os.path.join(path_enh, imgname+".tiff")

    def minmax(img):
        return (img - np.min(img))/(np.max(img)-np.min(img))
    img = imread(pth_img)
    img = minmax(img)
    img_enh = imread(pth_img_enh)
    plt.figure(figsize=(12,3))
    plt.subplot(1,3,1)
    plt.imshow(img, cmap='gray')
    plt.subplot(1,3,2)
    plt.imshow(img_enh, cmap='gray')
    plt.subplot(1,3,3)
    plt.hist(img[img!=0], bins=50, label="original")
    plt.hist(img_enh[img_enh!=0], bins=50, alpha = 0.5, label="enhanced")
    plt.suptitle(imgname)