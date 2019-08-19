import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


class BoardFreeHand:

    def __init__(self, parent = plt.figure(),**attr):
        self.figure = parent
        self.ax = self.figure.add_subplot(111)
        self.press = None
        self.penColor = 'blue'
        self.background = None
        self.__in_axes = False
        self._xdata = []
        self._ydata = []
        self.erse_color = self.ax.get_facecolor()
        self.erse_size = 1
        self.__erse_size = 1
        



    @property
    def draw(self)->bool:
        return self.__draw

    @draw.setter
    def draw(self, state: bool):
        self.__draw = state

        if self.__draw :
            self.mouse_motion(True)
        else:
            self.mouse_motion(False)


    @property
    def erse_size(self)->int:
        return self.__erse_size

    @erse_size.setter
    def erse_size(self,size:int):
        if size<1:
            self.__erse_size =1
        else:
            self.__erse_size = size




    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)

        self.enter_axes = self.figure.canvas.mpl_connect(
            'axes_enter_event', self.enter_axes)
        self.leave_axes = self.figure.canvas.mpl_connect(
            'axes_leave_event', self.leave_axes)

    def mouse_motion(self,state:bool=False):
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
        'on button press we will see if the mouse is over us and store some data'
        if self.__in_axes:
            self.draw= True
    
    def on_scroll(self, event):
        
        scroll_direction = event.button 
        print('scroll dirction'+scroll_direction)
        if scroll_direction == 'down':
            self.erse_size  -=1
            pass
      
        elif scroll_direction == 'up':
             
            self.erse_size  +=1
            pass
    def on_motion(self, event):
        
        if self.__in_axes == True: 
           if event.button == 1:
                self.draw_on( event.xdata , event.ydata,self.penColor)
                pass
           elif event.button == 3:
               self.draw_on( event.xdata , event.ydata, self.erse_color, self.erse_size)
               pass

    def draw_on(self, x0:float , y0:float, drawcolor='black',size = 1):
        self._xdata.append(x0)
        self._ydata.append(y0)
        line = plt.plot(self._xdata, self._ydata,color = drawcolor,linewidth=size)
        self.figure.canvas.draw()
        pass
       

    def on_release(self, event):
        self.draw = False
        self._xdata = []
        self._ydata = []

    def enter_axes(self,event):
        self.__in_axes = True
        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
        pass
 
    def leave_axes(self,event):
        self.__in_axes = False
        QApplication.restoreOverrideCursor()

  
    def disconnect(self):
        self.figure.canvas.mpl_disconnect(self.cidpress)
        self.figure.canvas.mpl_disconnect(self.cidrelease)
        self.figure.canvas.mpl_disconnect(self.cidmotion)
        if self.draw:
            self.mouse_motion(False)



class BoaredImage(BoardFreeHand):
    def __init__(self, parent = plt.figure(),**attr):
        super().__init__( parent ,**attr)
        self.image_size = [45,45]
        self.image = self.create_binary_image()

    def create_binary_image(self):

        black_image = np.zeros([self.image_size[0], self.image_size[0]], dtype=np.bool)
        self.ax.imshow(black_image,cmap=plt.cm.gray)
        return black_image

    def draw_on(self, x0:int , y0:int, drawcolor='black',size = 1):

 
        self.image[int(y0), int(x0)] = True
        self.ax.cla
        self.ax.imshow(self.image,cmap=plt.cm.gray)
        self.figure.canvas.draw()
        










def main():
 
    ax = BoardFreeHand()
    ax.connect()
    plt.show()


if __name__ == "__main__":
    main()



