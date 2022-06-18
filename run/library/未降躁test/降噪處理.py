from PIL import Image
from PIL import ImageEnhance
import os
import glob

def captcha(path):
	img=Image.open(path)
	#img to gray
	imggray=img.convert('L')
#	imggray.show()
	#img to binary
	threshold=100
	pixdata=imggray.load()
	width,height=imggray.size
	for y in range(height):
		for x in range(width):
			if pixdata[x,y]<threshold:
				pixdata[x,y]=0
			else:
				pixdata[x,y]=255
	imgbin=imggray
#	imgbin.show()
	#img clear
	pixdata=imgbin.load()
	width,height=imgbin.size
	for y in range(1,height-1):
		for x in range(1,width-1):
			count=0
			#up
			if pixdata[x,y-1]>245:
				count=count+1
			#down
			if pixdata[x,y+1]>245:
				count=count+1
			#left
			if pixdata[x-1,y]>245:
				count=count+1
			#right
			if pixdata[x+1,y]>245:
				count=count+1
			#up-left
			if pixdata[x-1,y-1]>245:
				count=count+1
			#down-left
			if pixdata[x-1,y+1]>245:
				count=count+1
			#up-right
			if pixdata[x+1,y-1]>245:
				count=count+1
			#down-right
			if pixdata[x+1,y+1]>245:
				count=count+1
			#clear
			if count>4:
				pixdata[x,y]=255
	imgclear=imgbin
#	imgclear.show()
	return imgclear

paths=glob.glob('*.png')
#print(paths)

for i in paths:
	im=Image.open(i)
	nim=captcha(i)
#	nim.show()
	nim.save(f'../test/{i}')