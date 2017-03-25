import subprocess
import random
import os
import stat

# capture random frame in video
# args:
#   video_in : input video file name
#   image_out : output image file name
def randomCapture( video_in, image_out ):
  str1 = subprocess.run( ['ffmpeg', '-stats', '-i', video_in], shell=True, encoding='utf-8', stderr=subprocess.PIPE, universal_newlines=True ).stderr
  lines = str1.split('\n')
  for line in lines:
    if( line[0:10] == '  Duration' ):
      h = float(line[12:14])
      m = float(line[15:17])
      s = float(line[18:20])
      tm = float(line[21:23])
      duration = h * 3600 + m * 60 + s + tm / 100
      start_time = duration * random.random()
      end_time = start_time + 1
      str2 = subprocess.run( ['ffmpeg', '-y', '-ss', str(start_time), '-t', str(end_time), '-r', '0.01', '-i', video_in, '-f', 'image2', image_out], shell=True, encoding='utf-8', stderr=subprocess.PIPE, universal_newlines=True ).stderr
      break

# true if file has one of extention in exts
def hasExt( file, exts ):
  for ext in exts:
    dotext = '.' + ext
    if file.lower().find(dotext) + len(dotext) == len(file):
      return True
  return False

# true if filepath is image
def isImg( filepath ):
 return os.stat( filepath ).st_mode != stat.S_ISDIR and \
   hasExt( filepath, ['bmp', 'dib', 'eps', 'gif', 'pcx', 'tif', 'tiff', 'jpg', 'jpe', 'jpeg', 'jp2', 'j2k', 'j2c', 'png', 'psd', 'pdd', 'pcd', 'fax', 'g3n', 'g3f', 'ico', 'pxm', 'ppm', 'pgm', 'tga', 'tagra', 'xbm', 'xpm', 'im', 'dcx' ] )

# true if filepath is video
def isVideo( filepath ):
 return os.stat( filepath ).st_mode != stat.S_ISDIR and \
   hasExt( filepath, ['3gp', '3g2', 'asf', 'avi', 'flv', 'mkv', 'mpg', 'mpeg', 'webm', 'mov', 'm1v', 'm2v', 'm2ts', 'ts', 'm4v', 'mp4', 'mjpeg', 'swf', 'vob', 'dvd', 'dvr-ms', 'wmv', 'rm', 'rmvb', 'ogv', 'ogm' ] )
