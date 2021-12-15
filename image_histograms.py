#!/usr/bin/env python3
import cv2
from matplotlib import pyplot as plt 
import PIL
import os
import glob

year_start = 1978
year_end = 2021

month_start = 1
month_end = 12

DATA_DIR = 'images'

year_res_list = {}

for year in tqdm(range(year_start, year_end+1)):
    images = glob.glob(f'{DATA_DIR}/{year}/*/*.gif')
    resolutions = []
    for img in images:
        im = cv2.imread(img)
