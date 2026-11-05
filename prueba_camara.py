import cv2

webcam = cv2.VideoCapture(0)

while True:
    encendido, capturaImagen = webcam.read()
    
    if not encendido:
        print("No hemos podido encontrar la webcam... Vuelve a intentarlo.")
        break

    cv2.imshow("Temporizador - Webcam", capturaImagen)
    
    if cv2.waitKey(1) == 27:
        print("Cerrando la webcam...")
        break;
    
webcam.release()
cv2.destroyAllWindows()
