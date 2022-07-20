
-Para la calibración de la cámara se utilizó un tablero 9x6 y se obtuvieron las matrices de calibración y distorsión con el objetivo de obtener "tvec" que es lo necesario para el cálculo de la distancia.


![Imagen1](https://github.com/cascajo3/EurobotOpenCV/blob/main/Distancia/prueba1.png)
![Imagen2](https://github.com/cascajo3/EurobotOpenCV/blob/main/Distancia/prueba2.png)


-ACTUALIZACIÓN: El siguiente avance ha sido intentar implementar lo anterior en una Raspberry Pi Zero.

Pese a tener poca potencia, se ha conseguido con la ayuda de la cámara la detección del AruCo y la distancia (aunque falta por pulir la matriz de distorsión usando más imágenes para su calibración y la mejora en la fluidez de detección de los frames) en Raspberry Pi OS.
