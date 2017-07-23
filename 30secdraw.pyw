# -*- coding: utf-8 -*-
# 30秒ドローイング資料めくりツール
# ファイル形式：画像、動画
# 準備
# 1. python:3.6.0をインストール
# 2. "folders.dat"というファイル（Encoding:UTF-8）を実行ファイルと同じ場所に置いて資料フォルダのパスを列挙する
#   /*を含む行から*/を含む行までコメントアウト可能

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Tk, Canvas
import re
import math
import random
import media
import os

class MainWindow():

  width = 140
  height = 100
  change_ms = 300

  #----------------

  def __init__(self, main):

    # canvas for image
    self.canvas = Canvas(main, width=self.width, height=self.height)
    self.canvas.grid(row=0, column=0)

    # set first image on canvas
    self.photo_image = self.createPhotoImage()
    self.image_on_canvas = self.canvas.create_image(0, 0, anchor = tk.NW, image = self.photo_image)

    # set timer
    self.canvas.after( self.change_ms, self.onTimer )

    # set event
    self.canvas.bind("<Button-1>", self.onTimer )

  #----------------

  def onTimer(self):

    # change image
    self.photo_image = self.createPhotoImage()
    self.canvas.itemconfig(self.image_on_canvas, image = self.photo_image)

    # set timer
    self.canvas.after( self.change_ms, self.onTimer )

  #----------------

  def createPhotoImage( self ):

    # read image
    canvas = Canvas( root, width=self.width, height=self.height )
    pil_img = Image.open( self.nextFile() )
    pil_img.thumbnail((self.width,self.height), Image.ANTIALIAS)
    pil_canvas = Image.new( 'RGB', (self.width,self.height), (255,255,255) )

    # fit into window
    top = 0
    left = 0
    if pil_img.size[0] / pil_img.size[1] > self.width / self.height:
      left = 0
      top = math.floor( ( self.height - pil_img.size[1] ) / 2 )
    else:
      left = math.floor( ( self.width - pil_img.size[0] ) / 2 )
      top = 0
    pil_canvas.paste( pil_img, (left,top) )

    return ImageTk.PhotoImage(pil_canvas)

  #----------------

  def nextFile( self ):

    while 1:
      # read folder list
      a_file = open('folders.dat', encoding='utf-8')
      folders = []
      comment_flg = False
      for a_line in a_file:
        if a_line.find( '/*' ) >= 0 :
          comment_flg = True
          continue
        elif a_line.find( '*/' ) >= 0 :
          comment_flg = False
          continue
        elif comment_flg :
          continue
        else :
          folders.append( re.sub( r'\n', '', a_line ) )

      # select random folder
      idx = math.floor(len(folders)*random.random())
      folder = folders[idx]
      print( 'LS: ' + folder )
      if os.path.isdir( folder ) == False:
        continue

      # select random file
      files = os.listdir( folder )
      for i in range(len(files)):
        files[i] = folder + "\\" + files[i]
      idx = math.floor(len(files)*random.random())
      file = files[idx]

      # check extension
      if media.isImg( file ) or media.isVideo( file ):
        break

    print(file)
    out_file = file
    if media.isVideo(file):
      out_file = 'out.png'
      media.randomCapture( file, out_file )

    return out_file

#----------------------------------------------------------------------

root = Tk()
MainWindow(root)
root.mainloop()
