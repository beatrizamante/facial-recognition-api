import numpy as np
import cv2

def resizing(image):
    '''Essa função recebe uma imagem e reajusta seu tamanho antes de 
ser reconhecida para diminuir o tempo de reconhecimento antes
de receber o label correto'''

    small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    return small_frame;

def brightness_contrast(image):
    '''Essa função recebe uma imagem e ajusta seu contraste através do cv2
para ter uma exatidão melhor na hora de a imagem ser reconhecida.'''
    return ""

