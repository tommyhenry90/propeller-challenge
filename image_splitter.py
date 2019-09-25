import cv2 as cv
import sys
import os
import math


class ImageSplitter:
    def __init__(self, filename, directory, tile_size=256, num_levels=9):
        self.filename = filename
        self.directory = directory
        self.sub_directory = "image_pyramid"
        self.tile_size = tile_size
        self.num_levels = num_levels
        self.img = None
        self.load_image(self.filename, self.directory)
        self.tiles = []

    def load_image(self, filename, directory):
        self.img = cv.imread(directory + "/" + filename)
        return self.img

    def save_image(self, img, level, x, y):
        sub_sub_directory = self.directory + "/" + self.sub_directory + "/" + str(level)
        if not os.path.exists(sub_sub_directory):
            os.makedirs(sub_sub_directory)
        name = str(x) + "_" + str(y) + ".jpg"
        cv.imwrite(sub_sub_directory + "/" + name, img)
        return True

    def downsize_image(self, img, factor=2):
        rows, cols, _channels = map(int, img.shape)
        return cv.pyrDown(img, dstsize=(cols // factor, rows // factor))

    # TODO downsize original images first before tiling to avoid pixelation on higher levels
    def tile_image(self, tile_size=256, num_levels=9):
        if not os.path.exists(self.directory + "/" + self.sub_directory):
            os.makedirs(self.directory + "/" + self.sub_directory)
        rows, cols, _channels = map(int, self.img.shape)
        num_cols = math.ceil(cols/tile_size)
        num_rows = math.ceil(rows / tile_size)
        for x in range(num_cols):
            for y in range(num_rows):
                temp_img = self.img[y*tile_size: y*tile_size + tile_size, x*tile_size: x*tile_size + tile_size]
                for level in range(num_levels):
                    self.save_image(temp_img, level, x, y)
                    temp_img = self.downsize_image(temp_img)
        return True

    def recombine_tiles(self, level, num_x, num_y):
        sub_sub_directory = self.directory + "/" + self.sub_directory + "/" + str(level)
        previous_rows = []
        for x in range(num_x):
            next_row = []
            for y in range(num_y):
                next_image = cv.imread(sub_sub_directory + "/" + str(x) + "_" + str(y) + ".jpg")
                next_row.append(next_image)
            previous_rows.append(cv.vconcat(next_row))
        recombined_tiles = cv.hconcat(previous_rows)
        return recombined_tiles


def main(argv):
    if len(argv) > 0:
        path_name = argv[0]
    else:
        print("invalid input")
        return False
    directory = os.path.dirname(path_name)
    filename = os.path.basename(path_name)
    splitter = ImageSplitter(filename, directory)
    splitter.tile_image()


if __name__ == '__main__':
    main(sys.argv[1:])
