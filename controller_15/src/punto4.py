#!/usr/bin/env python
import rospy
import time
#import networkx as nx
from pacman.msg import actions
from pacman.msg import pacmanPos
from pacman.msg import ghostsPos
from pacman.msg import cookiesPos
from pacman.msg import bonusPos
from pacman.msg import game
from pacman.msg import performance
from pacman.srv import mapService

#Variables para actualiza
pacmanX = 0
pacmanY = 0
actualAction = 2 

def pacmanPosCallback(msg):
	global pacmanX
	pacmanX = msg.pacmanPos.x
	global pacmanY
	pacmanY = msg.pacmanPos.y

def ghostsPosCallback(msg):
    pass

def cookiesPosCallback(msg):
  	pass

def bonusPosCallback(msg):
    pass

def gameStateCallback(msg):
#    rospy.loginfo('Game State: {} '.format(msg.state)) 
    pass

def performanceCallback(msg):
#    rospy.loginfo('Lives: {} Score: {} Time: {} PerformEval: {}'.format(msg.lives, msg.score, msg.gtime, msg.performEval) )
    pass

def actionsCallback(msg):
	global actualAction
	actualAction = msg.action


def right_hand():
    rospy.init_node('right_hand', anonymous=True)
    pub = rospy.Publisher('pacmanActions0', actions, queue_size=10)
    rospy.Subscriber('pacmanCoord0', pacmanPos, pacmanPosCallback)
    rospy.Subscriber('ghostsCoord', ghostsPos, ghostsPosCallback)
    rospy.Subscriber('cookiesCoord', cookiesPos, cookiesPosCallback)
    rospy.Subscriber('bonusCoord', bonusPos, bonusPosCallback)
    rospy.Subscriber('gameState', game, gameStateCallback)
    rospy.Subscriber('performanceEval', performance, performanceCallback)
    #rospy.spin()
    try:
		mapRequestClient = rospy.ServiceProxy('pacman_world', mapService)
		mapa = mapRequestClient("Leyendo mapa")
		obs = mapa.obs
		rate = rospy.Rate(6.666666666666666666666666666666666666)
		msg = actions();
		global actualAction
		actualAction = 2
		tiempo = 0.00000000000000000000000000000000001

		while not rospy.is_shutdown():
			#pacmanPosCallback0(pacmanPos())
			print(pacmanX)
			print(pacmanY)
			#actionsCallback(actions)
			paredIzquierda = False
			paredDerecha = False
			paredAbajo = False
			paredArriba = False

			for i in obs:
				obsX = i.x
				obsY = i.y
				if((obsX == pacmanX-1) and (obsY == pacmanY)):
					paredIzquierda = True
				if((obsX == pacmanX+1) and (obsY == pacmanY)):
					paredDerecha = True
				if((obsX == pacmanX) and (obsY == pacmanY+1)):
					paredArriba = True
				if((obsX == pacmanX) and (obsY == pacmanY-1)):
					paredAbajo = True


			if (actualAction == 0):
				print("Ciclo 0")
				if not(paredDerecha):
					nextAction = 2
				elif not(paredArriba):
					nextAction = 0
				elif not(paredIzquierda):
					nextAction = 3
				else:
					nextAction = 1

			elif (actualAction == 1):
				print("Ciclo 1")
				if not(paredIzquierda):
					nextAction = 3
				elif not(paredAbajo):
					nextAction = 1
				elif not(paredDerecha):
					nextAction = 2
				else:
					nextAction = 0

			elif (actualAction == 2):
				print("Ciclo 2")
				if not(paredAbajo):
					nextAction = 1
				elif not(paredDerecha):
					nextAction = 2
				elif not(paredArriba):
					nextAction = 0
				else:
					nextAction = 3

			elif (actualAction == 3):
				print("Ciclo 3")
				if not(paredArriba):
					nextAction = 0
				elif not(paredIzquierda):
					nextAction = 3
				elif not(paredAbajo):
					nextAction = 1
				else:
					nextAction = 2

			msg.action = nextAction
			actualAction = nextAction
			print(msg.action)
			pub.publish(msg.action)
			rate.sleep()

    except rospy.ServiceException as e:
		print ("Error!! Make sure pacman_world node is running", e)



if __name__ == '__main__':
    try:
        right_hand()
    except rospy.ROSInterruptException:
        pass