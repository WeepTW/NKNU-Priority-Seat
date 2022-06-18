from config import train_config as config
import torch
from dataset import Synth90kDataset, synth90k_collate_fn
import glob
from torch.utils.data import DataLoader, random_split
from model import CRNN
from tqdm import tqdm
from ctc_decoder import ctc_decode

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
    print('\n===== result =====')
    for path, pred in zip(paths, preds):
        text = ''.join(pred)
        print(f'{path} > {text}')

images_dir = r'C:\Users\user\Desktop\空間借用驗證碼\驗證碼預測\test'
reload_checkpoint = 'crnn_050001_loss0.01712806542714437.pt'
batch_size = 256
decode_method = 'beam_search'
beam_size = 10

img_height = config['img_height']
img_width = config['img_width']
"""Usage: predict.py [-m MODEL] [-s BS] [-d DECODE] [-b BEAM] [IMAGE ...]
-h, --help    show this
-m MODEL     model file [default: ./checkpoints/crnn_synth90k.pt]
-s BS       batch size [default: 256]
-d DECODE    decode method (greedy, beam_search or prefix_beam_search) [default: beam_search]
-b BEAM   beam size [default: 10]
"""

images = glob.glob(f'{images_dir}/*.png')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'device: {device}')

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


preds = predict(crnn, predict_loader, Synth90kDataset.LABEL2CHAR,decode_method=decode_method,beam_size=beam_size)
show_result(images, preds)