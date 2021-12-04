#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO                     # импортируем библиотеку по работе с GPIO
import sys, traceback                       # Импортируем библиотеки для обработки исключений
import paho.mqtt.client as mqtt

from time import sleep                      # Импортируем библиотеку для работы со временем

# Данные для MQTT брокера
brokerHost = "localhost"
brokerPort = 1883
clientID = "TestMQTT"
clientLogin = "login"
clientPswd = "password"
publishTopic = "connect"
publishMsg = "Raspberry is connected!"
subTopic = "led/single"

try:
    controlPin = 25                         # Управляющий пин светодиода
    
    # === Инициализация пинов ===
    GPIO.setmode(GPIO.BCM)                  # Режим нумерации в BCM
    GPIO.setup(controlPin, GPIO.OUT, initial=0) # Управляющий пин в режим OUTPUT
      
    # Функция зажигания на 1 сек
    def flashLed():
        GPIO.output(controlPin, True)       # Зажигаем светодиод
        sleep(1)                            # Выдерживаем 1 сек
        GPIO.output(controlPin, False)      # Гасим светодиод

    # Функции для MQTT клиента
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        if rc == 0:
            client.publish(publishTopic, publishMsg, 1)
            client.subscribe(subTopic)
        
    def on_disconnect(client, userdata, rc):
        print("Unexpected disconnection")
    
    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        print("Message: " + message)
        flashLed()
        
    
    # Запускаем MQTT клиента
    client = mqtt.Client(client_id = clientID)
    
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set(username=clientLogin, password=clientPswd)
    print("Connecting...")
    client.connect(brokerHost, brokerPort, 60)

    client.loop_forever()


except KeyboardInterrupt:
    # ...
    print("Exit pressed Ctrl+C")            # Выход из программы по нажатию Ctrl+C
except:
    # ...
    print("Other Exception")                # Прочие исключения
    print("--- Start Exception Data:")
    traceback.print_exc(limit=2, file=sys.stdout) # Подробности исключения через traceback
    print("--- End Exception Data:")
finally:
    print("CleanUp")                        # Информируем о сбросе пинов
    GPIO.cleanup()                          # Возвращаем пины в исходное состояние
    print("End of program")                 # Информируем о завершении работы программы