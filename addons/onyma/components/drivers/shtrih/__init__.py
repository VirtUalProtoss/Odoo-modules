# -*- coding: utf-8 -*-

__author__ = 'virtual'

import time
from datetime import date, datetime


def fill_row(str_left, str_right, max_length=40, filler='.', margin_left=2):
    str_left = str_left.decode('utf-8')
    str_right = str_right.decode('utf-8')
    filler = filler.decode('utf-8')

    lmax_length = (max_length - margin_left - len(str_right))
    nstr = []
    sym_count = len(str_left)
    while sym_count > lmax_length:
        astr = str_left[:lmax_length].strip()
        nstr.append(astr.encode('utf-8'))
        str_left = str_left[lmax_length:].strip()
        sym_count -= len(astr)

    flen = max_length - len(str_left) - margin_left - len(str_right)
    nstr.append((str_left + filler*flen + str_right).encode('utf-8'))
    print nstr
    return nstr

def get_norm_text(text, max_length=40):
    if type(text) == str:
        text = text.decode('utf-8')
    else:
        text = str(text).decode('utf-8')

    if len(text) > max_length:
        text = text[:max_length]

    n_text = text + u' '*(max_length-len(text))
    n_text = n_text.encode('cp1251')
    return n_text


class Shtrih(object):

    connObj = None # RS-232 connection object

    N = -1
    message = {
        0: 'Признак начала сообщения STX',
        1: 'Длина сообщения - двоичное число (не включаются байты 0, 1, LRC',
        2: 'Код команды или ответа - двоичное число',
        3-(N+1): 'Параметры, зависящие от команды (могут отсутствовать)',
        N+2: 'Контрольная сумма сообщения - байт LRC (поразрядный XOR всех байтов кроме 0)',
    }

    ACK = 0x6
    NAK = 0x15
    STX = 0x2
    ENQ = 0x5

    msg_bytes = {
        'ENQ': 0x05,
        'ACK': 0x06,
        'NAK': 0x15,
        'STX': 0x02,
    }

    operator_password = None
    retr_timeout = 50

    commands = {
        0: {
            'code': 0x01,
            'timeout': 50,
        },
        13: {
            'code': 0x0d,
            'timeout': 50000,
            'name': 'Фискализация (перерегистрация)',
        },
        16: {
            'code': 0x10,
            'timeout': 5000,
            'name': 'Короткий запрос состояния ФР',
        },
        17: {
            'code': 0x11,
            'timeout': 5000,
            'name': 'Запрос состояния ФР',
        },
        18: {
            'code': 0x12,
            'timeout': 2000,
            'name': 'Печать жирной строки',
        },
        19: {
            'code': 0x13,
            'timeout': 500,
            'name': 'Гудок',
        },
        22: {
            'code': 0x16,
            'timeout': 50000,
            'name': 'Технологическое обнуление',
        },
        23: {
            'code': 0x17,
            'timeout': 1500,
            'name': 'Печать строки',
        },
        24: {
            'code': 0x18,
            'timeout': 1500,
            'name': 'Печать заголовка документа',
        },
        30: {
            'code': 0x1e,
            'timeout': 5000,
            'name': 'Запись таблицы',
        },
        31: {
            'code': 0x1f,
            'timeout': 5000,
            'name': 'Чтение таблицы',
        },
        34: {
            'code': 0x22,
            'timeout': 500,
            'name': 'Программирование даты',
        },
        35: {
            'code': 0x23,
            'timeout': 500,
            'name': 'Подтверждение программирования даты',
        },
        36: {
            'code': 0x24,
            'timeout': 5000,
            'name': 'Инициализация таблиц начальными значениями',
        },
        37: {
            'code': 0x25,
            'timeout': 1500,
            'name': 'Отрезка чека',
        },
        39: {
            'code': 0x27,
            'timeout': 5000,
            'name': 'Общее гашение',
        },
        41: {
            'code': 0x29,
            'timeout': 500,
            'name': 'Протяжка',
        },
        47: {
            'code': 0x2f,
            'timeout': 500,
            'name': 'Печать строки данным шрифтом',
        },
        64: {
            'code': 0x40,
            'timeout': 5000,
            'name': 'Суточный отчет без гашения',
        },
        65: {
            'code': 0x41,
            'timeout': 5000,
            'name': 'Суточный отчет с гашением',
        },
        66: {
            'code': 0x42,
            'timeout': 5000,
            'name': 'Отчет по секциям',
        },
        67: {
            'code': 0x43,
            'timeout': 5000,
            'name': 'Отчет по налогам',
        },
        80: {
            'code': 0x50,
            'timeout': 500,
            'name': 'Внесение',
        },
        81: {
            'code': 0x51,
            'timeout': 500,
            'name': 'Выплата',
        },
        99: {
            'code': 0x63,
            'timeout': 50,
            'name': 'Запрос даты последней записи в ФП',
        },
        100: {
            'code': 0x64,
            'timeout': 50,
            'name': 'Запрос диапазона дат и смен',
        },
        128: {
            'code': 0x80,
            'timeout': 5000,
            'name': 'Продажа',
        },
        132: {
            'code': 0x84,
            'timeout': 5000,
            'name': 'Сторно',
        },
        133: {
            'code': 0x85,
            'timeout': 5000,
            'name': 'Закрытие чека',
        },

        134: {
            'code': 0x86,
            'timeout': 500,
            'name': 'Скидка',
        },

        135: {
            'code': 0x87,
            'timeout': 500,
            'name': 'Надбавка',
        },

        136: {
            'code': 0x88,
            'timeout': 1500,
            'name': 'Аннулирование чека',
        },


        137: {
            'code': 0x89,
            'timeout': 1500,
            'name': 'Подытог чека',
        },

        141: {
            'code': 0x8d,
            'timeout': 1500,
            'name': 'Открыть чек',
        },
        166: {
            'code': 0xa6,
            'timeout': 15000,
            'name': 'Контрольная лента из ЭКЛЗ по номеру смены',
        },
        168: {
            'code': 0xa8,
            'timeout': 5000,
            'name': 'Итог активизации ЭКЛЗ',
        },
        169: {
            'code': 0xa9,
            'timeout': 15000,
            'name': 'Активизация ЭКЛЗ',
        },
        170: {
            'code': 0xaa,
            'timeout': 5000,
            'name': 'Закрытие архива ЭКЛЗ',
        },
        171: {
            'code': 0xab,
            'timeout': 500,
            'name': 'Запрос регистрационного номера ЭКЛЗ',
        },
        172: {
            'code': 0xac,
            'timeout': 15000,
            'name': 'Прекращение ЭКЛЗ',
        },
        173: {
            'code': 0xad,
            'timeout': 5000,
            'name': 'Запрос состояния по коду 1 ЭКЛЗ',
        },
        174: {
            'code': 0xae,
            'timeout': 5000,
            'name': 'Запрос состояния по коду 2 ЭКЛЗ',
        },
        176: {
            'code': 0xb0,
            'timeout': 50,
            'name': 'Продолжение печати',
        },
        178: {
            'code': 0xb2,
            'timeout': 15000,
            'name': 'Инициализация архива ЭКЛЗ',
        },
        186: {
            'code': 0xba,
            'timeout': 5000,
            'name': 'Запрос в ЭКЛЗ итогов смены по номеру смены',
        },
        192: {
            'code': 0xc0,
            'timeout': 5000,
            'name': 'Загрузка графики',
        },
        193: {
            'code': 0xc1,
            'timeout': 5000,
            'name': 'Печать графики',
        },
        194: {
            'code': 0xc2,
            'timeout': 5000,
            'name': 'Печать штрих-кода',
        },
        195: {
            'code': 0xc3,
            'timeout': 5000,
            'name': 'Печать расширенной графики',
        },
        196: {
            'code': 0xc4,
            'timeout': 5000,
            'name': 'Загрузка расширенной графики',
        },
        197: {
            'code': 0xc5,
            'timeout': 5000,
            'name': 'Печать линии',
        },
    }

    error_codes = {
        -3: 'Нет подтверждения получения команды - нет связи',
        -2: '',
        -1: 'Нет связи',
        0: 'Ошибок нет',
        51: 'Некорректные параметры в команде',
        55: 'Команда не поддерживается в данной реализации ФР',
        74: 'Открыт чек, операция невозможна',
        78: 'Смена превысила 24 часа',
        79: 'Неверный пароль',
        80: 'Идет печать предыдущей команды',

        88: 'Ожидание команды продолжения печати',
        93: 'Таблица не определена',
        97: 'Переполнение диапазона цены',
        115: 'Команда не поддерживается в данном режиме',
        126: 'Неверное значение в поле длины',
        162: 'ЭКЛЗ: Некорректный формат или параметр команды',
        163: 'Некорректное состояние ЭКЛЗ',
        196: 'Несовпадение номеров смен',
        176: 'ЭКЛЗ: Переполнение в параметре количество',
        178: 'ЭКЛЗ уже активизирована',
    }

    fr_modes = {
        0: 'Принтер в рабочем режиме',
        1: 'Выдача данных',
        2: 'Открытая смена, 24 часа не кончились',
        3: 'Открытая смена, 24 часа кончились',
        4: 'Закрытая смена',
        5: 'Блокировка по неправильному паролю налогового инспектора',
        6: 'Ожидание подтверждения ввода даты',
        7: 'Разрешение изменения положения десятичной точки',
        8: {
            'name': 'Открытый документ',
            'sub': {
                0: 'Продажа',
                1: 'Покупка',
                2: 'Возврат продажи',
                3: 'Возврат покупки',
            },
        },
        9: 'Режим разрешения технологического обнуления',
        10: 'Тестовый прогон',
        11: 'Печать полного фискального отчета',
        12: 'Печать отчета ЭКЛЗ',
        13: {
            'name': 'Работа с фискальным подкладным документом',
            'sub': {
                0: 'Продажа (открыт)',
                1: 'Покупка (открыт)',
                2: 'Возврат продажи (открыт)',
                3: 'Возврат покупки (открыт)',
            },
        },
        14: {
            'name':'Печать подкладного документа',
            'sub': {
                0: 'Ожидание загрузки',
                1: 'Загрузка и позиционирование',
                2: 'Позиционирование',
                3: 'Печать',
                4: 'Печать закончена',
                5: 'Выброс документа',
                6: 'Ожидание извлечения',
            },
        },
        15: 'Фискальный подкладной документ сформирован',
    }

    fr_sub_modes = {
        0: 'Бумага есть',
        1: 'Пассивное отсутствие бумаги',
        2: 'Активное отсутствие бумаги',
        3: 'После активного отсутствия бумаги',
        4: 'Фаза печати операции полных фискальных отчетов',
        5: 'Фаза печати операции',
    }
    ready = False
    sections = {
        0: '',
        1: 'Интернет',
        2: 'МР Спарк (местная, внз)',
        3: 'МР Спарк (мгмн)',
        4: 'Ростелеком зона',
        5: 'Ростелеком',
        6: 'Кубтелеком',
        7: 'Вымпелком',
    }

    mode = None
    submode = None
    error_code = 0

    def __init__(self, com_obj):
        self.connObj = com_obj
        self.test = True
        #self.init_connection()

    def init_connection(self, retr_time=10):
        if retr_time < 0:
            self.connObj.send(chr(self.ACK))
            self.connObj.send(chr(self.ENQ))
            return None
        self.connObj.send(chr(self.ENQ))
        result = self.connObj.recv(11000)
        if result:
            if len(result) == 1:
                #for el in result:
                r_byte = hex(ord(result[0]))
                if r_byte == hex(self.ACK):
                    # Готовит сообщение
                    print 'Prepare reply'
                    self.ready = False
                elif r_byte == hex(self.NAK):
                    # Ждет команд, готов к работе
                    print 'Ready to work'
                    self.ready = True
                else:
                    # Нет связи
                    print 'FR transmitting, wait'
                    self.ready = False
                    # ФР что-то передавал, обработать надо
                    reply = self.recv_message(50, retr_time-1, result)
                    if reply:
                        self.ready = True
                    else:
                        pass
            else:
                error_code = self.recv_message(50, retr_time-1, result)
                if error_code:
                    # Ошибка
                    print error_code, self.get_error_message(error_code)
                    self.connObj.send(chr(self.ACK))
                    self.connObj.send(chr(self.ENQ))
                    self.ready = True
                else:
                    self.ready = True
                #self.init_connection(retr_time-1)
        else:
            # Истек тайм-аут
            self.connObj.send(chr(self.ENQ))
            print 'Connection time-out'
            self.ready = False

    def xor_message(self, message):
        xor = 0 #ord(message[0])
        for i in message:
            xor ^= ord(i)

        return xor

    def get_command_code(self, cmd_code):

        return self.commands[cmd_code]['code']

    def summ_bytes(self, byte_arr):
        summ = 0
        for i in byte_arr:
            summ += ord(i)

        return summ

    def exec_command(self, code, cparams=[]):
        if not self.operator_password:
            return -1
        params = self.operator_password[:]
        if len(cparams) > 0:
            params.extend(cparams)

        result = self.recv_message(50)
        if result != 0:
            self.init_connection(3)

        if self.ready:
            return self.send_data(self.get_message_bytes(params, code))
        else:
            return False

    def read_table(self, table, row, column):
        params = []
        params.extend(self.num_to_rbytes(table, 1))
        params.extend(self.num_to_rbytes(row, 2))
        params.extend(self.num_to_rbytes(column, 1))
        return self.exec_command(31, params)

    def write_table(self, table, row, column, data):
        params = []
        params.extend(self.num_to_rbytes(table, 1))
        params.extend(self.num_to_rbytes(row, 2))
        params.extend(self.num_to_rbytes(column, 1))
        params.extend(data)
        return self.exec_command(30, params)

    def eklz_state_1(self):
        params = []
        self.exec_command(173, params)
        reply = self.message
        if reply and len(reply) > 1:
            data = {
                'error': ord(reply[0]),
                'summa': self.summ_bytes(reply[1:5]),
                'date': [ord(reply[8]), ord(reply[7]), ord(reply[6])],
                'time': [ord(reply[9]), ord(reply[10]), ],
                'kpk_number': self.summ_bytes(reply[10:15]),
                'eklz_number': self.summ_bytes(reply[16:20]),
                #'flags': bin(ord(reply[21])),
            }
            print data

    def eklz_state_2(self):
        params = []
        self.exec_command(174, params)
        reply = self.message
        if reply and len(reply) > 1:
            data = {
                'error': ord(reply[0]),
                'smena_num': self.summ_bytes(reply[1:2]),
                'summa_sell': self.summ_bytes(reply[3:8]),
                'summa_buy': self.summ_bytes(reply[10:15]),
                'summa_revert_sell': self.summ_bytes(reply[16:21]),
                'summa_revert_buy': self.summ_bytes(reply[22:27]),
            }
            print data

    def eklz_report(self, smena_num):
        params = []
        params.extend(self.num_to_rbytes(smena_num, 2))
        self.exec_command(186, params)
        reply = self.message
        if reply and len(reply) > 1:
            data = {
                'error': ord(reply[0]),
                'kkm_type': str(reply[1:17]),
            }
            print data


    def hexreverse(self, hex_data):
        nstr = str(hex_data)[2:]
        rhex = []

        while len(nstr) > 0:
            rhex.append(int(nstr[-2:], 16))
            nstr = nstr[:-2]

        return rhex

    def num_to_rbytes(self, value, length=4):
        if type(value) == float:
            part = str(value-round(value)).split('.')[1]
            plen = len(part)
            value = int(round(value))
            value = (value * int(('1' + '0'*plen))) + int(part)

        arr = self.hexreverse(hex(value))
        if len(arr) < length:
            arr.extend([0, ]*(length-len(arr)))
        return arr

    def get_message_bytes(self, message, cmd_code):
        msg_bytes = []
        if type(message) == str:
            for i in message:
                msg_bytes.append(chr(i))
        elif type(message) == list:
            for i in message:
                if type(i) == str:
                    val = chr(ord(i))
                else:
                    val = chr(i)
                msg_bytes.append(val)
        else:
            print 'Auchtung!', message
            msg_bytes.append(message)

        r_bytes = [
            chr(self.STX),
            chr(len(msg_bytes)+1),
            chr(self.get_command_code(cmd_code)),
        ]

        r_bytes.extend(msg_bytes)
        xor = 0
        for i in r_bytes[1:]:
            xor = xor ^ ord(i)

        r_bytes.append(chr(xor))
        return r_bytes

    def recv_message(self, timeout, tries=10, message=None):
        if tries < 0:
            return None

        if not message:
            result = self.connObj.recv(timeout)
        else:
            result = message

        print 'recv:', result
        if result:
            # Есть ответ
            if len(result) > 0:

                if len(result) == 1:
                    # Подтверждение принятия команды
                    r_byte = hex(ord(result[0]))
                    if r_byte == hex(self.ACK):
                        # Команда принята успешно, подтверждение
                        return 0
                    elif r_byte == hex(self.NAK):
                        # Ошибка интерфейса
                        # Посылаем ENQ для повторного запроса ответа
                        #self.connObj.send(hex(self.ENQ))
                        #return self.recv_message(11000, tries-1)
                        return -3
                    else:
                        # Прочие ответы ФР - данные в ответ на команду
                        return -2
                else:
                    # Ответ на команду
                    el = hex(ord(result[0]))
                    if el == hex(self.ACK):
                        # Ответ принят успешно, подтверждение
                        crc = self.xor_message(result[2:-1])
                        lrc = ord(result[-1])
                        if crc == lrc:
                            # Корректная КС
                            self.connObj.send(chr(self.ACK))
                            #print 'ACK'
                            # Только код ошибки
                            return self.process_message(result[2:-1])
                        else:
                            self.connObj.send(chr(self.NAK))
                            self.connObj.send(chr(self.ENQ))
                            #print 'NAK, ENQ'
                            return self.recv_message(11000, tries-1)
                    elif el == hex(self.NAK):
                        # Ошибка интерфейса
                        # Посылаем ENQ для повторного запроса ответа
                        #print 'ENQ'
                        self.connObj.send(hex(self.ENQ))
                        return self.recv_message(11000, tries-1)
                    else:
                        #print 'None'
                        return -1

            else:
                # Пустой ответ - ошибка?
                print 'No reply'
                return -1
        else:
            # Тай-аут ответа
            print 'Reply time-out'
            return -1

    def send_data(self, data, timeout=None):
        cmd = ord(data[2])
        if not timeout:
            timeout = self.commands[cmd]['timeout']
        b_timeout = 50
        sdata = ''
        if type(data) == list:
            for el in data:
                sdata +=  str(hex(ord(el)))[2:] + ' '
                #if not self.test:
                self.connObj.send(el)
                time.sleep(b_timeout/1000)
        else:
            self.connObj.send(data)
            time.sleep(b_timeout/1000)

        print 'Command:', self.commands[cmd]['name']
        print 'sent:', sdata
        result = self.recv_message(timeout)
        if result > 0:
            # Код ошибки ФР
            return result
        elif result == 0:
            # Нет ошибок, команда выполнена успешно
            return result
        elif result == -1:
            # нет связи
            return result
        elif result == -2:
            # Что-то странное
            return result
        elif result == -3:
            # Нет подтверждения получения команды - нет связи
            return result
        else:
            # Непонятно
            return result

    def get_error_message(self, code):
        msg = 'Error %d not implemented' % (code, )
        if code in self.error_codes:
            if code != 0:
                msg = self.error_codes[code]
            else:
                msg = 'Нет ошибок'

        return msg

    def process_message(self, msg_bytes):
        msg_len = ord(msg_bytes[0])
        cmd_code = ord(msg_bytes[1])
        error_code = ord(msg_bytes[2])
        msg = msg_bytes[3:]
        print self.get_error_message(error_code)

        self.error_code = error_code
        self.command = cmd_code
        self.message = msg
        return error_code

    def report_z(self):

        return self.exec_command(65)

    def report_x(self):
        result = self.exec_command(64)
        time.sleep(5)
        return result

    def roll_paper(self, rows, p_type=1):
        for row in range(0, rows):
            self.print_string(' ')

        params = []
        if p_type == 0: # Контрольная лента
            p_param = int('0b1', 2)
        elif p_type == 1: # Чековая лента
            p_param = int('0b10', 2)
        elif p_type == 2: # Подкладной документ
            p_param = int('0b100', 2)
        else:
            p_param = int('0b10', 2)
        params.extend([chr(p_param)])
        params.extend([rows, ])
        return self.exec_command(41, params)

    def get_status(self):
        reply = self.exec_command(16)
        if reply == 0:
            msg = self.message
            mode_byte = bin(ord(msg[4]))

            data = {
                'error_code': ord(msg[0]),
                'operator': ord(msg[1]),
                'flags': {'hi': bin(ord(msg[2])), 'lo': bin(ord(msg[3])), },
                'mode': {'status': str(int(mode_byte, 2) >> 4)[-4:], 'number': int(mode_byte[-5:], 2), },
                'submode': ord(msg[5]),
                'operations_l': ord(msg[6]),
                'error_fp': ord(msg[9]),
                'error_eklz': ord(msg[10]),
                'operations_h': ord(msg[11]),
            }
            self.mode = data['mode']['number']
            self.submode = data['submode']

    def beep(self):

        return self.exec_command(19)

    def sell(self, count, cost, section, text, vats=[0, 0, 0, 0, ]):
        params = []
        params.extend(self.num_to_rbytes(count, 5))
        params.extend(self.num_to_rbytes(cost, 5))
        params.extend(self.num_to_rbytes(section, 1))
        for vat in vats:
            params.extend(self.num_to_rbytes(vat, 1))
        params.extend(get_norm_text(text[:40]))
        return self.exec_command(128, params)

    def storno(self, count, cost, section, text, vats=[0, 0, 0, 0, ]):
        params = []
        params.extend(self.num_to_rbytes(count, 5))
        params.extend(self.num_to_rbytes(cost, 5))
        params.extend(self.num_to_rbytes(section, 1))
        for vat in vats:
            params.extend(self.num_to_rbytes(vat, 1))
        params.extend(get_norm_text(text[:40]))
        return self.exec_command(132, params)

    def check_open(self, doc_type):
        params = []
        params.extend(self.num_to_rbytes(doc_type, 1))
        return self.exec_command(141, params)

    def check_close(self, sums, text):
        params = []
        params.extend(self.num_to_rbytes(sums['pay1'], 5))
        params.extend(self.num_to_rbytes(sums['pay2'], 5)) # pay type 2
        params.extend(self.num_to_rbytes(sums['pay3'], 5)) # pay type 3
        params.extend(self.num_to_rbytes(sums['pay4'], 5)) # pay type 4
        params.extend(self.num_to_rbytes(sums['discount'], 2))
        params.extend(self.num_to_rbytes(sums['vat1'], 1)) # vat 1
        params.extend(self.num_to_rbytes(sums['vat2'], 1)) # vat 2
        params.extend(self.num_to_rbytes(sums['vat3'], 1)) # vat 3
        params.extend(self.num_to_rbytes(sums['vat4'], 1)) # vat 4
        params.extend(get_norm_text(text))

        return self.exec_command(133, params)

    def check_cancel(self):
        time.sleep(1)
        self.exec_command(136)

    def check_cut(self, full=True):
        params = []
        params.extend([int(full), ])
        return self.exec_command(37, params)

    def print_string(self, data, max_length=40):
        if self.test:
            print 'String:', data
        params = []
        params.extend([int('0b10', 2), ]) # flags
        params.extend(get_norm_text(data, max_length)) # text
        return self.exec_command(23, params)

    def print_string_font(self, data, font=1, max_length=40):
        if self.test:
            print 'String:', data
        params = []
        params.extend([int('0b10', 2), ]) # flags
        params.extend([font, ])
        params.extend(get_norm_text(data, max_length)) # text
        return self.exec_command(47, params)

    def print_header(self, header, doc_num):
        params = [] # password
        params.extend(get_norm_text(header, 30)) # text
        params.extend([doc_num, 0, ]) # text
        return self.exec_command(24, params)

    def print_line(self, data, retries=1):
        params = self.num_to_rbytes(retries, 2)
        params.extend(data)
        return self.exec_command(197, params)

    def print_g_line(self, line_from, line_to):
        params = [line_from, line_to, ]
        return self.exec_command(193, params)

    def load_g_line(self, line_num, data, ext=False):
        params = [line_num, ]
        params.extend(data)
        return self.exec_command(192, params)

    def load_image(self, file_path):

        pass

    def test_string(self, text=''):
        text = '123456 789 123456 345675786796784847356 54yv347' + str(0x2261)
        params = []
        params.extend([int('0b10', 2), ]) # flags
        params.extend(get_norm_text(text, 48)) # text
        params[-1] = int(0xf1)
        return self.exec_command(23, params)

    def test_check(self, data, pay_summa):
        str_length = 50
        '''
            Открыть чек:
            0 – продажа;
            1 – покупка;
            2 – возврат продажи;
            3 – возврат покупки
        '''
        self.print_g_line(1, 181)
        self.print_string(' ')
        self.print_string(' ')
        time.sleep(1)
        reply = self.check_open(0)
        #if not reply:
        #    return None
        time.sleep(2)


        self.print_string('Абонент: Иванов Иван Иванович', str_length)
        self.print_string('Лицевой счет: 233085689', str_length)
        self.print_string('Номер телефона: 671234', str_length)
        self.print_string('='*str_length, str_length)

        time.sleep(0.2)
        data = {
            0: {'section': 2, 'amount': 0.11, 'text': 'Абонентская плата за телефонную линию', 'count': 3, 'type': 'шт.', },
            1: {'section': 2, 'amount': 0.01, 'text': 'Абонентская плата за АОН',  'count': 2, 'type': 'шт.',},
            2: {'section': 2, 'amount': 0.02, 'text': 'Местные исходящие вызовы',  'count': 396, 'type': 'мин.',},
            3: {'section': 3, 'amount': 0.02, 'text': 'Международные вызовы',  'count': 7, 'type': 'мин.',},
            4: {'section': 4, 'amount': 0.03, 'text': 'Внутризоновые вызовы Ростелеком',  'count': 15, 'type': 'мин.',},
            5: {'section': 5, 'amount': 0.07, 'text': 'Междугородние вызовы Ростелеком',  'count': 5, 'type': 'мин.',},
        }

        summs = {'all': 0.0, }
        for el in data:
            section = data[el]['section']
            amount = data[el]['amount']
            count = 1
            text = data[el]['text'] + ', ' + str(data[el]['count']) + ' ' + data[el]['type']
            str_data = fill_row(self.sections[section] + ': ' + text, '  =  ' + str(amount), max_length=str_length, filler=' ')
            for row in str_data:
                self.print_string(row, str_length)

            if section not in summs:
                summs[section] = amount
            else:
                summs[section] += amount
            summs['all'] += amount

        self.print_string('='*str_length, str_length)
        count = 1
        for section in summs:
            time.sleep(0.2)
            if section == 'all':
                continue
            self.sell(count*1000, summs[section], section, self.sections[section])


        self.print_string('='*str_length, str_length)
        str_data = fill_row('Итого:',  '=' + str(summs['all']), max_length=26, filler=' ')

        for row in str_data:
            self.print_string_font(row, 2, 26)
        #self.print_string(' ')

        #self.roll_paper(5)
        #self.check_cut()

        for section in summs:
            time.sleep(0.2)
            if section == 'all':
                continue
            self.storno(count*1000, summs[section], section, self.sections[section])
            #self.storno(count*1000, summs[section], section, self.sections[section])

        if self.test:
            # Аннулируем чек
            return self.check_cancel()

        pay_summs = {
            'pay1': pay_summa,
            'pay2': 0,
            'pay3': 0,
            'pay4': 0,
            'discount': 0,
            'vat1': 0,
            'vat2': 0,
            'vat3': 0,
            'vat4': 0,
        }
        return self.check_close(pay_summs, 'ПРОДАНО')
        #self.check_cut()
