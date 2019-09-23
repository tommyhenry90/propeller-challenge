from PIL import Image
import cv2 as cv
import sys
import numpy as np


def crop_image(img, x, y):
    cropped_image = img[x:x+256, y:y+256]
    return cropped_image


def load_image(filename):
    src = cv.imread(filename)
    return src


def save_image(img, level, x, y):
    name = "images/" + str(level) + "_" + str(x) + "_" + str(y) + ".jpg"
    cv.imwrite(name, img)


def downsize_image(img):
    rows, cols, _channels = map(int, img.shape)
    return cv.pyrDown(img, dstsize=(cols // 2, rows // 2))


def tile_image(img):
    rows, cols, _channels = map(int, img.shape)
    for x in range(cols // 256 + 1):
        for y in range(rows // 256 + 1):
            temp_img = img[y*256:y*256+256, x*256:x*256+256]
            for level in range(9):
                save_image(temp_img, level, x, y)
                temp_img = downsize_image(temp_img)
    return None


def main(argv):
    filename = argv[0] if len(argv) > 0 else 'images/Cat 1.jpg'
    original_image = load_image(filename)
    tile_image(original_image)

if __name__ == '__main__':
    main(sys.argv[1:])
