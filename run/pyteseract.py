from PIL import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'D:/user/Program/NKNU-Priority-Seat/run/Tesseract-OCR/tesseract.exe'

def dirname():
	return os.path.dirname(os.path.realpath(__file__))

dirname = dirname()

def captcha(path = dirname+ '/captcha.png'):
	img=Image.open(path)
	imggray=img.convert('L')
	threshold=170
	pixdata=imggray.load()
	width,height=imggray.size
	for y in range(height):
		for x in range(width):
			if pixdata[x,y]<threshold:
				pixdata[x,y]=0
			else:
				pixdata[x,y]=255
	imgbin=imggray
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
	return pytesseract.image_to_string(imgclear,config='-c tessedit_char_whitelist=0123456789 --psm 6')