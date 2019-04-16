#!/usr/bin/env python3

'''
pip install tqdm numpy pillow mercantile 'rasterio==1.0b1' 'rio-tiler==1.0a7'
'''

import os

import argparse

from PIL import Image
import numpy as np

from tqdm import tqdm

import mercantile

from rio_tiler import main as tiler
from rio_tiler.utils import reshape_as_image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    parser.add_argument('out', type=str)
    parser.add_argument('--zoom', type=int, required=True)
    parser.add_argument('--ext', type=str, default='webp')
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    os.makedirs(os.path.join(args.out, str(args.zoom)), exist_ok=True)

    meta = tiler.bounds(args.path)
    bounds = meta['bounds']

    tiles = list(mercantile.tiles(*bounds + [[args.zoom]]))

    for x, y, z in tqdm(tiles, desc='Tiling', unit='tile', ascii=True):
        os.makedirs(os.path.join(args.out, str(z), str(x)), exist_ok=True)

        data, _ = tiler.tile(args.path, x, y, z)

        img = reshape_as_image(data)
        img = img[:,:,0]
        img = Image.fromarray(img, mode='L')
        img.save(os.path.join(args.out, str(z), str(x), str(y) + '.' + args.ext), optimize=True)


if __name__ == '__main__':
    main()
