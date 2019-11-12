import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication
from draw_binary_image import plot_binary_image


class AxesEvent:

    def __init__(self, *args, **kwargs):

        self.ax = plt.axes(*args, **kwargs)
        self.figure = self.ax.get_figure()
        self.__in_axes = False
        self.callback = {'on_press': '',
                         'on_release': '',
                         'on_motion': '',
                         'on_scroll': '',
                         'enter_axes': '',
                         'leave_axes': ''}

    def connect(self):
        # connect to all the events we need
        self.cidpress = self.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.enter_axes = self.figure.canvas.mpl_connect(
            'axes_enter_event', self.enter_axes)
        self.leave_axes = self.figure.canvas.mpl_connect(
            'axes_leave_event', self.leave_axes)

    def mouse_motion(self, state: bool = False):
        if state:
            self.cidrelease = self.figure.canvas.mpl_connect(
                'button_release_event', self.on_release)
            self.cidmotion = self.figure.canvas.mpl_connect(
                'motion_notify_event', self.on_motion)
            self.scroll = self.figure.canvas.mpl_connect(
                'scroll_event', self.on_scroll)
        elif state == False:
            self.figure.canvas.mpl_disconnect(self.cidrelease)
            self.figure.canvas.mpl_disconnect(self.cidmotion)
            self.figure.canvas.mpl_disconnect(self.scroll)

    def on_press(self, event):
        # on button press we will see if the mouse is over us and store some data
        if self.__in_axes and id(self.ax) == id(event.inaxes):
            self.mouse_motion(True)

            callback = self.callback['on_press']
            if callable(callback):
                callback(event)

            pass

    def on_scroll(self, event):

        callback = self.callback['on_scroll']
        if callable(callback):
            callback(event)

    def on_motion(self, event):

        if self.__in_axes and id(self.ax) == id(event.inaxes):

            callback = self.callback['on_motion']
            if callable(callback):
                callback(event)

        pass

    def on_release(self, event):
        self.__in_axes = True
        if id(self.ax) == id(event.inaxes):

            self.mouse_motion(False)

            callback = self.callback['on_release']
            if callable(callback):
                callback(event)
        pass

    def enter_axes(self, event):

        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
        self.__in_axes = True
        if id(self.ax) == id(event.inaxes):

            callback = self.callback['enter_axes']
            if callable(callback):
                callback(event)

        pass

    def leave_axes(self, event):
        QApplication.restoreOverrideCursor()
        self.__in_axes = False
        if id(self.ax) == id(event.inaxes):

            callback = self.callback['leave_axes']
            if callable(callback):
                callback(event)

        pass

    def disconnect(self):
        self.figure.canvas.mpl_disconnect(self.cidpress)
        self.figure.canvas.mpl_disconnect(self.cidrelease)
        self.figure.canvas.mpl_disconnect(self.cidmotion)


class BoardFreeHand:

    def __init__(self, *args, **kwargs):

        self.ax = plt.axes(*args, **kwargs)
        self.figure = self.ax.get_figure()
        self.press = None
        self.penColor = 'blue'
        self.background = None
        self.__in_axes = False
        self._xdata = []
        self._ydata = []
        self.erse_color = self.ax.get_facecolor()
        self.erse_size = 1
        self.__erse_size = 1

        self.ax.set_xlim((0,1))
        self.ax.set_ylim((0,1))
        self.clear_axes()


    @property
    def draw(self) -> bool:
        return self.__draw

    @draw.setter
    def draw(self, state: bool):
        self.__draw = state

        if self.__draw:
            self.mouse_motion(True)
        else:
            self.mouse_motion(False)

    @property
    def erse_size(self) -> int:
        return self.__erse_size

    @erse_size.setter
    def erse_size(self, size: int):
        if size < 1:
            self.__erse_size = 1
        else:
            self.__erse_size = size

    def connect(self):
        # connect to all the events we need
        self.cidpress = self.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)

        self.enter_axes = self.figure.canvas.mpl_connect(
            'axes_enter_event', self.enter_axes)
        self.leave_axes = self.figure.canvas.mpl_connect(
            'axes_leave_event', self.leave_axes)

    def mouse_motion(self, state: bool = False):
        if state:
            self.cidrelease = self.figure.canvas.mpl_connect(
                'button_release_event', self.on_release)
            self.cidmotion = self.figure.canvas.mpl_connect(
                'motion_notify_event', self.on_motion)
            self.scroll = self.figure.canvas.mpl_connect(
                'scroll_event', self.on_scroll)
        elif state == False:
            self.figure.canvas.mpl_disconnect(self.cidrelease)
            self.figure.canvas.mpl_disconnect(self.cidmotion)
            self.figure.canvas.mpl_disconnect(self.scroll)

    def on_press(self, event):
        # on button press we will see if the mouse is over us and store some data
        if self.__in_axes and id(self.ax) == id(event.inaxes):
            self.draw = True
            if event.button == 3:
                self.clear_axes()


    def on_scroll(self, event):

        scroll_direction = event.button
        print('scroll dirction' + scroll_direction)
        if scroll_direction == 'down':
            self.erse_size -= 1
            pass

        elif scroll_direction == 'up':

            self.erse_size += 1
            pass

    def on_motion(self, event):

        if self.__in_axes:

            if event.button == 1:
                self.draw_on( event.xdata, event.ydata, self.penColor)
                pass
            elif event.button == 3:
                self.draw_on(event.xdata, event.ydata, self.erse_color, self.erse_size)
                pass

    def on_release(self, event):
        self.draw = False
        self._xdata = []
        self._ydata = []

    def draw_on(self, x0: float, y0: float, draw_color='black', size=1):


        # LIFO
        self._xdata.append(x0)
        self._ydata.append(y0)
        if len(self._xdata) > 2:
            self._xdata.pop(0)
            self._ydata.pop(0)
        self.ax.plot( self._xdata, self._ydata, color=draw_color, linewidth=size )

        self.figure.canvas.draw()

        pass

    def clear_axes(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.cla()
        self.ax.set_xlim( xlim )
        self.ax.set_ylim( ylim )
        self.figure.canvas.draw()



    def enter_axes(self, event):
        self.__in_axes = True
        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
        pass

    def leave_axes(self, event):
        self.__in_axes = False
        QApplication.restoreOverrideCursor()

    def disconnect(self):
        self.figure.canvas.mpl_disconnect(self.cidpress)
        self.figure.canvas.mpl_disconnect(self.cidrelease)
        self.figure.canvas.mpl_disconnect(self.cidmotion)
        if self.draw:
            self.mouse_motion(False)


class BoardImage(BoardFreeHand):

    def __init__(self,image_size = [45, 45], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_size = image_size
        self.image = self.create_binary_image()

    def create_binary_image(self):

        black_image = np.zeros([self.image_size[0], self.image_size[0]], dtype=np.bool)
        self.ax.cla()
        self.ax.imshow( black_image, cmap=plt.cm.gray)
        return black_image

    def draw_on(self, x0: int, y0: int, drawcolor='black', size=1):

        self._xdata.append(x0)
        self._ydata.append(y0)
        self.ax.plot( self._xdata, self._ydata, color=drawcolor, linewidth=size )

        self.figure.canvas.draw()

    def on_release(self, event):
        if event.button == 1:
            black_image = np.zeros( [self.image_size[0], self.image_size[0]], dtype=np.bool )
            blob_image = plot_binary_image(black_image,self._xdata,self._ydata)
            self.image = self.image + blob_image
            self.ax.imshow(self.image, cmap=plt.cm.gray)
            self.figure.canvas.draw()

        super().on_release(event)

    def on_press(self, event):
        # on button press we will see if the mouse is over us and store some data
        super().on_press(event)
        if event.button == 3:
            self.image = np.zeros([self.image_size[0], self.image_size[0]], dtype=np.bool )
            self.ax.imshow(self.image, cmap=plt.cm.gray)
            self.figure.canvas.draw()


def main():

    plt.figure()
    ax1 = BoardImage()
    ax1.connect()

    plt.show()


if __name__ == "__main__":
    main()