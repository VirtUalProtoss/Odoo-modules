# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ..shtrih import Shtrih
import sys, serial, os, time, traceback
from binascii import b2a_hex, a2b_hex
from struct import pack, unpack, calcsize

ACK = '\x06'
NAK = '\x15'
STX = '\x02'
ENQ = '\x05'
PORT = '/dev/ttyS4'  # '/dev/ttyUSB0'
BAUDRATE = 9600
PASSWORD = 30  # Пароль админа по умолчанию = 30, Пароль кассира по умолчанию = 1
LASTRESPONS = None
REGKASSIR = False

resultKKM = {
    '0000': u'OK',
    '0001': u'Неисправен накопитель ФП 1, ФП 2 или часы',
    '0002': u'Отсутствует ФП 1',
    '0003': u'Отсутствует ФП 2',
    '0004': u'Некорректные параметры в команде обращения к ФП',
    '0005': u'Нет запрошенных данных',
    '0006': u'ФП в режиме вывода данных',
    '0007': u'Некорректные параметры в команде для данной реализации ФП',
    '0008': u'Команда не поддерживается в данной реализации ФП',
    '0009': u'Некорректная длина команды',
    '000A': u'Формат данных не BCD',

    '0033': u'Некорректные параметры в команде',

    '0037': u'Команда не поддерживается в данной реализации ФР',

    '0040': u'Переполнение диапазона скидок',

    '0045': u'Cумма всех типов оплаты меньше итога чека',

    '004a': u'Открыт чек – операция невозможна',
    '004b': u'Буфер чека переполнен',

    '004e': u'Смена превысила 24 часа',

    '0050': u'Идет печать предыдущей команды',

    '0058': u'Ожидание команды продолжения печати',

    '005e': u'Некорректная операция',

    '0056': u'Нет документа для повтора',

    '006b': u'Нет чековой ленты',

    '0072': u'Команда не поддерживается в данном подрежиме',
    '0073': u'Команда не поддерживается в данном режиме',
}

def lrc2(data, lenData=None):
    """Подсчет CRC"""
    result = 0
    if lenData is None:
        lenData = len(data)
    result = result ^ lenData
    for c in data:
        result = result ^ ord(c)
    return chr(result)

def readA(ser):
    fg = True
    data = None  # нет связи
    while fg:
        fg = False
        ser.write(ENQ)
        ch = ser.read(1)
        if '\x06' == ch:
            # print 'ACK'  # Получаем ответ от ФР
            stx = ser.read(1)
            lenCmd = ser.read(1)
            data = ser.read(ord(lenCmd))
            crc = ser.read(1)
            if crc == lrc2(data):
                ser.write(ACK)
            else:
                ser.write(NAK)
        elif '\x15' == ch:
            data = ''
            # print 'NAK'
        elif '' <> ch:  # Ожидаем конца передачи от ФР
            fg = True
            ch = '.'
            while ch:
                ch = ser.read(1)
    return data

def sendMsg(ser, cmd):
    lenCmd = len(cmd)
    crc = lrc2(cmd, lenCmd)
    ser.write(STX)
    ser.write(chr(lenCmd))
    ser.write(cmd)
    ser.write(crc)
    ser.flush()

def sendCmd(cmd, fmtA='', ser=None, port=None, passwd=PASSWORD):
    global LASTRESPONS, REGKASSIR, PORT, BAUDRATE
    if port is None:
        port = PORT
    r = []

    fgClose = False
    try:
        if ser is None:
            fgClose = True
            ser = serial.Serial(port, BAUDRATE, timeout=1)
        data = readA(ser)
        #~ if not REGKASSIR:
            #~ # Вычитываем ответ предыдущий команды
            #~ data = readA(ser)
            #~ REGKASSIR = True
        fg = data is not None
        while fg:
            fg = False
            #print 'Посылаем команду', cmd
            sendMsg(ser, cmd)
            #print 'Вычитываем ответ'
            data = readA(ser)
            arr = []
            #for el in data:
            #    arr.append(hex(ord(el)))
            #print 'ERX', arr
            #print 'hexxxx', b2a_hex(data[2:]), type(data[2:])

            if data:
                cmdA = b2a_hex(data[0])
                err = '00%s' % b2a_hex(data[1])
                if '0000' == err:
                    if fmtA:
                        if fmtA:
                            LASTRESPONS = cmdA, err, b2a_hex(data[2:])
                        else:
                            LASTRESPONS = cmdA, err, list(unpack(fmtA, data[2:]))
                    else:
                        LASTRESPONS = cmdA, err, None
                elif '0050' == err:  # Идет печать предыдущей команды
                    fg = True
                    LASTRESPONS = cmdA, err, None
                    time.sleep(0.25)
                elif '0058' == err:  # Ожидание команды продолжения печати
                    fg = True
                    LASTRESPONS = cmdA, err, None
                    time.sleep(0.25)
                    sendMsg(ser, pack('<Bi', 0xB0, passwd))
                    data = readA(ser)
                else:
                    LASTRESPONS = cmdA, err, None
        if data is None:
            r = (-1, u'нет связи')
        else:
            r = (0, 'OK')
    except Exception, e:
        LASTRESPONS = None
        r = (-1, str(e))
    finally:
        if fgClose and ser:
            ser.close()
    return r

def getRespons(filename=None, data=None):
    global LASTRESPONS
    # Ответ для анализа
    if data:
        r = data
        LASTRESPONS = r
    elif filename:
        with open(filename, 'rb') as f:
            r = f.read()
        LASTRESPONS = r
    else:
        r = LASTRESPONS

    try:
        respons_cmd = r[1]
    except Exception, e:
        respons_cmd = None

    if respons_cmd:
        return respons_cmd, resultKKM.get(respons_cmd, respons_cmd)  # результат выполнения команды
    else:
        return -1, u'нет связи'

def beep(ser=None, passwd=PASSWORD):
    """Команда: Гудок
        13H. Длина сообщения: 5 байт.
        • Пароль оператора (4 байта)
        Ответ:
        13H. Длина сообщения: 3 байта.
        • Код ошибки (1 байт)
        • Порядковый номер оператора (1 байт) 1...30
    """
    cmd = pack('<bi', 0x13, passwd)
    fmtA = '<B'

    #return execCmd(ser, cmd, fmtA)

    global LASTRESPONS
    rr = None
    try:
        rr = sendCmd(cmd, fmtA, ser)
        if 0 == rr[0]:
            rr = getRespons()
            #if '0000' == rr[0]:
            #    r = LASTRESPONS[2]
    except:
        rr = None
    return rr


class ShtrihM(Shtrih):

    def __init__(self):
        Shtrih.__init__(self)
