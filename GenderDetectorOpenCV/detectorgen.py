#Fuentes: sefiks.com
import cv2 as cv
import numpy as np

#Nombre de la imagen que usaremos
img=cv.imread("nombredelaimagen.jpg")

#Los documentos se encuentran en el paper de los creadores: data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki y en el github de OpenCv/data
gender_model = cv.dnn.readNetFromCaffe("deploy_gender.prototxt","gender_net.caffemodel")


#El documento originalmente se llama: haarcascade_frontalface_default.xml 
haar_cascade= cv.CascadeClassifier('caras.xml')

#Función que convierte la imagen en blanco y negro y pasa la función detectMultiScale
def detect_faces(img):
    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    faces=haar_cascade.detectMultiScale(gray, 1.1, 9)
    return faces


faces= detect_faces(img)


#Nos interesa conocer las filas para saber cuántos rectángulos tenemos para diferenciar el número de caras detectadas
rows,columns=faces.shape

for i in range(rows):
    #Necesitamos un vector 1x3 para cada cara detectada
    x,y,w,h=faces[i]
    t=img[int(y):int(y+h), int (x):int(x+w)]
    #Se adapta el tamaño en función a lo requerido en la documentación
    t = cv.resize(t,(224, 224))
    #Preprocesamiento
    img_blob = cv.dnn.blobFromImage(t)
    #Se lo pasamos al modelo
    gender_model.setInput(img_blob)
    gender_class = gender_model.forward()[0]
    #Distinguimos la salida en función del resultado
    gender = 'Mujer' if np.argmax(gender_class) == 0 else 'Hombre'
    #Imprimimos el género por la terminal
    print(gender)
    #Guardamos el primer rectángulo detectado en 'cara'
    cara=faces[i]
    #Dependiendo del género el color será azul o rosa
    if np.argmax(gender_class)==0:
        color=(255,0,255)
    else:
        color=(255,255,0)
    #Dibujamos el cuadrado de la cara e imprimimos el texto con el resultado encima
    dib= cv.rectangle(img,(cara[0],cara[1]),(cara[0]+cara[2],cara[1]+cara[3]),color,1)
    cv.putText(dib, gender, (cara[0], cara[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.99, color,2)
   
#Mostramos la imagen modificada
cv.imshow('Detector:',img)
#Mostramos por la terminal el número de caras que se han detectado
print("Se han detectado:", rows ,"caras")

k = cv.waitKey(0)
if k == 27:         # Salimos con ESC
    cv.destroyAllWindows()
elif k == ord('s'): # wSi pulsamos la 's' guardaremos la imagen
    cv.imwrite('imagenguardada4.png',img)
    cv.destroyAllWindows()
