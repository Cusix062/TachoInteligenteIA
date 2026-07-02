import cv2
import numpy as np
import tensorflow as tf
from datetime import datetime
import csv
import os

os.makedirs("capturas", exist_ok=True)

modelo = tf.keras.models.load_model("modelo/tacho_ia.h5")

clases = ["glass", "metal", "paper", "plastic", "trash"]

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cv2.namedWindow("Tacho Inteligente IA", cv2.WINDOW_NORMAL)

print("=== Tacho Inteligente IA ===")
print("Presiona S para guardar el registro y captura")
print("Presiona ESC para salir")
print(f"Clases: {clases}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo capturar el frame")
        break

    imagen = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imagen = cv2.resize(imagen, (224, 224))
    imagen = np.expand_dims(imagen, axis=0)

    prediccion = modelo.predict(imagen, verbose=0)
    indice = np.argmax(prediccion)
    categoria = clases[indice]
    confianza = float(np.max(prediccion) * 100)

    color = (0, 255, 0)
    if confianza < 60:
        color = (0, 255, 255)
    if confianza < 40:
        color = (0, 0, 255)

    texto = f"{categoria} ({confianza:.1f}%)"
    cv2.putText(frame, texto, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    bar_width = int(confianza * 3)
    cv2.rectangle(frame, (20, 60), (20 + bar_width, 70), color, -1)
    cv2.putText(frame, f"Confianza: {confianza:.1f}%", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv2.imshow("Tacho Inteligente IA", frame)

    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord('s') or tecla == ord('S'):
        timestamp = datetime.now()
        filename = f"capturas/{timestamp.strftime('%Y%m%d_%H%M%S')}_{categoria}.jpg"
        cv2.imwrite(filename, frame)
        with open("registros.csv", "a", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow([timestamp, categoria, f"{confianza:.1f}"])
        print(f"Registrado: {categoria} ({confianza:.1f}%) -> {filename}")

    if tecla == 27:
        break

cap.release()
cv2.destroyAllWindows()
print("Sistema cerrado")
