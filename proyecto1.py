import cv2
from pyzbar.pyzbar import decode
import numpy as np

# Función para decodificar el código QR
#img = cv2.imread('qr.jpg')

cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)

while True:
    
    success, img = cap.read()
    for barcode in decode(img):
        print(barcode.data)
        myData = barcode.data.decode('utf-8')
        print(myData)
    
    cv2.imshow('Result', img)
    cv2.waitKey(1)

