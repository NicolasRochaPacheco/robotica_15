#!/usr/bin/env python

#----------------------------------------------------------------------
#
#	TAREA0, PUNTO1
#	GRUPO 15
#
#----------------------------------------------------------------------




# Importamos la libreria de rospy
import rospy

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

#----------------------------------------------------------------------
#	VARIABLES / CONSTANTES
#----------------------------------------------------------------------

# Variable para almacenar el nombre del jugador
nombre = 'grupo_15'

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
rate = rospy.Rate(10)
msg = actions()
while not rospy.is_shutdown():
	msg.action = 3
	pub.publish(msg.action)
	rate.sleep()

