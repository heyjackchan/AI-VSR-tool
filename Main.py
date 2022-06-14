#!/usr/bin/env python
# coding: utf-8

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

def f_goto_page1():
    #changepage()
    page1(root)

def f_goto_page2():
    #changepage()
    page2(root)

def f_goto_page3():
    #changepage()
    page3(root)

def f_goto_page4():
    #changepage()
    page4(root)

def f_goto_page5():
    #changepage()
    page5(root)

def f_goto_page6():
    #changepage()
    page6(root)

def changepage():
    global pagenum, root
    for widget in root.winfo_children():
        widget.destroy()

def func_select_file():
    filetypes = (
        ('MP4 files', '*.mp4'),
    )

    filename = fd.askopenfilename(
        title='Open a video file',
        initialdir='/',
        filetypes=filetypes)
    
    basicVidData = func_getVideoStat(filename)
    if (basicVidData[1] > basicVidData[2]):
        longerSide = basicVidData[1]
        shorterSide = basicVidData[2]
    else:
        longerSide = basicVidData[2]
        shorterSide = basicVidData[1]
    if (longerSide == 'NO DATA' or shorterSide == 'NO DATA'):
        ctypes.windll.user32.MessageBoxW(0, "You haven't select a video file or it is a unsupported video format. Please reselect another video file.", "Invalid video file", 1)
    elif (int(shorterSide)>1079 or int(longerSide)>1919):
        ctypes.windll.user32.MessageBoxW(0, "The selected video resolution is higher than the system allows. Please reselect a lower resolution video.", "Video resolution is too large!", 1)
    else:
        f = open("temp_selected_file.txt", "w")
        f.write(filename)
        f.close()
        f_goto_page2()
    
def func_getVideoStat(videoFilepath):
    cmd='ffprobe -v quiet -print_format json -show_format -show_streams "' + videoFilepath + '"'
    result=subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE).stdout
    list_std=result.readlines()
    str_tmp=''
    for item in list_std:
        str_tmp+=bytes.decode(item.strip())
    json_data=json.loads(str_tmp)
    if 'format' in json_data:
        if 'filename' in json_data['format']:
            vid_filename = json_data['format']['filename']
        else:
            vid_filename = 'NO DATA'
        
        if 'duration' in json_data['format']:
            vid_dura_time = json_data['format']['duration']
        else:
            vid_dura_time = 'NO DATA'
    else:
        vid_filename = 'NO DATA'
        vid_dura_time = 'NO DATA'

    if 'streams' in json_data:
        if 'height' in json_data['streams'][0]:
            vid_height = json_data['streams'][0]['height']
        else:
            vid_height = 'NO DATA'
            
        if 'width' in json_data['streams'][0]:
            vid_width = json_data['streams'][0]['width']
        else:
            vid_width = 'NO DATA'
            
        if 'codec_long_name' in json_data['streams'][0]:
            vid_codec = json_data['streams'][0]['codec_long_name']
        else:
            vid_codec = 'NO DATA'
            
        if 'r_frame_rate' in json_data['streams'][0]:
            vid_fps = json_data['streams'][0]['r_frame_rate']
        else:
            vid_fps = 'NO DATA'
            
        if 'field_order' in json_data['streams'][0] and json_data['streams'][0]['field_order'] == "progressive":
            vid_field_order = 'p';
        elif 'field_order' in json_data['streams'][0] and json_data['streams'][0]['field_order'] == "interlaced":
            vid_field_order = 'i';
        elif 'field_order' in json_data['streams'][0]:
            vid_field_order = json_data['streams'][0]['field_order']
        else:
            vid_field_order = 'NO DATA'
    else:
        vid_height = 'NO DATA'
        vid_width = 'NO DATA'
        vid_codec = 'NO DATA'
        vid_fps = 'NO DATA'
        vid_field_order = 'NO DATA'
    return vid_filename, vid_height, vid_width, vid_codec, vid_fps, vid_dura_time, vid_field_order

def func_displayResolution(input1,input2,frameFieldOrder):
    if input1 > input2:
        return str(input1) + ' x ' + str(input2) + 'p'
    else:
        return str(input2) + ' x ' + str(input1) + 'p'


def func_returnToHomepage():
    if os.path.exists("temp_selected_file.txt"):
        os.remove("temp_selected_file.txt")
    f_goto_page1()

def func_modeSelector(x,y):
    if x>y:
        longerSide = x;
        shorterSide = y;
    else:
        longerSide = y;
        shorterSide = x;
    modeCounterW = 0;
    if longerSide < 853:
        modeCounterW = 3;
    elif longerSide < 1280:
        modeCounterW = 2;
    else:
        modeCounterW = 1;
    
    modeCounterH = 0;
    if shorterSide < 480:
        modeCounterH = 3;
    elif shorterSide < 720:
        modeCounterH = 2;
    else:
        modeCounterH = 1;
        
    modeDisplayer = 0;
    if modeCounterW > modeCounterH:
        modeDisplayer = modeCounterH
    elif modeCounterW < modeCounterH:
        modeDisplayer = modeCounterW
    else:
        modeDisplayer = modeCounterW
    
    return modeDisplayer

def func_newD2value(originalD1, newD1, originalD2):
    newD2 = int(newD1 * originalD2 / originalD1)
    return newD2
                
def page1(root):
    root.wm_iconbitmap('logo.ico')
    root.title('Video Super-Resolution Tool')
    root.geometry('1600x900')
    root.resizable(width=0, height=0)

    img = Image.open("Background.jpg")                    
    imgTk =  ImageTk.PhotoImage(img)                        
    p1_line0_bgimg = tk.Label(root, image=imgTk)                   
    p1_line0_bgimg.image = imgTk
    p1_line0_bgimg.grid(column=0, row=0)

    p1_line1_title = tk.Label(root, text="Video Super-Resolution Tool", bg='white', fg='#46A0E2', font=('Arial Bold', 32))
    p1_line1_title.place(x=250, y=205)

    p1_line2_text = tk.Label(root, text="Improve your video quality with several simple clicks.", bg='white', fg='#46A0E2', font=('Arial Italic', 16))
    p1_line2_text.place(x=250, y=275)

    p1_line3_text = tk.Label(root, text="Version 1.0", bg='white', fg='#46A0E2', font=('Arial Bold', 16))
    p1_line3_text.place(x=250, y=315)

    p1_line4_button = tk.Button(root, text="Select a video file", bg='#45A0E1', fg='white', font=('Arial', 16), command=func_select_file)
    p1_line4_button['width'] = 30
    p1_line4_button['height'] = 2
    p1_line4_button['activebackground'] = '#1C87D6'        
    p1_line4_button['activeforeground'] = 'black'     
    p1_line4_button.place(x=250, y=425)

    p1_line5a_text = tk.Label(root, text="About developing team", bg='white', fg='#46A0E2', font=('Arial', 16))
    p1_line5a_text.place(x=250, y=600)

    p1_line5b_text = tk.Label(root, text="Credits", fg='#46A0E2', bg='white', font=('Arial', 16))
    p1_line5b_text.place(x=500, y=600)

    p1_line5c_text = tk.Label(root, text="FAQ", fg='#46A0E2', bg='white', font=('Arial', 16))
    p1_line5c_text.place(x=600, y=600)

    p1_line5d_text = tk.Label(root, text="Check for updates", bg='white', fg='#46A0E2', font=('Arial', 16))
    p1_line5d_text.place(x=680, y=600)

def page2(root):
    img = Image.open("Background2.jpg")                    
    imgTk =  ImageTk.PhotoImage(img)                        
    p2_line0_bgimg = tk.Label(root, image=imgTk)                   
    p2_line0_bgimg.image = imgTk
    p2_line0_bgimg.grid(column=0, row=0)

    p2_line1a_top_title = tk.Label(root, text="STEP      /4  SELECT VIDEO", bg='white', fg='#46A0E2', font=('Arial Bold Italic', 32))
    p2_line1a_top_title.place(x=50, y=50)
    p2_line1b_top_stepnum = tk.Label(root, text="1", bg='white', fg='#46A0E2', font=('Arial Bold Italic', 56))
    p2_line1b_top_stepnum.place(x=185, y=21)
    
    p2_line2_text = tk.Label(root, text="You have selected the following video:", bg='white', fg='#1B4699', font=('Arial', 16))
    p2_line2_text.place(x=50, y=140)

    f = open("temp_selected_file.txt")
    videoFilePath = f.read()
    f.close()
    
    cmd='ffmpeg -i "' + videoFilePath + '" -ss 00:00:03 -t 00:00:01 vsrpreview1.mp4'
    result=subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE).stdout
    
    #videoBaseRectangle
    p2_line3aa_baseRect = tk.Canvas (root, width=782, height=440)
    p2_line3aa_baseRect.create_rectangle(0,0,783,441,fill='#000000')
    p2_line3aa_baseRect.place(x=50, y=190)

    videoData = func_getVideoStat(videoFilePath)
    originalHeight = videoData[1]
    originalWidth = videoData[2]
    originalFPS = eval(videoData[4])
    frameDefHeight = 440
    frameDefWidth = 782
    frameDefLocationX = 50
    frameDefLocationY = 190
    frameHeightRatio = frameDefHeight / originalHeight
    frameWidthRatio = frameDefWidth / originalWidth
    
    #Default play video frame size: 782, 440
    #Default play location: x=50, y=190
    if frameHeightRatio > frameWidthRatio:
        displayWidth = frameDefWidth
        displayHeight = frameWidthRatio * originalHeight
        displayLocationX = frameDefLocationX
        displayLocationY = frameDefLocationY + (frameDefHeight - displayHeight)/2
    else:
        displayWidth = frameHeightRatio * originalWidth
        displayHeight = frameDefHeight
        displayLocationX = frameDefLocationX + (frameDefWidth - displayWidth)/2
        displayLocationY = frameDefLocationY
    
    # create label
    p2_line3a_videoPlayer = tk.Label(root)
    p2_line3a_videoPlayer.place(x=int(displayLocationX), y=int(displayLocationY))
    # read video to display on label
    player = tkvideo(videoFilePath, p2_line3a_videoPlayer,
                     loop = 1, size = (int(displayWidth), int(displayHeight)),fps=originalFPS)
    
    player.play()

    p2_line3b_text = tk.Label(root, text="Video filepath:", bg='white', fg='#1B4699', font=('Arial', 16))
    p2_line3b_text.place(x=880, y=190)
    p2_line3b_ans = tk.Label(root, text=videoData[0], bg='white', fg='#000000', font=('Arial', 16))
    p2_line3b_ans.place(x=880, y=220)


    p2_line3c_text = tk.Label(root, text="Video frame resolution:", bg='white', fg='#1B4699', font=('Arial', 16))
    p2_line3c_text.place(x=880, y=280)
    
    p2_line3c_ans = tk.Label(root, text=func_displayResolution(videoData[1],videoData[2],str(videoData[6])), bg='white', fg='#000000', font=('Arial', 16))
    p2_line3c_ans.place(x=880, y=310)

    p2_line3d_text = tk.Label(root, text="Video coding method:", bg='white', fg='#1B4699', font=('Arial', 16))
    p2_line3d_text.place(x=880, y=370)
    p2_line3d_ans = tk.Label(root, text=videoData[3], bg='white', fg='#000000', font=('Arial', 16))
    p2_line3d_ans.place(x=880, y=400)

    p2_line3e_text = tk.Label(root, text="Video FPS:", bg='white', fg='#1B4699', font=('Arial', 16))
    p2_line3e_text.place(x=880, y=460)
    p2_line3e_ans = tk.Label(root, text=round(eval(videoData[4]), 3), bg='white', fg='#000000', font=('Arial', 16))
    p2_line3e_ans.place(x=880, y=490)

    p2_line3f_text = tk.Label(root, text="Video length:", bg='white', fg='#1B4699', font=('Arial', 16))
    p2_line3f_text.place(x=880, y=550)
    p2_line3f_ans = tk.Label(root, text=str(datetime.timedelta(seconds=float(videoData[5]))), bg='white', fg='#000000', font=('Arial', 16))
    p2_line3f_ans.place(x=880, y=580)

    p2_line81_text = tk.Label(root, text="Are the information listed above correct?", bg='white', fg='#1B4699', font=('Arial', 16))
    p2_line81_text.place(x=50, y=775)

    p2_line82a_button = tk.Button(root, text="YES, I would like to use this video to proceed.", bg='#45A0E1', fg='white', font=('Arial', 16), command=f_goto_page3)
    p2_line82a_button['height'] = 1
    p2_line82a_button['activebackground'] = '#1C87D6'        
    p2_line82a_button['activeforeground'] = 'black'     
    p2_line82a_button.place(x=50, y=805)

    p2_line82b_button = tk.Button(root, text="NO, I would like to go back to homepage.", bg='#45A0E1', fg='white', font=('Arial', 16), command=func_returnToHomepage)
    p2_line82b_button['height'] = 1
    p2_line82b_button['activebackground'] = '#1C87D6'        
    p2_line82b_button['activeforeground'] = 'black'     
    p2_line82b_button.place(x=520, y=805)

def page3(root):
    def f_p3_newResSelect1():
        f1 = open("temp_newHeight.txt", "w")
        f1.write(str(newResOne_H))
        f1.close()
        f2 = open("temp_newWidth.txt", "w")
        f2.write(str(newResOne_W))
        f2.close()
        f_goto_page4()
    def f_p3_newResSelect2():
        f1 = open("temp_newHeight.txt", "w")
        f1.write(str(newResTwo_H))
        f1.close()
        f2 = open("temp_newWidth.txt", "w")
        f2.write(str(newResTwo_W))
        f2.close()
        f_goto_page4()
    def f_p3_newResSelect3():
        f1 = open("temp_newHeight.txt", "w")
        f1.write(str(newResThree_H))
        f1.close()
        f2 = open("temp_newWidth.txt", "w")
        f2.write(str(newResThree_W))
        f2.close()
        f_goto_page4()
        
    f = open("temp_selected_file.txt")
    filename = f.read()
    f.close()
    basicVidData = func_getVideoStat(filename)
    vidHeight = basicVidData[1]
    vidWidth = basicVidData[2]
    vidFrameFieldOrder = basicVidData[6]
    vidWidthHeightRatio = vidWidth / vidHeight
    modeSelect = func_modeSelector(vidWidth,vidHeight)
    if vidWidthHeightRatio > 1:
        #newResOne_H = 480
        #newResTwo_H = 720
        #newResThree_H = 1080
        #newResOne_W = func_newD2value(vidHeight, newResOne_H, vidWidth)
        #newResTwo_W = func_newD2value(vidHeight, newResTwo_H, vidWidth)
        #newResThree_W = func_newD2value(vidHeight, newResThree_H, vidWidth)
        newResOne_W = 853
        newResTwo_W = 1280
        newResThree_W = 1920
        newResOne_H = func_newD2value(vidWidth, newResOne_W, vidHeight)
        newResTwo_H = func_newD2value(vidWidth, newResTwo_W, vidHeight)
        newResThree_H = func_newD2value(vidWidth, newResThree_W, vidHeight)
        if (newResOne_H>480 or newResTwo_H>720 or newResThree_H>1080):
            newResOne_H = 480
            newResTwo_H = 720
            newResThree_H = 1080
            newResOne_W = func_newD2value(vidHeight, newResOne_H, vidWidth)
            newResTwo_W = func_newD2value(vidHeight, newResTwo_H, vidWidth)
            newResThree_W = func_newD2value(vidHeight, newResThree_H, vidWidth)
    else:
        newResOne_W = 480
        newResTwo_W = 720
        newResThree_W = 1080
        newResOne_H = func_newD2value(vidWidth, newResOne_W, vidHeight)
        newResTwo_H = func_newD2value(vidWidth, newResTwo_W, vidHeight)
        newResThree_H = func_newD2value(vidWidth, newResThree_W, vidHeight)
        if (newResOne_H>853 or newResTwo_H>1280 or newResThree_H>1920):
            newResOne_H = 853
            newResTwo_H = 1280
            newResThree_H = 1920
            newResOne_W = func_newD2value(vidHeight, newResOne_H, vidWidth)
            newResTwo_W = func_newD2value(vidHeight, newResTwo_H, vidWidth)
            newResThree_W = func_newD2value(vidHeight, newResThree_H, vidWidth)
    
    if modeSelect == 1:
        img = Image.open("p3_img_mode1.jpg")                    
        imgTk =  ImageTk.PhotoImage(img)                        
        p3_line0_bgimg = tk.Label(root, image=imgTk)                   
        p3_line0_bgimg.image = imgTk
        p3_line0_bgimg.grid(column=0, row=0)
        p3_line3c_text = tk.Label(root, text=func_displayResolution(newResThree_W, newResThree_H, vidFrameFieldOrder), bg='white', fg='#46A0E2', font=('Arial Bold', 19))
        if (newResThree_W > 999 or newResThree_H > 999):
            p3_line3c_text.place(x=722, y=628)
        else:
            p3_line3c_text.place(x=728, y=628)
        p3_line82b_button = tk.Button(root, text='Select', bg='#45A0E1', fg='white', font=('Arial', 16), command=f_p3_newResSelect2)
        p3_line82b_button['height'] = 1
        p3_line82b_button['activebackground'] = '#1C87D6'        
        p3_line82b_button['activeforeground'] = 'black'     
        p3_line82b_button.place(x=764, y=750)
    elif modeSelect == 2:
        img = Image.open("p3_img_mode2.jpg")                    
        imgTk =  ImageTk.PhotoImage(img)                        
        p3_line0_bgimg = tk.Label(root, image=imgTk)                   
        p3_line0_bgimg.image = imgTk
        p3_line0_bgimg.grid(column=0, row=0)
        p3_line3b_text = tk.Label(root, text=func_displayResolution(newResTwo_W, newResTwo_H, vidFrameFieldOrder), bg='white', fg='#46A0E2', font=('Arial Bold', 19))
        if (newResTwo_W > 999 or newResTwo_H > 999):
            p3_line3b_text.place(x=512, y=628)
        else:
            p3_line3b_text.place(x=518, y=628)
        p3_line3c_text = tk.Label(root, text=func_displayResolution(newResThree_W, newResThree_H, vidFrameFieldOrder), bg='white', fg='#46A0E2', font=('Arial Bold', 19))
        if (newResThree_W > 999 or newResThree_H > 999):
            p3_line3c_text.place(x=937, y=628)
        else:
            p3_line3c_text.place(x=943, y=628)
        p3_line82b_button = tk.Button(root, text='Select', bg='#45A0E1', fg='white', font=('Arial', 16), command=f_p3_newResSelect2)
        p3_line82b_button['height'] = 1
        p3_line82b_button['activebackground'] = '#1C87D6'        
        p3_line82b_button['activeforeground'] = 'black'     
        p3_line82b_button.place(x=544, y=750)

        p3_line82c_button = tk.Button(root, text='Select', bg='#45A0E1', fg='white', font=('Arial', 16), command=f_p3_newResSelect3)
        p3_line82c_button['height'] = 1
        p3_line82c_button['activebackground'] = '#1C87D6'        
        p3_line82c_button['activeforeground'] = 'black'     
        p3_line82c_button.place(x=979, y=750)
    else:
        img = Image.open("p3_img_mode3.jpg")                    
        imgTk =  ImageTk.PhotoImage(img)                        
        p3_line0_bgimg = tk.Label(root, image=imgTk)                   
        p3_line0_bgimg.image = imgTk
        p3_line0_bgimg.grid(column=0, row=0)
        p3_line3a_text = tk.Label(root, text=func_displayResolution(newResOne_W, newResOne_H, vidFrameFieldOrder), bg='white', fg='#46A0E2', font=('Arial Bold', 19))
        p3_line3a_text.place(x=300, y=628)
        p3_line3b_text = tk.Label(root, text=func_displayResolution(newResTwo_W, newResTwo_H, vidFrameFieldOrder), bg='white', fg='#46A0E2', font=('Arial Bold', 19))
        if (newResTwo_W > 999 or newResTwo_H > 999):
            p3_line3b_text.place(x=722, y=628)
        else:
            p3_line3b_text.place(x=728, y=628)
        p3_line3c_text = tk.Label(root, text=func_displayResolution(newResThree_W, newResThree_H, vidFrameFieldOrder), bg='white', fg='#46A0E2', font=('Arial Bold', 19))
        if (newResThree_W > 999 or newResThree_H > 999):
            p3_line3c_text.place(x=1157, y=628)
        else:
            p3_line3c_text.place(x=1163, y=628)
        
        p3_line82a_button = tk.Button(root, text='Select', bg='#45A0E1', fg='white', font=('Arial', 16), command=f_p3_newResSelect1)
        p3_line82a_button['height'] = 1
        p3_line82a_button['activebackground'] = '#1C87D6'        
        p3_line82a_button['activeforeground'] = 'black'     
        p3_line82a_button.place(x=325, y=750)

        p3_line82b_button = tk.Button(root, text='Select', bg='#45A0E1', fg='white', font=('Arial', 16), command=f_p3_newResSelect2)
        p3_line82b_button['height'] = 1
        p3_line82b_button['activebackground'] = '#1C87D6'        
        p3_line82b_button['activeforeground'] = 'black'     
        p3_line82b_button.place(x=764, y=750)

        p3_line82c_button = tk.Button(root, text='Select', bg='#45A0E1', fg='white', font=('Arial', 16), command=f_p3_newResSelect3)
        p3_line82c_button['height'] = 1
        p3_line82c_button['activebackground'] = '#1C87D6'        
        p3_line82c_button['activeforeground'] = 'black'     
        p3_line82c_button.place(x=1199, y=750)

    #Test data:
    #print(func_modeSelector(50,300))
    #print(func_modeSelector(800,300))
    #print(func_modeSelector(1200,300))
    #print(func_modeSelector(800,600))
    #print(func_modeSelector(1200,600))
    #print(func_modeSelector(1800,600))
    #print(func_modeSelector(1900,900))

    p3_line1a_top_title = tk.Label(root, text="STEP      /4  SELECT OUTPUT RESOLUTION", bg='white', fg='#46A0E2', font=('Arial Bold Italic', 32))
    p3_line1a_top_title.place(x=50, y=50)
    p3_line1b_top_stepnum = tk.Label(root, text="2", bg='white', fg='#46A0E2', font=('Arial Bold Italic', 56))
    p3_line1b_top_stepnum.place(x=185, y=21)

    p3_line2_text = tk.Label(root, text="Below shows a schematic diagram for your reference to select the output video resolution:", bg='white', fg='#1B4699', font=('Arial', 16))
    p3_line2_text.place(x=50, y=140)

newDpZoomLv = 0 #control zoom in range, every time zoom in this amount of pixels.
newDpGoUpDown = 0 #control go uo down range, every time zoom in this amount of pixels.
# Positive number means to scroll up, negative number means to scroll down.
newDpGoLeftRight = 0
# Positive number means to scroll left, negative number means to scroll right.

def page4(root):
    def changeDisplay_goUp():
        global newDpGoUpDown
        if newDpGoUpDown>=0.25:
            ctypes.windll.user32.MessageBoxW(0, "You cannot go too up!", "Warning", 1)
        else:
            newDpGoUpDown = round(newDpGoUpDown + 0.05,2)
            f_goto_page4()
    def changeDisplay_goDown():
        global newDpGoUpDown
        if newDpGoUpDown<=-0.25:
            ctypes.windll.user32.MessageBoxW(0, "You cannot go too down!", "Warning", 1)
        else:
            newDpGoUpDown = round(newDpGoUpDown - 0.05,2)
            f_goto_page4()
    def changeDisplay_goLeft():
        global newDpGoLeftRight
        if newDpGoLeftRight>0.25:
            ctypes.windll.user32.MessageBoxW(0, "You cannot go too left!", "Warning", 1)
        else:
            newDpGoLeftRight = round(newDpGoLeftRight + 0.05,2)
            f_goto_page4()
    def changeDisplay_goRight():
        global newDpGoLeftRight
        if newDpGoLeftRight<=-0.25:
            ctypes.windll.user32.MessageBoxW(0, "You cannot go too right!", "Warning", 1)
        else:
            newDpGoLeftRight = round(newDpGoLeftRight - 0.05,2)
            f_goto_page4()
    def changeDisplay_zoomIn():
        global newDpZoomLv
        global newDpGoUpDown
        global newDpGoLeftRight
        if newDpZoomLv>=0.35:
            ctypes.windll.user32.MessageBoxW(0, "You cannot zoom in anymore!", "Warning", 1)
        else:
            newDpZoomLv = round(newDpZoomLv + 0.05,2)
            newDpGoUpDown = 0
            newDpGoLeftRight = 0
            f_goto_page4()
    def changeDisplay_zoomOut():
        global newDpZoomLv
        global newDpGoUpDown
        global newDpGoLeftRight
        if newDpZoomLv<=0:
            ctypes.windll.user32.MessageBoxW(0, "You cannot zoom out anymore!", "Warning", 1)
        else:
            newDpZoomLv = round(newDpZoomLv - 0.05,2)
            newDpGoUpDown = 0
            newDpGoLeftRight = 0
            f_goto_page4()

    def select_method1():
        f1 = open("temp_VSRmethod.txt", "w")
        f1.write(str("1"))
        f1.close()
        f_goto_page5()
    def select_method2():
        f2 = open("temp_VSRmethod.txt", "w")
        f2.write(str("2"))
        f2.close()
        f_goto_page5()
    def select_method3():
        f3 = open("temp_VSRmethod.txt", "w")
        f3.write(str("3"))
        f3.close()
        f_goto_page5()
    def select_method4():
        f4 = open("temp_VSRmethod.txt", "w")
        f4.write(str("4"))
        f4.close()
        f_goto_page5()
    def select_method5():
        f5 = open("temp_VSRmethod.txt", "w")
        f5.write(str("5"))
        f5.close()
        f_goto_page5()
    def select_method6():
        f6 = open("temp_VSRmethod.txt", "w")
        f6.write(str("6"))
        f6.close()
        f_goto_page5()

    def f_p4_videoCropper(video,originalHeight, originalWidth, cutHeight, cutWidth, displayWidth, displayHeight, playlabel, root):
        frame_counter = 0
        fps = eval("25")
        while video.isOpened():
            ret, frame = video.read()
            frame_counter += 1
            if frame_counter == int(video.get(cv2.CAP_PROP_FRAME_COUNT)):
                frame_counter = 0
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            if ret == True:
                vidvidHeightPt = 0 + cutHeight
                vidvidHeightAmount = originalHeight - cutHeight
                vidvidWidthPt = 0 + cutWidth
                vidvidWidthAmount = originalWidth - cutWidth
                
                if newDpGoUpDown != 0 and newDpGoUpDown >0: #Go up
                    vidvidHeightPt = vidvidHeightPt - int(originalHeight * newDpGoUpDown)
                    vidvidHeightAmount = vidvidHeightAmount - int(originalHeight * newDpGoUpDown)
                else: #Go down
                    vidvidHeightPt = vidvidHeightPt + int(originalHeight * (-newDpGoUpDown))
                    vidvidHeightAmount = vidvidHeightAmount + int(originalHeight * (-newDpGoUpDown))
                
                if newDpGoLeftRight != 0 and newDpGoLeftRight >0: #Go up
                    vidvidWidthPt = vidvidWidthPt - int(originalWidth * newDpGoLeftRight)
                    vidvidWidthAmount = vidvidWidthAmount - int(originalWidth * newDpGoLeftRight)
                else: #Go down
                    vidvidWidthPt = vidvidWidthPt + int(originalWidth * (-newDpGoLeftRight))
                    vidvidWidthAmount = vidvidWidthAmount + int(originalWidth * (-newDpGoLeftRight))
                
                imgarr = frame[vidvidHeightPt:vidvidHeightAmount,vidvidWidthPt:vidvidWidthAmount]
                img2 = cv2.cvtColor(imgarr, cv2.COLOR_BGR2RGBA)
                #img3 = cv2.imread(img2)
                current_image = PIL.Image.fromarray(img2).resize((displayWidth,displayHeight))
                imgtk2 = ImageTk.PhotoImage(current_image)
                #ImageTk.PhotoImage(image=)
                playlabel.imgtk = imgtk2
                playlabel.config(image=imgtk2)
                playlabel.update()
                #print("Run to f_p4")
                cv2.waitKey(fps)
                
    root.wm_iconbitmap('logo.ico')
    root.title('Video Super-Resolution Tool')
    root.geometry('1600x900')
    root.resizable(width=0, height=0)

    img = Image.open("Background3.jpg")                    
    imgTk =  ImageTk.PhotoImage(img)                        
    p4_line0_bgimg = tk.Label(root, image=imgTk)                   
    p4_line0_bgimg.image = imgTk
    p4_line0_bgimg.grid(column=0, row=0)

    p4_line1a_top_title = tk.Label(root, text="STEP      /4  SELECT VSR METHOD", bg='white', fg='#46A0E2', font=('Arial Bold Italic', 32))
    p4_line1a_top_title.place(x=50, y=50)
    p4_line1b_top_stepnum = tk.Label(root, text="3", bg='white', fg='#46A0E2', font=('Arial Bold Italic', 56))
    p4_line1b_top_stepnum.place(x=185, y=21)

    p4_line2_text = tk.Label(root, text="Below shows a list of previewed VSR effects, please select one to proceed:", bg='white', fg='#1B4699', font=('Arial', 16))
    p4_line2_text.place(x=50, y=140)

    p4_line82a_button = tk.Button(root, text="1", bg='#45A0E1', fg='white', font=('Arial', 16), command=select_method1)
    p4_line82a_button['height'] = 1
    p4_line82a_button['activebackground'] = '#1C87D6'        
    p4_line82a_button['activeforeground'] = 'black'     
    p4_line82a_button.place(x=770, y=130)

    p4_line82b_button = tk.Button(root, text="2", bg='#45A0E1', fg='white', font=('Arial', 16), command=select_method2)
    p4_line82b_button['height'] = 1
    p4_line82b_button['activebackground'] = '#1C87D6'        
    p4_line82b_button['activeforeground'] = 'black'     
    p4_line82b_button.place(x=820, y=130)

    p4_line82c_button = tk.Button(root, text="3", bg='#45A0E1', fg='white', font=('Arial', 16), command=select_method3)
    p4_line82c_button['height'] = 1
    p4_line82c_button['activebackground'] = '#1C87D6'        
    p4_line82c_button['activeforeground'] = 'black'     
    p4_line82c_button.place(x=870, y=130)

    p4_line82d_button = tk.Button(root, text="4", bg='#45A0E1', fg='white', font=('Arial', 16), command=select_method4)
    p4_line82d_button['height'] = 1
    p4_line82d_button['activebackground'] = '#1C87D6'        
    p4_line82d_button['activeforeground'] = 'black'     
    p4_line82d_button.place(x=920, y=130)

    p4_line82e_button = tk.Button(root, text="5", bg='#45A0E1', fg='white', font=('Arial', 16), command=select_method5)
    p4_line82e_button['height'] = 1
    p4_line82e_button['activebackground'] = '#1C87D6'        
    p4_line82e_button['activeforeground'] = 'black'     
    p4_line82e_button.place(x=970, y=130)

    p4_line82f_button = tk.Button(root, text="6", bg='#45A0E1', fg='white', font=('Arial', 16), command=select_method6)
    p4_line82f_button['height'] = 1
    p4_line82f_button['activebackground'] = '#1C87D6'        
    p4_line82f_button['activeforeground'] = 'black'     
    p4_line82f_button.place(x=1020, y=130)

    
    if newDpZoomLv==0.35:
        p4_line83a_button = tk.Button(root, text="▲", bg='#45A0E1', fg='white', font=('Arial', 16), command=changeDisplay_goUp)
        p4_line83a_button['height'] = 1
        p4_line83a_button['width'] = 2
        p4_line83a_button['activebackground'] = '#1C87D6'        
        p4_line83a_button['activeforeground'] = 'black'     
        p4_line83a_button.place(x=1220, y=130)

        p4_line83a_button = tk.Button(root, text="▼", bg='#45A0E1', fg='white', font=('Arial', 16), command=changeDisplay_goDown)
        p4_line83a_button['height'] = 1
        p4_line83a_button['width'] = 2
        p4_line83a_button['activebackground'] = '#1C87D6'        
        p4_line83a_button['activeforeground'] = 'black'     
        p4_line83a_button.place(x=1270, y=130)

        p4_line83a_button = tk.Button(root, text="◀", bg='#45A0E1', fg='white', font=('Arial', 16), command=changeDisplay_goLeft)
        p4_line83a_button['height'] = 1
        p4_line83a_button['width'] = 2
        p4_line83a_button['activebackground'] = '#1C87D6'        
        p4_line83a_button['activeforeground'] = 'black'     
        p4_line83a_button.place(x=1320, y=130)

        p4_line83a_button = tk.Button(root, text="▶", bg='#45A0E1', fg='white', font=('Arial', 16), command=changeDisplay_goRight)
        p4_line83a_button['height'] = 1
        p4_line83a_button['width'] = 2
        p4_line83a_button['activebackground'] = '#1C87D6'        
        p4_line83a_button['activeforeground'] = 'black'     
        p4_line83a_button.place(x=1370, y=130)

    p4_line83a_button = tk.Button(root, text="+", bg='#45A0E1', fg='white', font=('Arial', 16), command=changeDisplay_zoomIn)
    p4_line83a_button['height'] = 1
    p4_line83a_button['width'] = 2
    p4_line83a_button['activebackground'] = '#1C87D6'        
    p4_line83a_button['activeforeground'] = 'black'     
    p4_line83a_button.place(x=1420, y=130)

    p4_line83a_button = tk.Button(root, text="-", bg='#45A0E1', fg='white', font=('Arial', 16), command=changeDisplay_zoomOut)
    p4_line83a_button['height'] = 1
    p4_line83a_button['width'] = 2
    p4_line83a_button['activebackground'] = '#1C87D6'        
    p4_line83a_button['activeforeground'] = 'black'     
    p4_line83a_button.place(x=1470, y=130)
    
    frameDefHeight = 680
    frameDefWidth = 1500
    
    videoOne_videoData = func_getVideoStat("vsrpreview1.mp4")
    videoOne_originalHeight = videoOne_videoData[1]
    videoOne_originalWidth = videoOne_videoData[2]
    videoOne_originalFPS = eval(videoOne_videoData[4])

    videoOne_frameDefLocationX = 50
    videoOne_frameDefLocationY = 175
    videoOne_displayFrameRatio = frameDefWidth / frameDefHeight
    videoOne_videoRatio = videoOne_originalWidth / videoOne_originalHeight
    if videoOne_videoRatio>1:
        cutHeight = int(videoOne_originalHeight * newDpZoomLv)
        cutWidth = int(videoOne_originalWidth * newDpZoomLv)
    else:
        cutHeight = int(videoOne_originalHeight * newDpZoomLv)
        cutWidth = int(videoOne_originalWidth * newDpZoomLv)
    videoOne_frameHeightRatio = frameDefHeight / videoOne_originalHeight
    videoOne_frameWidthRatio = frameDefWidth / videoOne_originalWidth
    if videoOne_frameHeightRatio > videoOne_frameWidthRatio:
        videoOne_displayWidth = frameDefWidth
        videoOne_displayHeight = videoOne_frameWidthRatio * videoOne_originalHeight
        videoOne_displayLocationX = videoOne_frameDefLocationX
        videoOne_displayLocationY = videoOne_frameDefLocationY + (frameDefHeight - videoOne_displayHeight)/2
    else:
        videoOne_displayWidth = videoOne_frameHeightRatio * videoOne_originalWidth
        videoOne_displayHeight = frameDefHeight
        videoOne_displayLocationX = videoOne_frameDefLocationX + (frameDefWidth - videoOne_displayWidth)/2
        videoOne_displayLocationY = videoOne_frameDefLocationY

    videoOne_video = cv2.VideoCapture("vsrpreview1.mp4")
    p4_line3a_method1player = tk.Label(root)
    p4_line3a_method1player.place(x=int(videoOne_displayLocationX), y=int(videoOne_displayLocationY))
    f_p4_videoCropper(videoOne_video, videoOne_originalHeight, videoOne_originalWidth, cutHeight, cutWidth, int(videoOne_displayWidth), int(videoOne_displayHeight), p4_line3a_method1player, root)
    cv2.destroyAllWindows()

def page5(root):
    img = Image.open("Background2.jpg")                    
    imgTk =  ImageTk.PhotoImage(img)                        
    p5_line0_bgimg = tk.Label(root, image=imgTk)                   
    p5_line0_bgimg.image = imgTk
    p5_line0_bgimg.grid(column=0, row=0)
    
    f = open("temp_selected_file.txt")
    videoFilePath = f.read()
    f.close()
    videoData = func_getVideoStat(videoFilePath)
    
    f1 = open("temp_newHeight.txt")
    videonewHeight = f1.read()
    f1.close()
    
    f2 = open("temp_newWidth.txt")
    videonewWidth = f2.read()
    f2.close()
        
    f3 = open("temp_VSRmethod.txt")
    videoVSRmethod = f3.read()
    f3.close()
    p5_line1a_top_title = tk.Label(root, text="STEP      /4  FINAL CONFIRM", bg='white', fg='#46A0E2', font=('Arial Bold Italic', 32))
    p5_line1a_top_title.place(x=50, y=50)
    p5_line1b_top_stepnum = tk.Label(root, text="4", bg='white', fg='#46A0E2', font=('Arial Bold Italic', 56))
    p5_line1b_top_stepnum.place(x=185, y=21)
    
    p5_line2_text = tk.Label(root, text="Please check below information for your final confirm:", bg='white', fg='#1B4699', font=('Arial', 16))
    p5_line2_text.place(x=50, y=140)
    
    p5_line3b_text = tk.Label(root, text="Video filepath:", bg='white', fg='#1B4699', font=('Arial', 16))
    p5_line3b_text.place(x=280, y=190)
    p5_line3b_ans = tk.Label(root, text=videoData[0], bg='white', fg='#000000', font=('Arial', 16))
    p5_line3b_ans.place(x=280, y=220)


    p5_line3c_text = tk.Label(root, text="Original video frame resolution:", bg='white', fg='#1B4699', font=('Arial', 16))
    p5_line3c_text.place(x=280, y=280)
    
    p5_line3c_ans = tk.Label(root, text=func_displayResolution(videoData[1],videoData[2],str(videoData[6])), bg='white', fg='#000000', font=('Arial', 16))
    p5_line3c_ans.place(x=280, y=310)

    p5_line3d_text = tk.Label(root, text="New video frame resolution:", bg='white', fg='#1B4699', font=('Arial', 16))
    p5_line3d_text.place(x=280, y=370)
    p5_line3d_ans = tk.Label(root, text=func_displayResolution(int(videonewHeight),int(videonewWidth),str(videoData[6])), bg='white', fg='#000000', font=('Arial', 16))
    p5_line3d_ans.place(x=280, y=400)

    p5_line3e_text = tk.Label(root, text="VSR method:", bg='white', fg='#1B4699', font=('Arial', 16))
    p5_line3e_text.place(x=280, y=460)
    p5_line3e_ans = tk.Label(root, text=videoVSRmethod, bg='white', fg='#000000', font=('Arial', 16))
    p5_line3e_ans.place(x=280, y=490)

    p5_line3f_text = tk.Label(root, text="Video length:", bg='white', fg='#1B4699', font=('Arial', 16))
    p5_line3f_text.place(x=280, y=550)
    p5_line3f_ans = tk.Label(root, text=str(datetime.timedelta(seconds=float(videoData[5]))), bg='white', fg='#000000', font=('Arial', 16))
    p5_line3f_ans.place(x=280, y=580)

    p5_line81_text = tk.Label(root, text="Are the information listed above correct?", bg='white', fg='#1B4699', font=('Arial', 16))
    p5_line81_text.place(x=50, y=775)

    p5_line82a_button = tk.Button(root, text="YES, I confirm.", bg='#45A0E1', fg='white', font=('Arial', 16), command=f_goto_page6)
    p5_line82a_button['height'] = 1
    p5_line82a_button['activebackground'] = '#1C87D6'        
    p5_line82a_button['activeforeground'] = 'black'     
    p5_line82a_button.place(x=50, y=805)

    p5_line82b_button = tk.Button(root, text="NO, I would like to reselect resolution.", bg='#45A0E1', fg='white', font=('Arial', 16), command=f_goto_page3)
    p5_line82b_button['height'] = 1
    p5_line82b_button['activebackground'] = '#1C87D6'        
    p5_line82b_button['activeforeground'] = 'black'     
    p5_line82b_button.place(x=230, y=805)
    
    p5_line82c_button = tk.Button(root, text="NO, I would like to reselect VSR method.", bg='#45A0E1', fg='white', font=('Arial', 16), command=f_goto_page4)
    p5_line82c_button['height'] = 1
    p5_line82c_button['activebackground'] = '#1C87D6'        
    p5_line82c_button['activeforeground'] = 'black'     
    p5_line82c_button.place(x=620, y=805)

def page6(root):
    cwd = os.getcwd()
    f1 = open('temp_VSRmethod.txt', 'r')
    vsrmethod = int(f1.read())
    f1.close()
    f2 = open('temp_selected_file.txt', 'r')
    videoFilename = f2.readline()
    f2.close()
    f3 = open('temp_newHeight.txt', 'r')
    newHeight = f3.read()
    f3.close()
    f4 = open('temp_newWidth.txt', 'r')
    newWidth = f4.read()
    f4.close()
    
    videoData = func_getVideoStat(videoFilename)
    originalFPS = eval(videoData[4])
    newExtFilename = "_" + newHeight + "_" + newWidth + "."
    
    cwd = os.getcwd()
    vsr1Content1="ffmpeg -i \"" + videoFilename + "\" " + cwd +"\SRCNN\\data\\thumb%%06d.bmp -hide_banner"
    #\nmth1ImageSRandCombine.py>mth1_vsr1Content2.bat\nmth1_vsr1Content2.bat\n
    f98 = open('mth1_vsr1Content1.bat', 'w')
    f98.write(vsr1Content1)
    f98.close()
    os.startfile("mth1_vsr1Content1.bat")
    time.sleep(10)
    imgfilelist = os.listdir(os.getcwd()+"\SRCNN\\data")
    exp2 = "cd SRCNN\n"
    for ff in imgfilelist:
        if ".bmp" in ff:
            exp2 += "python test.py --weights-file \"BLAH_BLAH/srcnn_x3.pth\" --image-file data\\" + ff + " --scale 3 --new-width " + newWidth + " --new-height " + newHeight + "\n"
    exp2 += "cd data\nffmpeg -framerate " + str(int(originalFPS)) + " -i thumb%%06d.bmp " + videoFilename.replace(".", newExtFilename)
    f99 = open('mth1_vsr1Content2.bat', 'w')
    f99.write(exp2)
    f99.close()
    os.startfile("mth1_vsr1Content2.bat")
    
root = Tk()
page1(root)
root.mainloop()
