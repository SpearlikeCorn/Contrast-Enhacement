import os
from CE import CE, CE_e
import matplotlib.pyplot as plt
import sys
import numpy as np
from skimage import io, exposure, img_as_uint, img_as_float
import pandas as pd
import time

path = "D:\\Circa\\PolCovid_clean_07102020\\png_processed_without_duplicates"
path_to = "D:\\Circa\\PolCovid_clean_07102020\\png_processed_enhanced_without_duplicates"

df = pd.DataFrame()

pngCounter = 0
for dirpath, dirnames, filenames in os.walk(path):
    for filename in [f for f in filenames if f.endswith(".png")]:
        subset = dirpath.split("\\")[-2]
        if subset == "whole":
            continue
        pngCounter += 1

i = 0
# progress print
sys.stdout.write('\033[2K\033[1G')
progress = i/pngCounter*100
sys.stdout.write("\r{0:0.2f}%".format(progress))
for dirpath, dirnames, filenames in os.walk(path):
    for filename in [f for f in filenames if f.endswith(".png")]:
        # path image READ ONLY
        path_image_read = os.path.join(dirpath, filename)
        # get subset and diagnosis
        diagnosis = dirpath.split("\\")[-1]
        subset = dirpath.split("\\")[-2]
        if subset == "whole":
            continue

        # prepare path for saving
        path_to_subset_diagnosis = os.path.join(path_to, diagnosis)
        bold_filename = filename.split(".")[0]
        path_image_save = os.path.join(path_to_subset_diagnosis, bold_filename+".tiff")

        # READ the image
        img = plt.imread(path_image_read)

        # process the data
        print("===CE===")
        start = time.time()
        img_enhanced = CE(img, stop_condition=20)
        df.loc[bold_filename, "time CE"] = time.time() - start
        print("time CE =", time.time() - start)
        print("===CE_E===")
        start = time.time()
        img_enhanced = CE_e(img, stop_condition=20)
        df.loc[bold_filename, "time CE_e"] = time.time() - start
        print("time CE_e =", time.time() - start)
        # SAVE the data
        img_enhanced = img_as_float(img_enhanced)
        #io.imsave(path_image_save, img_enhanced)

        '''# progress print
        sys.stdout.write('\033[2K\033[1G')
        progress = i / pngCounter * 100
        sys.stdout.write('\r{0:0.2f}% | saved to path: '.format(progress) + path_image_save)'''
        i += 1
        if i > 20:
            break