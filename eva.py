import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import numpy as np
import cv2 
import chistesESP as chistes
import random


engine = pyttsx3.init()
engine.say("Hola, yo soy eva tu asistente virtual")
engine.runAndWait()


# Nos indica cuando tomar la foto
foto = True
# nombre de nuestro asistente virtual
name = 'eva'
# Bandera para saber si termino el programa
encendido = 1

listener = sr.Recognizer()

engine = pyttsx3.init()

"""RATE DEL ASISTENTE"""
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)

"""VOZ DEL ASISTENTE"""
voice_engine = engine.getProperty('voices')
engine.setProperty('voice', voice_engine[0].id)

# Selecciona una palabra de forma aleatoria
def frase():
    lista = ['Te escucho', 'Dime tu orden', 'Estoy escuchándote', 'Dime','En que te ayudo?']
    seleccion = random.choice(lista)
    return seleccion

def talk(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print('Error en 01: ')
        print(e)
        pass

def listen():
    try:
        with sr.Microphone() as source:
            select = frase()
            print('Escuchando...')
            talk(select)
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language='es-ES')
            rec = rec.lower()
            print('Reconocido: ' + rec)
            if name in rec:
                rec = rec.replace(name, '')
                rec = rec.replace('hola', '')
                print(rec)
                comandos(rec)
    except Exception as e:
        print('Error en 02: ')
        print(e)
        pass

def tomarFoto():
    #Vamos a capturar el objeto que queremos identificar
        cap = cv2.VideoCapture(0)              # Elegimos la camara con la que vamos a hacer la deteccion
        while(foto):
            ret,frame = cap.read()             # Leemos el video
            cv2.imshow('Deteccion',frame)         # Mostramos el video en pantalla
        cv2.imwrite('Deteccion.jpg',frame)       # Guardamos la ultima caputra del video como imagen
        cap.release()                         # Cerramos
        cv2.destroyAllWindows()
        talk("Foto tomada")

        
def comandos(rec):
    print("Ejecutando...")
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Reproduciendo ' + music)
        pywhatkit.playonyt(music)
        print('termino ' + music)
    elif 'hora' in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk("Son las " + hora)
    elif 'busca' in rec:
        order = rec.replace('busca', '')
        wikipedia.set_lang("es")
        info = wikipedia.summary(order, 1)
        talk(info)
    elif 'foto' in rec:
        #Vamos a capturar el objeto que queremos identificar
        cap = cv2.VideoCapture(0)              # Elegimos la camara con la que vamos a hacer la deteccion
        while(True):
            ret,frame = cap.read()             # Leemos el video
            cv2.imshow('Objeto',frame)         # Mostramos el video en pantalla
            if cv2.waitKey(1) == 27:           # Cuando oprimamos "Escape" rompe el video
                break
        cv2.imwrite('objeto.jpg',frame)       # Guardamos la ultima caputra del video como imagen
        cap.release()                         # Cerramos
        cv2.destroyAllWindows()

        #Leemos la imagen del objeto que queremos identificar
        obj = cv2.imread('objeto.jpg',0)      # Leemos la imagen
        recorte = obj[160:300, 230:380]       # Recortamos la imagen para que quede solo el objeto (fila:fila, colum:colum)
        cv2.imshow('objeto',recorte)          # Mostramos en pantalla el objeto a reconocer

        #Una vez tenemos el objeto definido tomamos la foto con el resto de objetos
        cap = cv2.VideoCapture(0)                 # Elegimos la camara con la que vamos a hacer la deteccion
        while(True):
            ret2,frame2 = cap.read()              # Leemos el video
            cv2.imshow('Deteccion',frame2)        # Mostramos el video en pantalla
            if cv2.waitKey(1) == 27:              # Cuando oprimamos "Escape" rompe el video
                break
        cv2.imwrite('Deteccion.jpg',frame2)       # Guardamos la ultima caputra del video como imagen
        cap.release()                             # Cerramos
        cv2.destroyAllWindows()

        #Mostramos la imagen con todos los objetos
        img = cv2.imread('Deteccion.jpg',3)
        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Pasamos la imagen a escala de grises
        cv2.imshow('Deteccion',img)

        #Empezamos el algoritmo
        w, h = recorte.shape[::-1]                                           # Extraemos el ancho y el alto del recorte del objeto
        deteccion  = cv2.matchTemplate(gris, recorte, cv2.TM_CCOEFF_NORMED)  # Realizamos la deteccion por patrones
        umbral = 0.75                                                        # Asignamos un umbral para filtrar objetos parecidos
        ubi = np.where(deteccion >= umbral)                                  # La ubicacion de los objetos la vamos a guardar cuando supere el umbral
        for pt in zip (*ubi[::-1]):                                          # Creamos un for para dibujar todos los rectangulos
            cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (255,0,0), 1)         # Dibujamos los n rectangulos que hayamos identificado con el tamaño del recorte y de color

        cv2.imshow('Deteccion 1',img)
        foto=True
    elif 'exit' in rec:
        encendido = 0
        talk("Saliendo...")
    elif "saludos" in rec:
        talk("Hola, que tal, yo soy eva tu asistente virtual")
    elif 'chiste' in rec:
        chiste = chistes.get_random_chiste()
        talk(chiste)
    else:
        talk("Vuelve a intentarlo, no reconozco comando: " + rec)

while encendido:
    listen()
    print("Corriendo...")
    
    
print('algo paso')