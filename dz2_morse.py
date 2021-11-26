#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO                     # импортируем библиотеку по работе с GPIO
import sys, traceback                       # Импортируем библиотеки для обработки исключений

from time import sleep                      # Импортируем библиотеку для работы со временем

dotDelay = 0.2                               # Длительность точки по заданию 1 сек, но устанешь ждать
letters = {'a':'.-', 'b':'-...', 'c':'-.-.', 'd':'-..', 'e':'.', 'f':'..-.', 'g':'--.', 'h':'....', 'i':'..',
           'j':'.---', 'k':'-.-', 'l':'.-..', 'm':'--', 'n':'-.', 'o':'---', 'p':'.--.', 'q':'--.-', 'r':'.-.',
           's':'...', 't':'-', 'u':'..-', 'v':'...-', 'w':'.--', 'x':'-..-', 'y':'-.--', 'z':'--..',
           '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----'}


try:
    controlPin = 25                         # Управляющий пин светодиода
    checkWord = ''                          # Контрольное слово
    
    # === Инициализация пинов ===
    GPIO.setmode(GPIO.BCM)                  # Режим нумерации в BCM
    GPIO.setup(controlPin, GPIO.OUT, initial=0) # Управляющий пин в режим OUTPUT
    
    # Функция обработки буквы/цифры
    def flashSequence(sequence):
        global checkWord
        for letter in sequence:
            flashDotOrDash(letter)
        sleep(2*dotDelay)                   # Выдерживаем паузу после буквы/цифры
        checkWord = checkWord + '00'
        
    # Функция обработки точки или тире
    def flashDotOrDash(dotOrDash):
        global checkWord
        GPIO.output(controlPin, True)       # Зажигаем светодиод
        if dotOrDash == '.':
            sleep(dotDelay)                 # Выдерживаем точку
            checkWord = checkWord + '1'
        else:
            sleep(3*dotDelay)               # Выдерживаем тире
            checkWord = checkWord + '111'
        GPIO.output(controlPin, False)      # Гасим светодиод
        sleep(dotDelay)                     # Выдерживаем ноль
        checkWord = checkWord + '0'

    while True:                            # Бесконечный цикл запроса ввода
        checkWord = ''                     # Обнуляем Контрольное слово
        message = input("Введите сообщение: ").lower() 
        for ch in message:
            if ch in letters.keys():       # Проверка на наличие символа в словаре
                flashSequence(letters[ch]) # Обрабатываем знак Морзе
            elif ch == ' ':                # Если пробел
                sleep(4*dotDelay)          # Выдерживаем паузу после слова
                checkWord = checkWord + '0000'
            else:    
                print("Символ: " + ch + " не может быть использован!") # Выводим в консоль
                           
        print(checkWord)                   # Вывод контрольного слова
        





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