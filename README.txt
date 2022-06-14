REMARK
======
Please download the full set of resources in order to run the system:
https://drive.google.com/drive/folders/1UQtKAnkDD0vNjn5f54IWrFB4tpmqb5iM?usp=sharing


NOTE
====
0. This program can be operated in Windows OS only. It is because it will call external Windows software (ffmpeg.exe, ffplay.exe, ffprobe.exe). These executable files cannot be recognized by other operating systems.
1. Install all required libraries (Listed below) before launching the system.
2. Open "CMD" in Windows.
3. Go to the system's folder by command "cd /d " <folderpath>
4. Drag the "Main.py" into the CMD.
5. Press enter, a GUI interface will be displayed.
6. Follow the steps displayed on the screen to implement Video SR.
7. The selected video should be longer than 5 seconds, otherwise, the preview video cannot be generated.
8. The rendered wideo will be produced in the same folder where input video is placed. The naming will be changed by adding new height and new width pixel values.
8. Sample demostrating video: https://youtu.be/-renfFlkR-c
9. Sample video attached are used for demostrating. They are retrieved from the Internet.


PYTHON LIBRARIES REQUIRED
=========================
import tkinter as tk
import subprocess,json
import datetime
import os
import ctypes
import cv2
import numpy as np
import PIL
import time
from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from tkvideo import tkvideo
from tkVideoPlayer import TkinterVideo


STUDENT INFORMATION
===================
Department of Computer Science, City University of Hong Kong
BSCCS Final Year Project Report (2021-2022)

FYP Code: 21CS152
Topic: A user-friendly tool for implementing AI Video Super-Resolution

Student ID: 55711777
Student Name: CHAN Tsz Yin
Programme Code: BSCEGU4

Supervisor: Dr. WANG Shiqi
1st Reader: Dr. LIAO, Jing
2nd Reader: Dr. LAU, Rynson W H


DOCUMENT STATUS
===============
Last update: 9th April, 2022 17:11
