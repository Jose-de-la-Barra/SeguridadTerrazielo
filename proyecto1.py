import cv2
from pyzbar.pyzbar import decode
import re

# Función para decodificar el código QR

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

found_qr = False  # Variable de control para determinar si se encontró un código QR

while not found_qr:
    success, img = cap.read()

    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        run = myData.split("RUN=")[1]
        run = run.split("&")[0]
        print(run)
        found_qr = True  # Establece la variable de control en True cuando se encuentra un código QR

    cv2.imshow('Result', img)
    cv2.waitKey(1)

# Liberar la captura de la cámara
cap.release()
cv2.destroyAllWindows()
