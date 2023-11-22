# Librerías necesarias para el funcionamiento del programa
import cv2
from pyzbar.pyzbar import decode
import json

# Función para imprimir la información de un usuario
def imprimir_informacion(qr_info):
    print('Información:')
    print('RUN:', qr_info['RUN'])
    print('Número de pulsera:', qr_info['Numero de pulsera'])
    print('Todas las banderas y comentarios:')
    for info_key, info_value in qr_info['Informacion'].items():
        print(f'{info_key}:')
        print('Bandera:', info_value['Bandera'])
        print('Comentario:', info_value['Comentario'])

# Camara para capturar el código QR
cap = cv2.VideoCapture(1)  # Puedes cambiar el índice a 1 si tienes múltiples cámaras
cap.set(3, 640)
cap.set(4, 480)

# Variable para detectar el código QR y detener la captura
qr_detected = False

# Leer la lista de códigos QR guardados en un archivo JSON
try:
    with open('qr_info.json', 'r') as json_file:
        qr_info_list = json.load(json_file)
except FileNotFoundError:
    qr_info_list = []

# Ciclo principal
while True:
    print("\nMenú:")
    print("1. Escanear código QR")
    print("2. Ver información existente")
    print("3. Salir")

    opcion = input("Ingrese la opción deseada: ")

    if opcion == "1":
        # Ciclo para capturar el código QR
        while not qr_detected:
            # Leer la imagen de la cámara
            success, img = cap.read()

            # Decodificar el código QR
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                run = myData.split("RUN=")[1]
                run = run.split("&")[0]

                # Validar la pulsera antes de agregarla a la lista
                nro_pulsera = input("Ingrese el número de pulsera (máximo 10 caracteres): ")

                if len(nro_pulsera) <= 10:
                    # Verificar si el código QR ya está en la lista
                    qr_exists = any(qr['RUN'] == run for qr in qr_info_list)

                    if qr_exists:
                        qr_detected = True
                        for qr in qr_info_list:
                            if qr['RUN'] == run:
                                # Actualizar el número de pulsera
                                qr['Numero de pulsera'] = nro_pulsera

                                imprimir_informacion(qr)

                                # Generar una clave única para cada nueva entrada de información adicional
                                info_key = 'Informacion' + str(len(qr['Informacion']) + 1)

                                # Agregar un nuevo diccionario bajo la clave única
                                qr['Informacion'][info_key] = {
                                    'Bandera': input("Ingrese las banderas: "),
                                    'Comentario': input("Ingrese los comentarios: ")
                                }
                                break
                    else:
                        # Agregar el diccionario a la lista
                        qr_info = {
                            'RUN': run,
                            'Numero de pulsera': nro_pulsera,
                            'Informacion': {
                                'Informacion1': {
                                    'Bandera': input("Ingrese las banderas: "),
                                    'Comentario': input("Ingrese los comentarios: ")
                                }
                            }
                        }

                        qr_info_list.append(qr_info)

                        # Imprimir la información del nuevo usuario
                        imprimir_informacion(qr_info)

                    # Guardamos la lista de códigos QR en un archivo JSON
                    with open('qr_info.json', 'w') as json_file:
                        json.dump(qr_info_list, json_file, indent=4)

                    # Detener la captura
                    qr_detected = True
                else:
                    print("Número de pulsera inválido. Debe tener como máximo 10 caracteres.")

            cv2.imshow('Result', img)
            cv2.waitKey(1)

    elif opcion == "2":
        # Ciclo para capturar el código QR
        while not qr_detected:
            # Leer la imagen de la cámara
            success, img = cap.read()

            # Decodificar el código QR
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                run = myData.split("RUN=")[1]
                run = run.split("&")[0]

                # Verificar si el código QR está en la lista
                qr_exists = any(qr['RUN'] == run for qr in qr_info_list)

                if qr_exists:
                    for qr_info in qr_info_list:
                        if qr_info['RUN'] == run:
                            imprimir_informacion(qr_info)
                            break
                        
                    else:
                        print("No se encontró información para el código QR escaneado.")
                else:
                    print("El código QR no existe. Primero debe escanearlo e ingresarlo.")

                # Detener la captura
                qr_detected = True

            cv2.imshow('Result', img)
            cv2.waitKey(1)





    elif opcion == "3":
        # Salir del programa
        break

    else:
        print("Opción no válida. Por favor, ingrese una opción válida.")

# Liberar la captura de la cámara
cap.release()
cv2.destroyAllWindows()
