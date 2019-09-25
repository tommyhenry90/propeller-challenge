import unittest
from image_splitter import ImageSplitter
import numpy as np
import cv2 as cv


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
        self.assertEqual(original_dimensions[0] / factor, downsized_dimensions[0])
        self.assertEqual(original_dimensions[1] / factor, downsized_dimensions[1])
        self.assertEqual(original_dimensions[2], downsized_dimensions[2])

    def test_tiles_create_original_image(self):
        self.splitter.tile_image(1, 1)
        recombined_tiles = self.splitter.recombine_tiles(0, 4, 4)
        # Check images have same dimensions and channels
        self.assertEqual(recombined_tiles.shape, self.splitter.img.shape)
        difference = cv.subtract(recombined_tiles, self.splitter.img)
        b, g, r = cv.split(difference)
        self.assertEqual(cv.countNonZero(b), 0)
        self.assertEqual(cv.countNonZero(g), 0)
        self.assertEqual(cv.countNonZero(r), 0)


if __name__ == '__main__':
    unittest.main()
