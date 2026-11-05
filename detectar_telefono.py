
import cv2
import random
import vlc

from pathlib import Path
from ultralytics import YOLO

modelo = YOLO("yolo26n.pt")

camara = cv2.VideoCapture(0)

carpetaVideos = Path("videos")

videos = (
    list(carpetaVideos.glob("*.mp4")) +
    list(carpetaVideos.glob("*.avi")) +
    list(carpetaVideos.glob("*.mov"))
)

instancia = vlc.Instance()
reproductor = instancia.media_player_new()

videoActivo = False
videoActual = None

def reproducirVideo():
    global videoActual

    videoActual = random.choice(videos)

    media = instancia.media_new(str(videoActual))
    reproductor.set_media(media)
    reproductor.play()

    print("Reproduciendo:", videoActual.name)


print("Programa iniciado")

while True:

    correcto, imagen = camara.read()

    if not correcto:
        print("Error al acceder a la cámara")
        break

    resultados = modelo.predict(
        imagen,
        classes=[67],
        conf=0.40,
        verbose=False
    )

    movilDetectado = len(resultados[0].boxes) > 0

    imagenDetectada = resultados[0].plot()
    cv2.imshow("Temporizador de Estudio", imagenDetectada)

    if movilDetectado:

        if not videoActivo:

            if videos:
                videoActivo = True
                reproducirVideo()
            else:
                print("No hay vídeos en la carpeta 'videos'")

        
        if videoActivo and reproductor.get_state() == vlc.State.Ended:
            reproducirVideo()

    else:

        if videoActivo:
            reproductor.stop()
            videoActivo = False
            print("Telefono retirado. ¡Ponte a estudiar!")

   
    tecla = cv2.waitKey(1)

    if tecla == 27:
        break

    if cv2.getWindowProperty(
        "Temporizador de Estudio",
        cv2.WND_PROP_VISIBLE
    ) < 1:
        break
    
reproductor.stop()
camara.release()
cv2.destroyAllWindows()

print("Programa cerrado")
