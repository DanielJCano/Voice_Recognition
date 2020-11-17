from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import pyttsx3
import pytz
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september","october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]
def homework(link):
    count = 0
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get(link)
    agree = driver.find_element_by_id("agree_button")
    agree.click()
    nombre = driver.find_element_by_name("user_id")
    nombre.send_keys("t023052")
    password = driver.find_element_by_name("password")
    password.send_keys("sscz70ic")
    password.send_keys(Keys.ENTER)
    try:
        Dis_Algo = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "[2020-2] B5 - DISEÑO")))
        Dis_Algo.click()
        Tarea_Dis_Algo_Hoy = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "blocklist::3-dueView:::::3-dueView_1")))
        if Tarea_Dis_Algo_Hoy:
            print("No hay tarea de Diseño de Algoritmos.")
            count += 1
        else:
            print("Tarea de Diseño de Algoritmos: ")
            print("\n" + Tarea_Dis_Algo_Hoy.text)
        driver.back()
        Estructura_Datos = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "ESTRUCTURA")))
        Estructura_Datos.click()
        Tarea_Estru_Datos = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "blocklist::3-dueView:::::3-dueView_1")))
        if Tarea_Estru_Datos:
            print("\nNo hay tarea de Estructura de Datos.")
            count += 1
        else:
            print("Tarea de Estructura de Datos: ")
            print("\n" + Tarea_Estru_Datos.text)
        driver.back()
        Electronica_Digital = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "ELECTRONICA ")))
        Electronica_Digital.click()
        Tarea_Electro_Digi = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "blocklist::3-dueView:::::3-dueView_1")))
        if Tarea_Electro_Digi:
            print("\nNo hay Tarea de Electronica Digital II. ")
            count += 1
        else:
            print("\nTarea de Electronica Digital II: ", "\n" + Tarea_Electro_Digi.text)
        driver.back()
        Ecuaciones = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "20-2 ")))
        Ecuaciones.click()
        Tarea_Ecuaciones = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "blocklist::3-dueView:::::3-dueView_1")))
        if Tarea_Ecuaciones:
            print("\nNo hay Tarea de Ecuaciones Diferenciales. ")
            count += 1
        else:
            print("\nTarea de Ecuaciones Diferenciales: ", "\n" + Tarea_Ecuaciones.text)
    except:
        driver.quit()
    if count == 4:
        driver.quit()
        return "there is no homework"


def Weather():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.accuweather.com/en/mx/tijuana/241912/weather-forecast/241912")
    w = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "temp")))
    return w.text


def speak(text):                                    # Traduce el texto escrito en a audio
    engine = pyttsx3.init()                         # Esto nomas empieza a pyttsx3
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)                                # aqui procesa el texto a audio
    engine.runAndWait()                             # corre y espera que todo el texto se haya dicho

def get_audio():                                    # Esta funcion sirve para captar el audio del usuario.
    r = sr.Recognizer()
    with sr.Microphone() as source:                 # Manda a llamar el mic como fuente
        audio = r.listen(source)                    # aqui escucha lo que se dijo
        said = ""                                   # se crea un string vacio para sostener lo que se llego a decir como texto

        try:                                        # Ya capturando el audio en texto
            said = r.recognize_google(audio)        # Usa el API de google para reconocer lo que se dijo.
            print(said)                             # Mandamos a imprimir el texto de lo dicho para comprobar que esta bien
        except Exception as e:
            print("Exception: " + str(e))
    return said                                     # Se regresa el audio en texto para ser analizado.


def authenticate_google():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(day, service):
    date = datetime.datetime.combine(day, datetime.datetime.min.time())            # esto saca el tiempo minimo de un dia o sea 00:00
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())        # esto saca el tiempo maximo de un dia o sea 23:59
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isofromat(), timeMax = end_date,
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def get_date(text):                             # pasa lo dicho como "text"
    text = text.lower()                         # se pasa el texto a minusculas
    today = datetime.date.today()               # se agarra la fecha actual

    if text.count("today") > 0:                 # revisa si se ah dicho "today" en alguna parte del texto
        return today                            # si este es el caso se regresara la fecha de hoy

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():                   # si no se habla de hoy entonces buscara por palabras claves
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)          # se encuentra por ejemplo "5th" que "th" se encuentra en el indice 1
                if found > 0:                   # buscara lo que viene antes del "th" o sea el 5
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1: # si se encuentra un mes en el texto y es menor al mes en el que estamos, necesitamos agregar un año
        year = year + 1
    if day < today.day and month == -1 and day != -1:       # si llega a hablarse de un dia sin especificar el mes y el numero es menor al que se esta actualmente
        month = month + 1                               # tomara ese numero como el dia para el siguiente mes.
    if month == -1 and day == -1 and day_of_week != -1: # si nomas se llega a hablar de un dia de la semana como "jueves"
        current_day_of_week = today.weekday()           # checara el dia actual
        dif = day_of_week - current_day_of_week         # revisara la diferencia entre el dia actual y el dia dicho
        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7
        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return None

    return datetime.date(month = month, day = day, year = year)

def main():
        lock = True
        while lock == True:
            speak("hello, how can I help")
            print("Listening...")
            text = get_audio().lower()

            if "hello" in text:
                speak("Hello Daniel.")
                continue

            speak("okay, let me take a look")
            if "weather" in text:
                speak(Weather())
                continue

            elif "homework" in text:
                link = "https://cetys.blackboard.com/webapps/login/"
                h = homework(link)
                speak(h)
                continue
            elif "goodbye" in text:
                speak("goodbye, daniel")
                break
            else:
                try:
                    service = authenticate_google()
                    speak(get_events(get_date(text), service))
                except:
                    pass


if __name__ == '__main__':
    main()


