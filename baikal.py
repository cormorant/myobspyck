#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Описание старого формата Байкал
"""
import struct
import numpy as np
import datetime
import math


def stripnulls(s):
    """ очищает строку от символов пропуска и нулевых символов """
    #TODO: удалять цифры из строки станции (re.compile...)
    #s = s.split('\x00')[0] #???
    if not isinstance(s, str): return s
    for sym in ("\00", "\01", ".st"):
        s = s.replace(sym, "")
    return s.strip()


def get_time(to, unpack=False):
    """ Возвращаем вычисленное время из числа секунд. 'to' -- это Т0 (T нулевое) """
    # t0 - должно быть число
    hours, remainder = divmod(to, 3600)
    minutes, seconds = divmod(remainder, 60)
    if not unpack:# если нужно время
        microseconds, seconds = math.modf(seconds)
        microseconds *= 1e6 # multiple by 1mln seconds
        return datetime.time(*map(int, (hours, minutes, seconds, microseconds)))
    else:# если вернуть отдельно все значения
        return (hours, minutes, seconds)


#=== Главный заголовок файла (120 байт)
MainHeaderMap = (
    #name          type   start   default  end
    ("kan",         "h",    0,      3,      2),
    ("test",        "h",    2,      0,      4),
    ("vers",        "h",    4,      53,     6),
    ("day",         "h",    6,      1,      8),
    ("month",       "h",    8,      1,      10),
    ("year",        "h",    10,     1980,   12),
    ("satellit",    "h",    12,     0,      14),
    ("valid",       "H",    14,     0,      16),
    ("pri_synhr",   "h",    16,     0,      18),
    ("razr",        "h",    18,     24,     20),
    ("reserv_short","6h",   20,     0,      32),
    ("station",     "16s",  32,     "st",   48),
    ("dt",          "d",    48,     0.01,   56),
    ("to",          "d",    56,     0.0,    64),
    ("deltas",      "d",    64,     0.0,    72),
    ("latitude",    "d",    72,     0.0,    80),
    ("longitude",   "d",    80,     0.0,    88),
    ("reserv_doubl","2d",   88,     0.0,    104),
    ("reserv_long", "4I",   104,    0,      120),
)

ChannelHeaderMap = (
    #name           typ     size
    ("phis_nom",     "h",    2),#0 2
    ("reserv",       "3h",   6),#2-8
    ("name_chan",    "24s",  24),#8 32, stripnulls
    ("tip_dat",      "24s",  24),#32 56, stripnulls
    ("koef_chan",    "d",    8),#56 64
    ("calcfreq",     "d",    8),#64 72
)
# выбрать только нужные кортежи
#ShortMainHeaderMap = [i for i in MainHeaderMap if i[0] in
#    ['kan', 'day', 'month', 'year', "razr", 'station', 'dt', 'to']]

#TODO: use AttribDict from obspy
class MyDictClass(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
    def __getattr__(self, name):
        #try:
        v = self[name]
        #except KeyError:
        #    v = None
        return v


class BaikalFile(object):
    """ Полное описание файлов формата Байкал """
    def __init__(self, filename):
        self.filename = filename
        self.valid = self.is_baikal()
        # чтение файла
        if self.valid:
            main_header, channels, data = self.read()
            self.main_header = main_header
            self.channels = channels
            self.data = data

    def read(self):
        """ извлекаем информацию из файла """
        #try:
        with open(self.filename, 'rb') as _f:
            # читать главный заголовок
            data = _f.read(120)
            main_header = MyDictClass()
            for name, typ, start, _, end in MainHeaderMap:
                main_header[name] = struct.unpack(typ, data[start:end])[0]
            # поправим станцию
            main_header["station"] = stripnulls(main_header["station"])
            # неправильный год кое-где
            if main_header["year"] < 1900: main_header["year"] += 2000
            # channels headers (соотв количеству каналов в файле)
            channels = []
            # считать заголовки каналов
            for _ in range(main_header.kan):
                channel = MyDictClass()
                for _name, _typ, _size in ChannelHeaderMap:
                    value = struct.unpack(_typ, _f.read(_size))[0]
                    channel[_name] = stripnulls(value)
                channels += [channel]
            # считать область данных
            nkan = main_header.kan
            razr = main_header.razr
            # размер одного замера
            razm = 2 if razr==16 else 4
            # тип
            typ = "h" if razr==16 else "i"
            # dtype
            dtyp = np.int16 if razr==16 else np.int32
            a = np.fromstring(_f.read(), dtype=dtyp)
            # обрезать массив с конца пока он не делится на 3
            while len(a) % 3 != 0: a = a[:-1]
            # демультиплексируем
            data = a.reshape((len(a)/nkan, nkan)).T
            #
        return main_header, channels, data
    
    def is_baikal(self):
        """ является ли файлом формата Байкал """
        # проверка вдруг текстовый файл
        if self.filename[-3:].lower() == "prn": return
        # количество каналов
        try:
            with open(self.filename, 'rb') as _f:
                nkan = struct.unpack("h", _f.read(2))[0]
        except (struct.error, IOError), msg:
            print("Error in file %s with msg: %s" % (self.filename, msg))
            return
        # должно быть вразумительное число каналов
        if not nkan in range(1,7): return
        # если сюда дошло - все проверки выполнены
        return True

    def get_datetime(self):
        """ сформировать дату/время """
        date = datetime.date(
            self.main_header.year,
            self.main_header.month,
            self.main_header.day
        )
        time = get_time(self.main_header.to)
        #
        return datetime.datetime.combine(date, time)
