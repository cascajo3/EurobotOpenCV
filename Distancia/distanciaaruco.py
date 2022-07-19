
#Fuentes
#pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/
#github.com/tizianofiorenzani/how_do_drones_work/tree/master/opencv

from imutils.video import VideoStream
import imutils
import time
import cv2
import sys
import numpy as np
import cv2.aruco as aruco  

#Los códigos de eurobot son 4x4
arucoDict = cv2.aruco.Dictionary_get(aruco.DICT_4X4_1000)
arucoParams = cv2.aruco.DetectorParameters_create()

#Para calcular la matriz se ha utilizado otro script que analiza las imágenes sobre un tablero 9x6 de ajedrez y genera 2 txt que son 2 matrices 
#para la cameraMatrix y para el distCoeffInit
cameraMatrix=np.array([[8.076850796744689660e+02,0.000000000000000000e+00,6.421958068073640788e+02],
                                 [0.000000000000000000e+00,8.156196098810844433e+02,4.212121397910903511e+02],
                                 [0.000000000000000000e+00,0.000000000000000000e+00,1.000000000000000000e+00]])

distCoeffsInit = np.array([1.499148298275206903e-01,-5.700021300945858904e-01,2.540227249710461793e-02,5.650734482171571038e-03,1.393534846970322594e+00])

#Tamaño del código en metros
markerSizeInM = 0.094

# Iniciamos la web cam y esperamos a que se encienda
print("Iniciando la transmisión desde la cámara...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
	# Se utiliza un máximo de 1000 pixels en el frame
	frame = vs.read()
	frame = imutils.resize(frame, width=1000)
	
	# Detectamos arucos en el frame
	(corners, ids, rejected) = cv2.aruco.detectMarkers(frame,arucoDict, parameters=arucoParams)
	rvec , tvec, trash = aruco.estimatePoseSingleMarkers(corners, markerSizeInM, cameraMatrix,distCoeffsInit)
        	# Se verifica que como mínimo hay un aruco detectado
	if len(corners) > 0:
		#reducción de dimensión
		ids = ids.flatten()

		# Bucle sobre los arucos detectados
		for (markerCorner, markerID) in zip(corners, ids):
			#Posición de las esquinas del aruco

			corners = markerCorner.reshape((4, 2))
			(topLeft, topRight, bottomRight, bottomLeft) = corners

			# Se transforman en enteros
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))

			#z es el eje z del aruco
			z=tvec[0][0][2]

			#redondeamos a 3 decimales
			z=round(z,3)

			#Ponemos la distancia en la esquina
			cv2.putText(frame, str(z),
				(topLeft[0], topLeft[1] - 15),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (0, 0, 0), 2)        

			# Se dibuja la caja que los contiene para marcarlos
			cv2.line(frame, topLeft, topRight, (0, 0, 255), 2)
			cv2.line(frame, topRight, bottomRight, (0, 0, 255), 2)
			cv2.line(frame, bottomRight, bottomLeft, (0, 0, 255), 2)
			cv2.line(frame, bottomLeft, topLeft, (0, 0, 255), 2)

			#Se marca y se calcula (x,y) el centro del aruco
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
			cv2.circle(frame, (cX, cY), 4, (0, 255, 0), -1)

			# Se dibuja el número del aruco
			#cv2.putText(frame, str(markerID),
			#	(topLeft[0], topLeft[1] - 15),
			#	cv2.FONT_HERSHEY_SIMPLEX,
			#	0.5, (0, 255, 0), 2)

	# Salida 
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# Se sale del bucle pulsando la "q"
	if key == ord("q"):
		break

# Se cierran el resto de ventanas
cv2.destroyAllWindows()
vs.stop()


