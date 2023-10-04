import cv2
from pyzbar.pyzbar import decode
import json

# Función para decodificar el código QR

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# Variable de control para determinar si se ha detectado un código QR
qr_detected = False

while not qr_detected:
    success, img = cap.read()

    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        run = myData.split("RUN=")[1]
        run = run.split("&")[0]
        print(run)

        # Cargar los registros existentes desde el archivo JSON si existe
        try:
            with open('qr_info.json', 'r') as json_file:
                qr_info_list = json.load(json_file)
        except FileNotFoundError:
            qr_info_list = []

        # Crear un diccionario con la información del código QR
        qr_info = {
            'RUN': run,
            'bandera': '',
            'comentario': ''
        }

        qr_info_list.append(qr_info)

        # Guardar la lista actualizada en un archivo JSON
        with open('qr_info.json', 'w') as json_file:
            json.dump(qr_info_list, json_file, indent=4)

        qr_detected = True

    cv2.imshow('Result', img)
    cv2.waitKey(1)

# Liberar la captura de la cámara
cap.release()
cv2.destroyAllWindows()
