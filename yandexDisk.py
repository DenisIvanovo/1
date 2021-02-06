"""
Скрипт написан для автоматизации создания резервной копии важных файлов,
Файлы архивируются  для удобства в zip-архив,имя архива формируется из текущей даты.
Проходит подключение  ЯНДЕКС ДИСКУ после удачному подключению загружаем zip-врхов на диск.
Выполняет уведомления электронным сообщение (удачная загрузка архива или нет).
zip-архив удаляется с компьютера(при удачной загрузке архива)
"""

import yadisk
import zipfile
import os
from datetime import datetime

from email_ import Email__notification
from lot__yandex import tok_


connection_disk = yadisk.YaDisk(token=tok_())


def delete_the_specified_file(archive):
        #Удаляем архив.
        os.remove(archive)


# Проверка работаспособность токена.
if connection_disk.check_token():
    print('Подключились к яндекс диску.')
    # Файлы загрузки в яднекс диск.
    file_to_upload = ['/home/denis-linux/Загрузки/yy.txt',
                      '/home/denis-linux/Загрузки/uuu.txt',


                          ]

    # Создаем название архива и указываем его место нахождения.
    archive = '/home/denis-linux/'+ datetime.today().strftime("%d.%m.%Y")+'.zip'
    if  os.path.isfile(archive):
        archive = '/home/denis-linux/доп' + datetime.today().strftime("%d.%m.%Y") + '.zip'

    # Упаковка файлов в zip архив
    with zipfile.ZipFile(archive, "a")as zip_:
        for i in file_to_upload:
            if os.path.isfile(i):
                zip_.write(i)

            else:
                folder_contents = os.listdir(i)
                for s in folder_contents:
                    file_to_upload.append(i + "/" + s)
    zip_.close()

    backup_date = datetime.today().strftime("%d.%m.%Y")
    try:
        connection_disk.upload(archive,'backup от '+ backup_date + '.zip')
        #Информация о ошибке по загрузке архива в яндекс диск.
        download_error = False
        #Вызов модуля для уведомления о результате загрузке данных.
        Email__notification(download_error)

        delete_the_specified_file(archive)

    except:
        download_error = True
        Email__notification(download_error)

else:
    download_error = True
    Email__notification(download_error)






