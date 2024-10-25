import numpy as np
import cv2

#Essa função recebe a imagem da câmera cv2 e transforma os pixels 
#em um array vetorial de numpy, sendo assim identificada na base
#de dados pelo label (hash);
def process_image(image): 
    return "";

#Essa função recebe uma imagem e reajusta seu tamanho antes de 
#ser reconhecida para diminuir o tempo de reconhecimento antes
#de receber o label correto
def resizing(image):
    small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    return small_frame;

#Essa função recebe uma imagem e ajusta seu contraste através do cv2
#para ter uma exatidão melhor na hora de a imagem ser reconhecida.
def brightness_contrast(image):
    return ""