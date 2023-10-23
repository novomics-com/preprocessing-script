#!/bin/env python

import os
import glob
import tifffile
import tqdm

from PIL import Image

import openslide as osd
import numpy as np

PATH_SVS_DIR = "/mnt/data/IMAGE/2023_01_NPOG확증임상/LEICA/03 등록 102/0.svs"
PATH_TIF_DIR = "/data01/workspace.moonsik/preprocessing-scripts/temp"

os.path.exists(PATH_SVS_DIR)
files = os.listdir(PATH_SVS_DIR)

def main():
    for svs_path in tqdm.tqdm(glob.glob(f"{PATH_SVS_DIR}/*.svs"), desc='Processing SVS files'):
        path_new_tif = os.path.join(PATH_TIF_DIR, os.path.basename(svs_path)[:-4])+".tif"
        slide = osd.OpenSlide(svs_path)
        images = [np.array(slide.read_region((0, 0), level, slide.level_dimensions[level])) for level in range(slide.level_count)]
        with tifffile.TiffWriter(path_new_tif, bigtiff=True) as tif:
            for img in images:
                tif.save(img[:, :, :3])

if __name__ == "__main__":
    main()