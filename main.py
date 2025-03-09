# version 0.1.5 стабильная, полная, попытка оптимизировать используя polling(interval = 1)
import psutil
import socket
import cv2
import os
import sys
import telebot
import pyautogui
import requests
from bs4 import BeautifulSoup
from telebot import types

sys.path.insert(1, 'D:\\MyProg\\Python\\MyProg\\TrapBot')

from procces import *


Path = "C:\\Users\\Astromik\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"

Thanks = ["спасибо", "спс"]


# Функция создания фото с камеры, отправки его и последующее удаление
def Photo(ID, text):
    global Path

    # Включаем первую камеру
    cap = cv2.VideoCapture(0)

    # "Прогреваем" камеру, чтобы снимок не был тёмным
    for i in range(30):
        cap.read()

    # Делаем снимок    
    ret, frame = cap.read()

    # Записываем в файл
    cv2.imwrite(Path + "cam.png", frame)   

    # Отключаем камеру 
    cap.release()
  
    # Открываем фото
    Img = open(Path + "cam.png", 'rb')
    
    # Отправляем фото
    bot.send_photo(ID, Img, text)

    # Закрываем и удаляем фото
    Img.close()
    os.remove(Path + "cam.png")


# Функция которая делает скриншот, отправляет его, а потом удаляет
def screenshot(ID, text):
    global Path

    screen = pyautogui.screenshot(Path + "screenshot.png")
    bot.send_photo(ID, screen, text)
    os.remove(Path + "screenshot.png")


# Функция которая возвращает долготу и широту
def Location():
    IP = requests.get('https://api.ipify.org?format=json').json()['ip']   # Сайт который возращает IP при заходе на него
        
    url = f'https://ipinfo.io/{IP}/json'
    
    response = requests.get(url)
    data = response.json().get("loc").split(",")

    Lat, Lon = data[0], data[1]

    return Lat, Lon, IP



# Функция проверки интернет соединения (Вернет True если инет есть)
def InternetCheck():
    try:
        socket.gethostbyaddr('www.google.com')
        return True
    except socket.gaierror:
        return False


# Убийство процесса по сообщению
def kill_process(message):
    # Проверяем, является ли введенное сообщение числом (PID)
    try:
        pid = int(message.text)  # Преобразуем введённое сообщение в число
        # Вызываем функцию kill_process с PID
        # Если функция kill_process принимает PID, то делаем вызов
        kill_proccess(pid)
        bot.send_message(message.chat.id, f"Процесс с PID {pid} был убит.")
    except ValueError:
        # Если введено не число, сообщаем об ошибке
        bot.send_message(message.chat.id, "Вы ввели не число. Попробуйте снова.")


# ФУНКЦИЯ БОТА #
def BOT():
    # Подключаем токен для отправки фото в телеграм бота #
    global bot
    bot = telebot.TeleBot('2059009950:AAGR961dnTNHYS6xVuQ_tsnLwqxqO90bru0')

        
    # Само сообщение и фото (отправка в бота) 

    # Текст который пишет бот при запуске ПК
    PC_name = str(socket.gethostname())
    Start_text = PC_name + " был запущен!"

    # Эта ID пользователя если что
    chatID = 806031974

    # Отправляем сообщение о запуске и запускаем функцию проверки сети
    Photo(chatID, Start_text)

    # Кнопки, кнопки, кнопки! (Реагируют в чате на команду /start)
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # Делаем кнопки
        button_turn_off = types.KeyboardButton("Выключить ПК")
        button_reboot = types.KeyboardButton("Перезагрузить ПК")
        button_make_screenshot = types.KeyboardButton("Сделать скриншот")
        button_make_screenshot_1 = types.KeyboardButton("Сделать повторное фото")
        button_send_location = types.KeyboardButton("Отправить местоположение")
        button_send_process = types.KeyboardButton("Отправить работающие процессы")
        button_kill_process = types.KeyboardButton("Убить процесс")
        # Вставляем кнопки
        markup.add(button_turn_off, button_reboot, button_make_screenshot, 
                   button_make_screenshot_1, button_send_location, button_send_process,
                   button_kill_process)
        bot.send_message(chatID, text = "Привет, {0.first_name}! Я бот ловушка для твоего ПК :)".format(message.from_user), reply_markup=markup)
    

    @bot.message_handler(func=lambda message: message.text.lower() == "убить процесс")
    def ask_pid(message):
        # Запрашиваем у пользователя ввод PID
        bot.send_message(chatID, "Введите PID процесса: (указывайте только те числа, которые видите)")
        # Регистрация следующего шага (ожидаем PID)
        bot.register_next_step_handler(message, kill_process)



    # Функция обработки введенного текста в боте
    @bot.message_handler(content_types=['text'])
    def func(message):

        # Команда отвечающая за выключенеи ПК
        if (message.text.lower() == "выключить пк"):
            try:
                bot.send_message(chatID, text = "Выключаю...")
                os.system("shutdown /p")
            except:
                bot.send_message(chatID, text = "По неизвестной причине не удалось выключить ПК")

        # Команда отвечает за перезагрузку ПК
        elif (message.text.lower() == "перезагрузить пк"):
            try:
                bot.send_message(chatID, text = "Перезагружаю...")
                os.system("shutdown -r -t 0")
            except:
                bot.send_message(chatID, text = "По неизвестной причине не удалось перезагрузить ПК")

        # Эта команда запускает функцию screenshot()
        elif (message.text.lower() == "сделать скриншот"):
            try:
                Repeated_screenshot_text = "Вот что он/она делает"
                screenshot(chatID, Repeated_screenshot_text)
            except:
                bot.send_message(chatID, text = "Не удалось сделать скриншот")
    
        # Эта повторно запускает функцию Photo()
        elif (message.text.lower() == "сделать повторное фото"):
            try:
                Repeated_text = "Вот он/она"
                Photo(chatID, Repeated_text)  
            except:
                bot.send_message(chatID, text = "Не удалось получить изображение")

        # Вычисляет местоположение по IP
        elif (message.text.lower() == "отправить местоположение"):
            try:
                bot.send_message(chatID, text = "Моё примерное, город указан точно")
                lat, lon, ip = Location()
                bot.send_location(chatID, lat, lon)
                bot.send_message(chatID, "IP: " + str(ip))
            except:
                bot.send_message(chatID, text = "Не удалось получить местоположение")

        # Отправляем список работающих процессов
        elif (message.text.lower() == "отправить работающие процессы"):
            try:
                bot.send_message(chatID, text = "Вот список работающих процессов:")
                bot.send_message(chatID, text = DictToString(monitor_processes()))
            except:
                bot.send_message(chatID, text = "Ошибка при получении процессов")

        # По фану
        elif (message.text.lower() in Thanks):
            bot.send_message(chatID, text = "Всегда пожалуйста)")

        # Ну и естественно защита от дурака)
        else:
            bot.send_message(chatID, text = "На такую комманду я не запрограммирован...")



    bot.polling(interval = 1)









BOT()