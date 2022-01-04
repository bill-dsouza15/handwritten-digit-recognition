# Handwritten Digit Recognition

This is a handwritten digit recognition application using keras and tkinter. 
<br>
___

## Idea
1. The user draws the number on the canvas space.
2. The canvas is "auto-captured" every 4s and is converted to postscript and then to an image using Pillow.
3. This number is then identified using the saved image and the serialized model that is then displayed on the screen.

___

## Setup
1. A requirements.txt file for installing the required libraries has been provided. The libraries can be installed by
    ```
    pip install -r requirements.txt
    ```
    Creating a virtual environement is recommended.

2. Ghostscript is needed to save the canvas as postscript. Ghostscript can be installed from [here](https://ghostscript.com/releases/gsdnld.html). Additionally, the path to gswin64c in the bin folder of the installation is to be added in app.py (line 8)

___

## Output
A demo testing some digits is shown below
<br>

![Demo](https://github.com/bill-dsouza15/handwritten-digit-recognition/blob/main/demo.gif)


