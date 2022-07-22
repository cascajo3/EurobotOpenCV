
En esta carpeta están los 2 archivos utilizados para el mini-robot que se acerca o se aleja al ArUco en función de una distancia objetivo.

<video src="https://github.com/cascajo3/EurobotOpenCV/blob/main/arduinoRaspAruco/video.MOV" style="max-width: 730px;">
</video>


Como se puede apreciar, está muy limitado y simplemente es un pequeño prototipo.

Problemas a solucionar:
-Aumentar la alimentación del L298N como mínimo a 9 (en el ejemplo se alimentó a 6V).

-Mejorar la colocación de cada parte encima del acrílico del robot para que no dificulte o impida que el robot pueda ir recto.

-Realizar el control del robot de una manera eficiente (en este ejemplo sólo tenía implementado el avance y el retroceso, aunque. tampoco conseguía ir del todo recto)

-Mejorar la tasa de detección de los frames en la raspberry pi, aunque esto se debe a que sólo tiene 512mb de RAM y va muy lento. En el vídeo se aprecia que tarda varios segundos en reaccionar con el robot a la nueva distancia.


