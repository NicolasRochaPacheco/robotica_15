#!/usr/bin/env python

#----------------------------------------------------------------------------------------------------------------------
#				CLASE PARA LANZAR EL THREAD DE MANEJO DEL TECLADO
#----------------------------------------------------------------------------------------------------------------------

from threading import Thread
from pynput.keyboard import Key, Listener


class Keyreader(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.num = 4
		print("Se ha lanzado el hilo para leer las teclas")

	def on_press(self, key):
		key = str(key)
		char = key.replace("u'", "")
		char = char.replace("'", "")
		if char == 'w':
			self.num = 0
		elif char == 's':
			self.num = 1
		elif char == 'a':
			self.num = 3
		elif char == 'd':
			self.num = 2

	def on_release(self, key):
		if key == Key.esc:
			return False
		else:
			self.num = 4

	def getNumber(self):
		return self.num

	def run(self):
		with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
				listener.join()


# Test script
# key = keyreader()
# key.start()
#
# while True:
#	num = key.getNumber()
#	print(num)