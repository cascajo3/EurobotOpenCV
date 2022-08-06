En este proyecto se trabaja con el detector YOLO para personas (aunque detecta muchos objetos), el de género usado anteriormente y el de la pose.

El objetivo era trazar una línea que fuera desde la nariz hasta el punto medio entre las caderas y fuese de color rosa en el caso de ser mujer o verde en el caso de ser hombre.


La manera de proceder ha sido utilizar el detector YOLO para aislar a cada persona encontrada a la que se le pasará el detector de cara, género y pose individualmente para sacar los puntos (se procede así porque si se pasa el detector de pose con toda la imagen sólo detecta a 1 persona). Desconozco si habría alguna mejor manera de proceder, pero esta me ha parecido la más intuitiva.

Estaba destinado sólo a identificar lo previo en una foto con 2 personas de frente.

Los resultados obtenidos son:

![Imagen1](https://github.com/cascajo3/EurobotOpenCV/blob/main/GenderPoseLines/images/foto1.jpg)


![Imagen2](https://github.com/cascajo3/EurobotOpenCV/blob/main/GenderPoseLines/images/imagenfinal1.jpg)

![Imagen3](https://github.com/cascajo3/EurobotOpenCV/blob/main/GenderPoseLines/images/foto3.jpg)


![Imagen4](https://github.com/cascajo3/EurobotOpenCV/blob/main/GenderPoseLines/images/imagenfinal3.jpg)



Se trata de un código lioso porque apenas ha sido pulido dividiendo bien las funciones o modificándolo para que trazase lo previo en más de 2 persona en las fotos. También faltaría añadirle los casos de error para que mandase un mensaje diciendo que no ha podido detectar los requisitos mínimos en las fotos.


Para mejorarlo simplemente habría que hacerlo más legible y dividirlo mejor en funciones.