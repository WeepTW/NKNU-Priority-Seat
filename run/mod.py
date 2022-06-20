from concurrent.futures import thread
import os
from PIL import Image
from cv2 import threshold
import pytesseract
import torch
from dataset import Synth90kDataset
from torch.utils.data import DataLoader
from model import CRNN
from tqdm import tqdm
from ctc_decoder import ctc_decode
from PIL import Image
from config import train_config as config

def captcha1(x=1):
	path = os.path.dirname(os.path.realpath(__file__)) + r'\captcha.png'
	pytesseract.pytesseract.tesseract_cmd = os.path.dirname(os.path.realpath(__file__)) + r'\Tesseract-OCR\tesseract.exe'
	img=Image.open(path)
	imggray=img.convert('L')
	if x ==1:
		threshold=170
	elif x ==2:
		threshold = 140
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

def captcha2():
    dirname = os.path.dirname(os.path.realpath(__file__))
    path = dirname + r'\captcha.png'
    def captcha(path):
        img=Image.open(path)
        imggray=img.convert('L')
        threshold=140
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
    #   imgclear.show()
        return imgclear

    def predict(crnn, dataloader, label2char, decode_method, beam_size):
        crnn.eval()
        pbar = tqdm(total=len(dataloader), desc="Predict")

        all_preds = []
        with torch.no_grad():
            for data in dataloader:
                device = 'cuda' if next(crnn.parameters()).is_cuda else 'cpu'
                
                images = data.to(device)

                logits = crnn(images)
                log_probs = torch.nn.functional.log_softmax(logits, dim=2)

                preds = ctc_decode(log_probs, method=decode_method, beam_size=beam_size,
                                label2char=label2char)
                all_preds += preds

                pbar.update(1)
            pbar.close()

        return all_preds

    def show_result(paths, preds):
        for path, pred in zip(paths, preds):
            text = ''.join(pred)

    images_dir = path

    nim=captcha(images_dir)
    nim.save(images_dir)


    reload_checkpoint = dirname + r'\crnn_050001_loss0.01712806542714437.pt'
    batch_size = 256
    decode_method = 'beam_search'
    beam_size = 10

    img_height = config['img_height']
    img_width = config['img_width']

    images = [images_dir]

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    predict_dataset = Synth90kDataset(paths=images, img_height=img_height, img_width=img_width)

    predict_loader = DataLoader(
        dataset=predict_dataset,
        batch_size=batch_size,
        shuffle=False)

    num_class = len(Synth90kDataset.LABEL2CHAR) + 1
    crnn = CRNN(1, img_height, img_width, num_class,
                map_to_seq_hidden=config['map_to_seq_hidden'],
                rnn_hidden=config['rnn_hidden'],
                leaky_relu=config['leaky_relu'])
    crnn.load_state_dict(torch.load(reload_checkpoint, map_location=device))
    crnn.to(device)

    s = ''
    for char in predict(crnn, predict_loader, Synth90kDataset.LABEL2CHAR,decode_method=decode_method,beam_size=beam_size)[0]:
        s += char
    return s
