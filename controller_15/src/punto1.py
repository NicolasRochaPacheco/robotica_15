#!/usr/bin/env python

#----------------------------------------------------------------------
#
#	TAREA0, PUNTO1
#	GRUPO 15
#
#----------------------------------------------------------------------




# Importamos la libreria de rospy
import rospy

# Importamos la libreria de pygame como interfaz de usuario.
import pygame

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

# Funcion que devuelve la tecla que esta siendo presionada. Sera
# lanzada como un hilo.


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

# Inicializamos pygame y una ventana
pygame.init()
(width, height) = 	(300, 200)
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 255))
pygame.display.set_caption("Grupo 15: Punto 1")
pygame.display.flip()

# Loop infinito para mantener el nodo mientras sea necesario.
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()




# Enviamos la solicitud para iniciar el juego
mapRequestClient = rospy.ServiceProxy('pacman_world', mapService)
mapa = mapRequestClient(nombre)

# Enviamos el comando para controlar a Pacman
rate = rospy.Rate(10)
msg = actions()
num = 0
while not rospy.is_shutdown():
	msg.action = num
	pub.publish(msg.action)
	rate.sleep()
