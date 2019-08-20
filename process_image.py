import sys
import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2
from PIL import Image
from .colors import ColorLoader
from scipy.spatial import KDTree

def nearest_analysis(old_img, colors):
    kd = KDTree(colors)
    dists, ndx = kd.query(old_img.flatten().reshape(img_shape[0] * img_shape[1], 3))    
    unique, counts = np.unique(ndx, return_counts=True)
    sorted_count_ndx = np.argsort(-counts)
    sorted_unique = unique[sorted_count_ndx]
    sorted_counts = counts[sorted_count_ndx]

    return ndx, dists,sorted_unique, sorted_counts

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    
    if height is None:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("img", type=cv2.imread,
                        help="image file to be processed")
    parser.add_argument("n_colors", type=int,
                        help="number of colors to be processed")
    args = parser.parse_args()

    img_data = image_resize(args.img, width=256)
    img_shape = img_data.shape
    colors = ColorLoader().to_np_array()
    _, _, unique, counts = nearest_analysis(img_data, colors)
    
    fig, axs = plt.subplots(1, 1)
    axs.bar(unique, counts)
    plt.show()
    n_colors = colors[unique[:args.n_colors]]
    
    ndx, dists, _, _ = nearest_analysis(img_data, n_colors)
    
    new_img = n_colors[ndx].flatten().reshape(img_shape)
    print(new_img)
    print(new_img.astype(np.uint8))

    
    cv2.imshow('new',new_img.astype(np.uint8))
    cv2.imshow('old_rescaled', img_data.astype(np.uint8))
    cv2.waitKey(0)
