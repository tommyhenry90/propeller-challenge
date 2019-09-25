import unittest
from image_splitter import ImageSplitter
import numpy as np
import cv2 as cv
import math


def create_image(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)
    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


class TestImageSplitter(unittest.TestCase):
    def setUp(self):
        directory = "test_images"
        filename = "test_image.jpg"
        self.splitter = ImageSplitter(filename, directory)

    def test_load_non_existent_image(self):
        directory = "pretend"
        filename = "pretentfile.jpg"
        self.assertFalse(self.splitter.load_image(filename, directory))

    def test_downsize_image(self):
        factor = 2
        downsized_image = self.splitter.downsize_image(self.splitter.img, factor)
        original_dimensions = self.splitter.img.shape
        downsized_dimensions = downsized_image.shape
        self.assertEqual(original_dimensions[0] // factor, downsized_dimensions[0])
        self.assertEqual(original_dimensions[1] // factor, downsized_dimensions[1])
        self.assertEqual(original_dimensions[2], downsized_dimensions[2])

    # TODO make this test more robust for different image sizes
    def test_tiles_create_original_image(self):
        tile_size = 1
        num_y, num_x, _channels = map(int, self.splitter.img.shape)
        num_x = math.ceil(num_x / tile_size)
        num_y = math.ceil(num_y / tile_size)
        self.splitter.tile_image(tile_size, num_levels=1)
        recombined_tiles = self.splitter.recombine_tiles(0, num_x, num_y)
        # Check images have same dimensions and channels
        self.assertEqual(recombined_tiles.shape, self.splitter.img.shape)

        # Check images are exactly the same
        difference = cv.subtract(recombined_tiles, self.splitter.img)
        b, g, r = cv.split(difference)
        self.assertEqual(cv.countNonZero(b), 0)
        self.assertEqual(cv.countNonZero(g), 0)
        self.assertEqual(cv.countNonZero(r), 0)


if __name__ == '__main__':
    unittest.main()
