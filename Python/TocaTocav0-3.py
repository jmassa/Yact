import sys
import os
import time
from pynput import keyboard
from pynput.keyboard import Listener, Key
from playsound import playsound


logfilename = "key_log.txt"  # The file to write characters to
f = open ( logfilename, "w+")

# inicializacion de variables
# entradas directas del makey makey
# sp: 0 , w: 1, a: 2, s: 3, d: 4, f: 5, arr: 6, ab: 7, izq: 8, der: 9
n_preguntas = 9
n_elementos = 9
n_aciertos = [0,0,0,0,0,0,0,0,0,0]
n_fallas = [0,0,0,0,0,0,0,0,0,0]
elementosdisponibles = [["tomate","rojo","redonda","fruta"],["banana","amarillo","alargada","fruta"],["limon","amarillo","redonda","fruta"],
                        ["manzana","rojo","redonda","fruta"],["ajo","blanco","redonda","verdura "],["pera","amarillo","redonda","fruta"],
                        ["pepino","verde","alargada"],["zapallito","verde","redonda","verdura"],["batata","marron","alargada","verdura"],
                        ["zanahoria","naranja","alargada","verdura"]]

otros =  ["naranja","naranja","redonda","fruta"]                       
elementos = [0,1,2,3,4,5,6,7,8,9]
entradas = ["space","down","right","left","up","w","a","s","d","f"]
entradask = [Key.space,Key.down,Key.right,Key.left,Key.up]
ultima_respuesta_correcta = False
pregunta_actual = 0
elemento_pregunta_actual = 0
elemento_presionado = -1
preguntando = False

# escribe las teclas presionadas en el log filename
def log_tecla(key):
   if hasattr(key, 'char'):  # Write the character pressed if available
     f.write(key.char)
   elif key == Key.space:  # If space was pressed, write a space
       f.write(' ')
   elif key == Key.enter:  # If enter was pressed, write a new line
       f.write('\n')
   elif key == Key.tab:  # If tab was pressed, write a tab
       f.write('\t')
   else:  # If anything else was pressed, write [<key_name>]
        f.write('[' + key.name + ']')
# fin escribe las teclas presionadas en el log filename

def presiona_elemento(key):
    for k in entradas:
       if k==key:
         return 

def acierta(key):   
   global ultima_respuesta_correcta
   global preguntando
   n_aciertos[elemento_pregunta_actual] = n_aciertos[elemento_pregunta_actual] + 1
   ultima_respuesta_correcta = True
   preguntando = False
   playsound("muybien.mp3")      

def falla(key):
   global ultima_respuesta_correcta
   global preguntando
   n_fallas[elemento_pregunta_actual] = n_fallas[elemento_pregunta_actual] + 1
   ultima_respuesta_correcta = False
   playsound("pruebaotravez.mp3")   

# detecta la presión de cada tecla
def on_press(key):
    global ultima_respuesta_correcta        
    global f    
    global preguntando
    if not preguntando:
      return
    elemento_presionado = -1
    log_tecla(key)
    print (key)            
    #si la tecla presionada es una de las entradas y coincide con la
    #tecla asociada al elemento de la pregunta actual entonces
    #sumar aciertos a ese elemento, poner ultimarespuestacorrecta en true
    #si la tecla está en entradask o es un char de una de las entradas es una tecla válida   
    if key in entradask:
      elemento_presionado = entradask.index(key)   
      if ((elemento_pregunta_actual==entradask.index(key))):  
        acierta(key)     
      else:
        falla(key)
    else:
      if hasattr(key, 'char'):  
        elemento_presionado = entradas.index(key.char)   
        if (elemento_pregunta_actual==entradas.index(format(key.char))):
          acierta(key)     
        else:
          falla(key)     
      else:
          falla(key)     
    if key == Key.esc:  # If tab was pressed, write a tab
        print("saliendo")
        sys.exit(0)   
# fin detecta la presión de cada tecla    

# detecta cuando sueltan una tecla    
def on_release(key):
   global ultima_respuesta_correcta
   #print("Soltaron la tecla")
# fin detecta cuando sueltan una tecla    


f = open(logfilename, 'a')  # Open the file
# instala la función listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()  # Join the thread to the main thread
# fin instala la función listener

# Comienza el juego
playsound("holabienvenidosaljuegotocatoca.mp3")
n_preguntas = 10
for p in range(1, n_preguntas):
   ultima_respuesta_correcta = False
   pregunta_actual = p
   preguntando = True
   playsound("porfavortocaelelemento.mp3")
   elemento_pregunta_actual = p-1
   while (not ultima_respuesta_correcta):
     print (ultima_respuesta_correcta)
     playsound(elementosdisponibles[elemento_pregunta_actual][0] + ".mp3")
     time.sleep(5)

listener.stop()
playsound("felicitacionestucantidaddeaciertoses.mp3")
n_aciertostotales = sum(n_aciertos)
playsound(str(n_aciertostotales) + ".mp3")
f.close()  # Close the file
# fin Comienza el juego