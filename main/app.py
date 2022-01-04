import tkinter as tk
from tkinter.constants import CENTER, W
from PIL import Image, EpsImagePlugin
import cv2
import numpy as np
from tensorflow.keras.models import load_model

EpsImagePlugin.gs_windows_binary = r'D:/gs/gs9.55.0/bin/gswin64c'


class App:
    # Init function/Constructor
    def __init__(self, window=tk.Tk(), window_title='Handwritten Digit Recognizer'):
        self.window = window
        self.window_title = window_title
        self.window_width = 700
        self.window_height = 400
        self.delay = 4000

    # Function for initializing the GUI
    def init_gui(self):
        # Setting window properties
        self.window.title(self.window_title)
        self.window.geometry("{}x{}".format(
            self.window_width, self.window_height))
        self.window.eval('tk::PlaceWindow . center')
        self.window.config(bg='white')
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        # Adding Canvas for drawing the digit
        self.canvas = tk.Canvas(self.window, width=350,
                                height=400, borderwidth=2)
        self.canvas.grid(row=0, column=0, columnspan=1, sticky=W, rowspan=21)
        self.canvas.create_rectangle(0, 0, 358, 408, fill='black')
        self.canvas.bind('<B1-Motion>', self.paint)

        # Adding Label for displaying the message
        self.l1 = tk.Label(self.window, width=12, bg='white',
                           text="Predicted Digit", font=('Arial', 15), justify=CENTER)
        self.l1.grid(row=5, column=1, columnspan=1, padx=81.5)

        # Adding Label for displaying the predicted number
        self.l2 = tk.Label(self.window, width=12, bg='white',
                           text="N.A.", font=('Arial', 25), justify=CENTER)
        self.l2.grid(row=7, column=1, rowspan=3, columnspan=1, padx=81.5)

    # Function for drawing on canvas
    def paint(self, event):
        color = 'white'
        x1, y1 = (event.x-1), (event.y-1)
        x2, y2 = (event.x+1), (event.y+1)
        self.canvas.create_oval(
            x1-5, y1+5, x2+5, y2-5, fill=color, outline=color, tags='ovals')

    # Save canvas as image
    def save_img(self):
        # Save postscript image
        self.canvas.postscript(file='img/canvas.ps', colormode='color')

        # Use PIL to convert to PNG
        img = Image.open('img/canvas.ps')
        img.save('img/digit.png', 'png')

    # Process image to be fed to the model
    def process_img(self, path):
        # Read image from path
        drawing = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        self.window.update()

        # Resize image to 28x28
        drawing = cv2.resize(drawing, (28, 28), interpolation=cv2.INTER_AREA)

        # Add grayscale channel
        drawing = drawing.reshape((1, 28, 28, 1))

        # Scale data to range of [0, 1]
        drawing = drawing.astype('float32')
        drawing /= 255.0
        return drawing

    # Update GUI
    def update_gui(self):
        # Save canvas drawing as image
        self.save_img()

        # Process image
        drawingArray = self.process_img(path='img/digit.png')

        # Feed to saved model
        dmodel = load_model('model/digit_recognition.h5')
        pred_digit = np.argmax(dmodel.predict(drawingArray), axis=1)

        # Display result
        self.l2.config(text=pred_digit[0])

        # Clear canvas
        self.canvas.delete('ovals')

        # Schedule next check
        self.window.after(self.delay, self.update_gui)


def main():
    # Create object
    digit_app = App()
    digit_app.init_gui()

    # Call after for first update
    digit_app.window.after(digit_app.delay, digit_app.update_gui)

    # Call tkinter mainloop
    digit_app.window.resizable(False, False)
    digit_app.window.mainloop()


main()
