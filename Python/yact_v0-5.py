import sys
import os
import time
from pynput import keyboard
from pynput.keyboard import Listener, Key
from playsound import playsound
#import json
import csv
import random
import streamlit as st


st.title("Bienvenidos a yact")
st.markdown("Herramienta para estimulación cognitiva de adultos mayores")
st.header("Por favor, escuche la consigna")
st.markdown(">...")


logfilename = "yact_key_log.txt"  # The file to write characters to
f = open ( logfilename, "w+")


# arreglo para hacer mas eficiente la lectura en el juego, luego  será sobreescrito por el json
elementosdisponibles = [["tomate","rojo","redonda","fruta"],["banana","amarillo","alargada","fruta"],["limon","amarillo","redonda","fruta"],
                        ["manzana","rojo","redonda","fruta"],["ajo","blanco","redonda","verdura "],["pera","amarillo","redonda","fruta"],
                        ["pepino","verde","alargada","verdura"],["zapallito","verde","redonda","verdura"],["batata","marron","alargada","verdura"],
                        ["zanahoria","naranja","alargada","verdura"]]
# fin arreglo para hacer mas eficiente la lectura en el juego, luego  será sobreescrito por el json
with open('Yact_elementos.csv') as elementoscsv:
  csv_reader = csv.reader(elementoscsv,delimiter=',')
  line_count = 0
  for row in csv_reader:   
      if line_count!=0:
           print(elementosdisponibles[line_count])
           elementosdisponibles[line_count][0] = row[1]
           elementosdisponibles[line_count][1] = row[2]
           elementosdisponibles[line_count][2] = row[3]
           elementosdisponibles[line_count][3] = row[4]
           line_count += 1

with open('Yact_parametros.csv') as parametroscsv:
  csv_reader = csv.reader(parametroscsv,delimiter=',')  
  fila = 0;
  for row in csv_reader:
    if fila==0:
       n_elementos = int(row[1])
    if fila==1:   
       n_preguntas = int(row[1])
    fila = fila + 1     
print (n_elementos)
print (n_preguntas)

'''
#Escritura de json template con elementos
if not os.path.exists("elementos.json"):
  lista = {}
  lista['elementos'] = []
  lista['elementos'].append({'nombre': 'tomate', 'color': 'rojo', 'forma': 'redonda', 'tipo': 'fruta'})
  lista['elementos'].append({'nombre': 'banana', 'color': 'amarillo', 'forma': 'alargada', 'tipo': 'fruta'})
  lista['elementos'].append({'nombre': 'limon', 'color': 'amarillo', 'forma': 'redonda', 'tipo': 'fruta'})
  lista['elementos'].append({'nombre': 'manzana', 'color': 'rojo', 'forma': 'redonda', 'tipo': 'fruta'})
  lista['elementos'].append({'nombre': 'ajo', 'color': 'blanco', 'forma': 'redonda', 'tipo': 'verdura'})
  lista['elementos'].append({'nombre': 'pera', 'color': 'amarillo', 'forma': 'redonda', 'tipo': 'fruta'})
  lista['elementos'].append({'nombre': 'pepino', 'color': 'verde', 'forma': 'alargada', 'tipo': 'verdura'})
  lista['elementos'].append({'nombre': 'zapallito', 'color': 'verde', 'forma': 'redonda', 'tipo': 'verdura'})
  lista['elementos'].append({'nombre': 'batata', 'color': 'marron', 'forma': 'alargada', 'tipo': 'verdura'})
  lista['elementos'].append({'nombre': 'zanahoria', 'color': 'naranja', 'forma': 'alargada', 'tipo': 'verdura'})  
  with open('elementos.json', 'w') as file:
     json.dump(lista, file, indent=4)
#Fin Escritura de json template con elementos

#Escritura de json template con parametros
if not os.path.exists("parametros.json"):
  parametros = {}
  parametros['parametros'] = []
  parametros['parametros'].append({'cantidad preguntas': 9, 'cantidad elementos': 9})
  with open('parametros.json', 'w') as file:
     json.dump(parametros, file, indent=4)
#Fin Escritura de json template con parametros

# comienzo lectura del json con elementos
with open('elementos.json') as file:
    listaelementos = json.load(file)   
for elemento in listaelementos['elementos']:        
        print('nombre:', elemento['nombre'])
        print('color:', elemento['color'])
        print('forma:', elemento['forma'])
        print('tipo:', elemento['tipo'])
        print('')
# fin lectura del json con elementos

# comienzo lectura del json con parametros
with open('parametros.json') as file:
    parametros = json.load(file)   
n_preguntas = parametros['parametros'][0]['cantidad preguntas']
n_elementos = parametros['parametros'][0]['cantidad elementos']
# fin lectura del json con elementos
'''

'''
# Carga del diccionario json en un arreglo por cuestiones de eficiencia
aux = 0
#print (listaelementos["elementos"][1])
for elem in listaelementos["elementos"]:
  elementosdisponibles[aux][0] = elem["nombre"]
  elementosdisponibles[aux][1] = elem["color"]
  elementosdisponibles[aux][2] = elem["forma"]
  elementosdisponibles[aux][3] = elem["tipo"]
  aux = aux + 1
# Fin Carga del diccionario json en un arreglo por cuestiones de eficiencia
'''


'''
# está comentado porque por ahora las entradas siguen fijas

#Escritura de json template con entraddas
if not os.path.exists("entradas.json"):
  entra = {}
  entra['entradas'] = []
  entra['entradas'].append({  "space": 0, "down": 1, "right": 2, "left": 3, "up": 4, "w": 5,    "a": 6,
            "s": 7, "d": 8, "f": 9})
  with open('entradas.json', 'w') as file:
     json.dump(entra, file, indent=4)
#Fin Escritura de json template con entradas

# comienzo lectura del json con entradas
with open('parametros.json') as file:
    parametros = json.load(file)   
n_preguntas = parametros['parametros'][0]['cantidad preguntas']
n_elementos = parametros['parametros'][0]['cantidad elementos']
# fin lectura del json con entradas
'''


# inicializacion de variables
# entradas directas del makey makey
# sp: 0 , w: 1, a: 2, s: 3, d: 4, f: 5, arr: 6, ab: 7, izq: 8, der: 9
n_aciertos = [0,0,0,0,0,0,0,0,0,0]
n_fallas = [0,0,0,0,0,0,0,0,0,0]

# impresion de elementos y configuracion
print ("Elementos disponibles: ", elementosdisponibles)
print ("Cantidad de preguntas: ", n_preguntas)
print ("Cantidad de elementos: ", n_elementos)
# fin impresion de elementos y configuracion

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
    if key == Key.esc:  # If esc was pressed, exit
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
preguntas = []
preguntas = random.sample(range(1,n_elementos+1),n_preguntas)
print (preguntas)
for p in range(1, n_preguntas+1):
   ultima_respuesta_correcta = False
   pregunta_actual = preguntas[p-1]
   print ("pregunta_actual: ",pregunta_actual)
   #pregunta_actual = p // para testear recorriendo pregunta por pregunta en orden
   preguntando = True
   playsound("porfavortocaelelemento.mp3")
   elemento_pregunta_actual = pregunta_actual-1
   print ("elemento_pregunta_actual: ",elemento_pregunta_actual)
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

