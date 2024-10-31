'''Funções utils para auxiliar no processamento da imagem'''
import cv2
import numpy as np

def gamma_correction(frame, gamma=1.0):
    '''Função responsável por ajustar a correção gamma da imagem
    recebe um frame atual e retorna o valor gamma balanceado para a mesma'''
    
    inv_gamma = 1.0/ gamma
    table = np.array([(i/255.0) ** inv_gamma * 255 for i in np.arange(0, 255)]).astype("uint8")
    return cv2.LUT(frame, table)

def brightness_contrast(frame):
    '''Essa função recebe uma imagem e ajusta seu contraste através do cv2
para ter uma exatidão melhor na hora de a imagem ser reconhecida, comparando 
o valor médio de pixels claros numa imagem em grayscale e ajusta baseado nisso.
Retorna o valor gamma e a frame'''
    
    grayScale = cv2.cvColor(frame, cv2.COLOR_BGR2GRAY)
    
    mean_scale = np.mean(grayScale)
    
    if mean_scale < 50:
        gamma = 1.5
    elif mean_scale > 200:
        gamma = 0.5
    else: gamma = 1.0
    
    return gamma_correction(frame, gamma)
