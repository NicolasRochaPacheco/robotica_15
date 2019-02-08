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

# Importamos los mensajes y servicios de PacMan
from pacman.msg import actions
from pacman.msg import pacmanPos
from pacman.srv import mapService

#----------------------------------------------------------------------
#	FUNCIONES
#----------------------------------------------------------------------

# Defiinimos la funcion de callback para la actualizacion
# del topico de la posicion del Pacman.
def posCallback(data):
	pass

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

# Inicializamos el nodo, creamos un publisher y un suscriptor
rospy.init_node('grupo15_punto1', anonymous=True)
pub = rospy.Publisher('pacmanActions0', actions, queue_size=10)
rospy.Subscriber('pacmanCoord0', pacmanPos, posCallback)

# Enviamos la solicitud para iniciar el juego
mapRequestClient = rospy.ServiceProxy('pacman_world', mapService)
mapa = mapRequestClient(nombre)

# Enviamos el comando para controlar a Pacman
rate = rospy.Rate(60)
msg = actions()

print( 'Para terminar la ejecucion presione ESC y luego CTRL + C' )

# Lanzamos el hilo que revisa que tecla esta siendo presionada.
key.start()

# Ciclo en el cual trabaja el nodo.
while not rospy.is_shutdown():
	msg.action = key.getNumber()
	pub.publish(msg.action)
	rate.sleep()


