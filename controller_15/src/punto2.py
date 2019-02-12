#!/usr/bin/env python
import rospy
import time
import numpy as np 
from pacman.msg import actions
from pacman.msg import pacmanPos
from pacman.msg import ghostsPos
from pacman.msg import cookiesPos
from pacman.msg import bonusPos
from pacman.msg import game
from pacman.msg import performance
from pacman.srv import mapService

# Variables globales del mapa para actualizar
xMax = 0
xMin = 0
yMax = 0
yMin = 0
mapaRec = None

def pacmanPosCallback(msg):
    # Publicar informacion sobre Pacman
    #rospy.loginfo('----Numero de Pacmans en juego: {}.'.format(msg.nPacman))
    #rospy.loginfo('Posicion de Pacman {}: x = {}, y = {}'.format(1, msg.pacmanPos.x, msg.pacmanPos.y))
    
    # Reiniciar posiciones anteriores
    for i in range(xMin,xMax):
        for j in range(yMin,yMax):
            if mapaRec[i,j] == 4:
                mapaRec[i,j] = 0
    # Establecer nuevas posiciones
    for i in range(xMin,xMax):
        for j in range(yMin,yMax):
            if (i == msg.pacmanPos.x) and (j == msg.pacmanPos.y):
                mapaRec[i+xMin,j+yMin] = 4
    pass

def ghostsPosCallback(msg):
    # Publicar informacion sobre los fantasmas
    #rospy.loginfo('----Numero de fantasmas: {}.'.format(msg.nGhosts)) 
    #for i in range(msg.nGhosts):
    #    rospy.loginfo('Posicion de fantasma {}: x = {}, y = {}'.format(i+1, msg.ghostsPos[i].x, msg.ghostsPos[i].y))
    
    # Reiniciar posiciones anteriores
    for i in range(xMin,xMax):
        for j in range(yMin,yMax):
            if mapaRec[i,j] == 9:
                mapaRec[i,j] = 0
    # Establecer nuevas posiciones
    for i in range(xMin,xMax):
        for j in range(yMin,yMax):
            for aux in range(msg.nGhosts):
                if (i == msg.ghostsPos[aux].x) and (j == msg.ghostsPos[aux].y):
                    mapaRec[i+xMin,j+yMin] = 9
    pass

def cookiesPosCallback(msg):
    # Publicar informacion sobre las galletas
    #rospy.loginfo('----Numero de Galletas: {}.'.format(msg.nCookies)) 
    #for i in range(msg.nCookies):
    #    rospy.loginfo('Posicion de Galleta {}: x = {}, y = {}'.format(i+1, msg.cookiesPos[i].x, msg.cookiesPos[i].y))
    
    # Reiniciar posiciones anteriores
    for i in range(xMin,xMax):
        for j in range(yMin,yMax):
            if mapaRec[i,j] == 6:
                mapaRec[i,j] = 0
    # Establecer nuevas posiciones
    for i in range(xMin,xMax):
        for j in range(yMin,yMax):
            for aux in range(msg.nCookies):
                if (i == msg.cookiesPos[aux].x) and (j == msg.cookiesPos[aux].y):
                    mapaRec[i+xMin,j+yMin] = 6
    pass

def bonusPosCallback(msg):
    # Publicar informacion sobre los Bonus
    #rospy.loginfo('----Numero de Bonus: {}.'.format(msg.nBonus)) 
    #for i in range(msg.nBonus):
    #    rospy.loginfo('Posicio de Bonus {}: x = {}, y = {}'.format(i+1, msg.bonusPos[i].x, msg.bonusPos[i].y))

    # Reiniciar posiciones anteriores
    for i in range(xMin,xMax):
        for j in range(yMin,yMax):
            if mapaRec[i,j] == 5 :
                mapaRec[i,j] = 0
    # Establecer nuevas posiciones
    for i in range(xMin,xMax):
        for j in range(yMin,yMax):
            for aux in range(msg.nBonus):
                if (i == msg.bonusPos[aux].x) and (j == msg.bonusPos[aux].y):
                    mapaRec[i+xMin,j+yMin] = 5
    pass

#def gameStateCallback(msg):
#    rospy.loginfo('Game State: {} '.format(msg.state)) 
#    pass

#def performanceCallback(msg):
#    rospy.loginfo('Lives: {} Score: {} Time: {} PerformEval: {}'.format(msg.lives, msg.score, msg.gtime, msg.performEval) )
#    pass

def show_elements():
    # Inicializar el nodo
    rospy.init_node('show_elements', anonymous=True)

    # Suscribirse a los topicos en los que publica el pacma_world
    rospy.Subscriber('pacmanCoord0', pacmanPos, pacmanPosCallback)
    rospy.Subscriber('ghostsCoord', ghostsPos, ghostsPosCallback)
    rospy.Subscriber('cookiesCoord', cookiesPos, cookiesPosCallback)
    rospy.Subscriber('bonusCoord', bonusPos, bonusPosCallback)
    #rospy.Subscriber('gameState', game, gameStateCallback)
    #rospy.Subscriber('performanceEval', performance, performanceCallback)

    try:
        # Solicitar el servicio del Mapa
        mapRequestClient = rospy.ServiceProxy('pacman_world', mapService)
        mapa = mapRequestClient("Leyendo Juego")
        rospy.loginfo("--- Numero de Obstaculos: {}".format(mapa.nObs))
        
        # Inicializacion de variables globales
        global xMin
        global xMax
        global yMin
        global yMax
        global mapaRec

        xMax = mapa.maxX 
        xMin = mapa.minX 
        yMax = mapa.maxY   
        yMin = mapa.minY

        print("Dimensiones en x : "+ str(xMin) + "," +str(xMax))
        print("Dimensiones en y : "+ str(yMin) + "," +str(yMax))
        mapaRec = np.zeros([xMax-xMin,yMax-yMin])
        
        # Reconstruccion de objetos en el mapa
        for i in range(xMin,xMax):
            for j in range(yMin,yMax):
                for aux in range(mapa.nObs):
                    if (i == mapa.obs[aux].x) and (j == mapa.obs[aux].y):
                        mapaRec[i+xMin,j+yMin] = 1

        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            print(np.flip(mapaRec.transpose(),0))
            print("----------------------------")
            rate.sleep()
        
    except rospy.ServiceException as e:
        print ("Error!! Make sure pacman_world node is running ")

    #rospy.spin()

if __name__ == '__main__':
    try:
        show_elements()
    except rospy.ROSInterruptException:
        pass

