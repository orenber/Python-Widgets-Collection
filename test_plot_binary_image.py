from unittest import TestCase
from matplotlib import pyplot as plt
import numpy as np
from draw_binary_image import plot_binary_image, create_line


class TestPlotBinaryImage(TestCase):
    def test_plot_binary_image(self):
        # create figure
        plt.figure(1)
        ax = plt.axes()
        ax.cla()

        # create blank image
        blank_image = np.zeros([100, 100], dtype=np.bool)
        ax.imshow(blank_image, cmap=plt.cm.gray)

        # get array input
        x = np.array(range(1, 1000, 1))
        y = 20 * np.sin(x/4) + 50
        ax.set_xlim((0, 100))
        ax.set_ylim((0, 100))
        ax.plot(x, y, 'r')

        mask = plot_binary_image(blank_image, x, y)
        ax.imshow(mask, cmap=plt.cm.gray)

        plt.show()

    def test_create_line(self):
        fu = create_line( 1, 3, 5, 6 )
        fu(3)
        print(fu)
