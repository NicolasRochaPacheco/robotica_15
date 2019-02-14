# robotica_15
Repositorio oficial de los miembros del grupo 15 del curso de "Robótica" de la Universidad de Los Andes 
En este paquete se encuentra implementado el Taller 1: Introducción a ROS.

Para correrlo se deben ejecutar los siguientes comandos en la terminal:
En todos los puntos se debe iniciar el ROSCORE:
     $ roscore
     
Punto 1:
     $ rosrun pacman pacman_world --c "mapa"
     $ rosrun controller_15 punto1.py
     
Punto 2:
     $ rosrun pacman pacman_world --c "mapa"
     $ rosrun controller_15 punto2.py
       
Adicionalmente, también puede correrse en modo de juego --g o en conjunto con otros nodos. para ver la actualización y cambio de los elementos en la terminal. 
        
Punto 3:
     $ rosrun pacman pacman_world --c "mapa"
     $ rosrun controller_15 punto3.py

Punto 4:
     $ rosrun pacman pacman_world --c mediumCorners
     $ rosrun controller_15 punto4.py

Punto 5:
     $ rosrun pacman pacman_world --c newPacman
     $ rosrun controller_15 punto5_1.py
     $ rosrun controller_15 punto5_2.py

Para información detallada de cada uno de los puntos (la planeación de la solución, la implementación en código, los resultados y el analisis) puede referise a la documentación oficial en la carpeta resultados (Taller1_results.pdf). 


