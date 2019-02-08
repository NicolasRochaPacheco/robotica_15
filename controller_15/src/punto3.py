#!/usr/bin/env python

#----------------------------------------------------------------------
#
#	TAREA0, PUNTO1
#	GRUPO 15
#
#----------------------------------------------------------------------

# Importamos la libreria de rospy
import rospy

# Importamos el hilo para leer los comandos del teclado.
from keyboard import Keyreader

# Importamos numpy para el manejo de matrices
import numpy as np

# Importamos los mensajes y servicios de PacMan
from pacman.msg import actions
from pacman.msg import pacmanPos
from pacman.srv import mapService



#----------------------------------------------------------------------
#	FUNCIONES
#----------------------------------------------------------------------

# Defiinimos la funcion de callback para la actualizacion
# del topico de la posicion del Pacman.
#
# Una matriz con banderas sera utilizada si el pacman no se puede mover
def posCallback(data):
	pacman_x = data.pacmanPos.x + abs(mapa.minX)
	pacman_y = data.pacmanPos.y + abs(mapa.minY)
	if map_array[pacman_x, pacman_y+1] == 1:
		flags[0] = 1
	else:
		flags[0] = 0
	
	if map_array[pacman_x, pacman_y-1] == 1:
		flags[1] = 1
	else:
		flags[1] = 0

	if map_array[pacman_x+1, pacman_y] == 1:
		flags[2] = 1
	else:
		flags[2] = 0

	if map_array[pacman_x-1, pacman_y] == 1:
		flags[3] = 1
	else:
		flags[3] = 0

# Creamos el objeto del hilo para leer la tecla que esta siendo 
# presionada.
key = Keyreader()

#----------------------------------------------------------------------
#	VARIABLES / CONSTANTES
#----------------------------------------------------------------------

# Variable para almacenar el nombre del jugador
nombre = 'grupo_15'

# Variable para mantener el nodo corriendo
running = True

#----------------------------------------------------------------------
#	LOGICA DEL NODO
#----------------------------------------------------------------------

# INICIALIZACION

# Inicializamos el nodo, creamos un publisher y un suscriptor
rospy.init_node('grupo15_punto1', anonymous=True)
pub = rospy.Publisher('pacmanActions0', actions, queue_size=10)
rospy.Subscriber('pacmanCoord0', pacmanPos, posCallback)

# Enviamos la solicitud para iniciar el juego
mapRequestClient = rospy.ServiceProxy('pacman_world', mapService)
mapa = mapRequestClient(nombre)

# Creamos la matriz que representa el mapa.
x_dim = abs(mapa.minX) + mapa.maxX + 1
y_dim = abs(mapa.minY) + mapa.maxY + 1
map_array = np.zeros((x_dim, y_dim))

# Agregamos los obstaculos al arreglo
obs_array = mapa.obs
for obs in obs_array:
	x = obs.x + abs(mapa.minX)
	y = obs.y + abs(mapa.minY)
	map_array[x, y] = 1

# Enviamos el comando para controlar a Pacman
rate = rospy.Rate(60)
msg = actions()

print( 'Para terminar la ejecucion presione ESC y luego CTRL + C' )

# Lanzamos el hilo que revisa que tecla esta siendo presionada.
key.start()

# Registro de banderas con los movimientos posibles de pacman.
flags = [0, 0, 0, 0]


# EJECUCION

# Variable con el comando que se va a enviar.
num = 4

# Variable con la direccion futura deseada.
fut = 4

# Ciclo en el cual trabaja el nodo.
while not rospy.is_shutdown():
	intended = key.getNumber()

	if intended != 4:

		if intended == 0 and flags[0] == 0:
			num = 0
		if intended == 1 and flags[1] == 0:
			num = 1
		if intended == 2 and flags[2] == 0:
			num = 2
		if intended == 3 and flags[3] == 0:
			num = 3

		if intended == 0 and flags[0] == 1:
			fut = 0
		if intended == 1 and flags[1] == 1:
			fut = 1
		if intended == 2 and flags[2] == 1:
			fut = 2
		if intended == 3 and flags[3] == 1:
			fut = 3

	if fut == 0 and flags[0] == 0:
		num = fut
		fut = 4
	if fut == 1 and flags[1] == 0:
		num = fut
		fut = 4
	if fut == 2 and flags[2] == 0:
		num = fut
		fut = 4
	if fut == 3 and flags[3] == 0:
		num = fut
		fut = 4




	pub.publish(num)
	rate.sleep()
