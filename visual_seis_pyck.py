#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
graphical search and editing events from database (postgres).
TOFIX:
 - ошибка с поиском по idDir при открытии окна в windows
TODO:
 - избавиться от сырых (raw) и сложных sql запросов, использовать sqlalchemy
 - использовать или array или numpy для чтения массивов данных
 - замена на более легковесную библиотеку вместо guiqwt
 - рисовать графики для каждого канала в отдельных связанных по оси х холстах (matplotlib)
 - сохранять настройки в файле ini
"""
APP_NAME = "visual_seis_pyck"
import os
import sys



try:
    import psycopg2
except ImportError:
    print("Database connection will not work. No psycopg2 package installed! Aborting.")
    sys.exit(1)

import numpy as np
import struct
import math






def main(results):
    # для каждой полученной строки...
    for line in e.results.splitlines():
        try:
            result = line.split()
            Dir = result[1].replace("\\", "/")
            # убрать из имени папки всё до seisobr (DATA_DIR)
            Dir = Dir[Dir.index(DATA_DIR):]
            # имя файла
            filename = os.path.join(Dir, result[2])
        except (IndexError, AttributeError), msg:
            print("Disaster! Cannot get filename from text:", msg)
            continue
        # получим значения из файлов
        baikal_data = read_baikal(filename)
        #
        if not baikal_data:
            print("Skipping file", filename)
            continue
        # unpack received tuple
        sampl_rate, t0, a, nkan = baikal_data
        #=== получить времена вступления волн P и S
        try:
            int(result[0])
        except (TypeError, ValueError, IndexError, msg):
            print("Error with waves parsing:", msg)
            waves = []
        else:
            waves = execute_query(SELECT_WAVES, [result[0]])
        #=== GRAPHIC PLOT, рисуем графику
        # передаём        данные/число каналов/дискретизация
        update = plot_graph(a, nkan, sampl_rate,
            t0, # время 1-й сек с поправками
            waves, # список полученных для события волн
            title=filename,
        )
        # если полученный список не пуст (изменены реперы), обновлять записи в бд
        if update:
            print("Have to update data on db!")
            for upd in update:
                print upd
                '''
                try:
                    cursor.execute(UPDATE_WAVES, upd)
                except psycopg2.Error, msg:
                    print("An error ocured while updating dataset:", msg)
                else:
                    conn.commit()
                '''


if __name__ == "__main__":
    #=== DB
    # connecting to database
    conn_string = "host='%(host)s' dbname='%(database)s' user='%(user)s' password='%(password)s'" % DB_OPTIONS
    try:
        conn = psycopg2.connect(conn_string)
    except psycopg2.OperationalError, msg:
        print("Error connecting to db:", msg)
        sys.exit(1)
    cursor = conn.cursor()
    #=== GUI
    #try:
    main(e.results)
    #! only in production mode!
    #except BaseException, msg:
    #    print("An error ocured. Error string is:", msg)
    # закрыть соединение с бд
    cursor.close()
