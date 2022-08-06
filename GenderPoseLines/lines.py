import cv2 as cv
import numpy as np
import mediapipe as mp

#Las fuentes han sido una mezcla de las previas para el detector de género y algún artículo para aprender a usar YOLO.
#Los documentos se encuentran en el paper de los creadores: data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki y en el github de OpenCv/data
gender_model = cv.dnn.readNetFromCaffe("deploy_gender.prototxt","gender_net.caffemodel")


#El documento originalmente se llama: haarcascade_frontalface_default.xml 
haar_cascade= cv.CascadeClassifier('caras.xml')

#Cargamos el algoritmo YOLO
net=cv.dnn.readNet("yolov3.weights","yolov3.cfg")

#Creamos las clases para los objetos detectados
classes=[]

#abrimos el archivo de los nombres de las clases y leemos todas las líneas
with open("coco.names", "r") as f: 
  classes = [line.strip() for line in f.readlines()] 
#Relacionas cada nombre de la clase 
output_layers=[]
layer_names=net.getLayerNames()
for i in net.getUnconnectedOutLayers():
    output_layers.append(layer_names[i-1])


#Se carga la imagen
img=cv.imread("images/foto1.jpg")
height,width,channels=img.shape


#Se extraen las características de los objetos detectados
blob=cv.dnn.blobFromImage(img,0.00392,(416,416),(0,0,0),True,crop=False)
#FUNCIONES:

def detect_faces(img):
    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    faces=haar_cascade.detectMultiScale(gray, 1.1, 9)
    return faces

def genderfunt(img):
        faces= detect_faces(img)
        #Necesitamos un vector 1x3 para cada cara detectada
        x,y,w,h=faces[0]
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
        return np.argmax(gender_class)




#Se pasa el blob al algoritmo
net.setInput(blob)
outs=net.forward(output_layers)


#Para mostrar la información
class_ids=[]
confidences=[]
boxes=[]
for output in outs:
    for detection in output:
        #Pasos para la confianza
        scores=detection[5:]                #1
        class_id=np.argmax(scores)          #2
        confidence =scores[class_id]        #3

        if confidence >0.5: #Tolerancia de los parámetros
            center_x=int(detection[0]*width)
            center_y=int(detection[1]*height)
            w=int(detection[2]*width)
            h=int(detection[3]*height)

            #Se trazan los rectángulos
            x=int(center_x-w/2) # IZQ
            y=int(center_y-h/2) # DER

            boxes.append([x,y,w,h])
            confidences.append(float(confidence))
            class_ids.append(class_id)
           

#para eliminar cajas dobles
indexes=cv.dnn.NMSBoxes(boxes,confidences,0.3,0.4)
cropped_image=[]
cropped_image2=[]
contador=0
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = classes[class_ids[i]]  #nombre de los objetos
        #Sólo queremos que nos recuadre a las personas y no al resto
        if label=='person':
           
            if contador==1:
                cropped_image2 = img[y:y+h,x:x+w]
               

            if contador==0:
                cropped_image = img[y:y+h,x:x+w]
               
                contador=contador+1


            

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

var=contador+1
original=img


#Tenemos que pasar esta parte 2 veces, una para imagen, luego se trazarán las líneas en la original
for q in range(var):
    if q==0:
        img=cropped_image
    else:
        img=cropped_image2

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results =  pose.process(imgRGB)

    for id, lm in enumerate(results.pose_landmarks.landmark):
        h,w,c =img.shape
        cx, cy = int(lm.x * w), int (lm.y *h)
        lista=([id,cx,cy])
        if(lista[0]==23):
            nlist=(cx,cy)
        if(lista[0]==24):
            nlist2=(cx,cy)

        if(lista[0]==0):
            nariz=(cx,cy)

    pmediox= (nlist[0]+nlist2[0])/2
    pmedioy=(nlist[1]+nlist2[1])/2


#Queremos obtener el punto medio entre la cadera izquierda y la derecha.

    if results.pose_landmarks:
    #mpDraw.draw_landmarks(img, results.pose_landmarks)
       # img=cv.circle(img,nlist,4,(0,0,255),3)
       # img=cv.circle(img,nlist2,4,(0,0,255),3)
       # img=cv.circle(img,(int(pmediox),int(pmedioy)),4,(255,0,0),3)
      #  img=cv.circle(img,nariz,4,(255,0,0),3)
        gen= genderfunt(img)
        if gen==0:
            cv.line(img,(int(pmediox),int(pmedioy)), nariz, (255,0,255), 2)
        else:
            cv.line(img,(int(pmediox),int(pmedioy)), nariz, (0,255,0), 2)


half = cv.resize(original, (0, 0), fx = 0.49, fy = 0.49)
#Mostramos la imagen modificada
cv.imshow('Detector:',half)   
       

k = cv.waitKey(0)
if k == 27:         # Salimos con ESC
    cv.destroyAllWindows()
elif k == ord('s'): # wSi pulsamos la 's' guardaremos la imagen
    cv.imwrite('imagenfinal.jpg',original)
    cv.destroyAllWindows()