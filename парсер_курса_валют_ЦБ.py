"""
Парсим курс валюты по API ЦБ РФ
Отображаем два курса (доллар и евро)
Устанавливаем параметры даты
(если параметры оставить пустыми тогда курсы валют мы полуим на текущию дату)
"""
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication,QHBoxLayout,QVBoxLayout,QComboBox,QWidget,QLabel,\
    QLCDNumber,QPushButton,QCalendarWidget,QDialog,QMessageBox
import sys
from PyQt5.QtCore import QDate
from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup as bs


class Window(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui()
        self.current_date()
        self.filling_in_data()

    def ui(self):

        """"
        Прописываем все необходимые видщеты.
        """
        self.setWindowTitle('Курс валюты ЦБ')
        self.setGeometry(320,320,200,100)

        # Создаем два дисплея для отображения курса валют.
        self.hbox_3 = QHBoxLayout()
        self.hbox_4 = QHBoxLayout()
        self.label_usd = QLabel('USD')
        self.label_usd.setPixmap(QPixmap('usd.png'))
        self.label_eur = QLabel('EUR')
        self.label_eur.setPixmap(QPixmap('eur.png'))
        self.lcd = QLCDNumber()
        self.lcd_2 = QLCDNumber()
        self.hbox_3.addWidget(self.label_usd)
        self.hbox_3.addWidget(self.lcd)
        self.hbox_4.addWidget(self.label_eur)
        self.hbox_4.addWidget(self.lcd_2)

        self.hbox_2 = QHBoxLayout()
        self.label = QLabel('День :')
        self.label.setFont(QFont('ubuntu', 15))
        self.label_2 = QLabel('Месяц :')
        self.label_2.setFont(QFont('ubuntu', 15))
        self.label_3 = QLabel('Год :')
        self.label_3.setFont(QFont('ubuntu', 15))
        # Упаковка в горизонтальный контейнер.
        self.hbox_2.addWidget(self.label)
        self.hbox_2.addWidget(self.label_2)
        self.hbox_2.addWidget(self.label_3)
        # Создаем горизонтальный контенер для установки даты.
        self.hbox = QHBoxLayout()
        # 3 Параметра для установки даты для запроса.
        self.date_h = QComboBox()
        self.date_h.setFont(QFont('ubuntu',12))
        self.month_h = QComboBox()
        self.month_h.setFont(QFont('ubuntu', 12))
        self.year_h = QComboBox()
        self.year_h.setFont(QFont('ubuntu', 12))
        self.btn_cal = QPushButton()
        self.btn_cal.setIcon(QIcon('cal.png'))
        self.dialog = Calendar(self)
        self.btn_cal.clicked.connect(self.dialog.exec)
        # Упаковываем ComboBox в горизонтальный контенер.
        self.hbox.addWidget(self.date_h)
        self.hbox.addWidget(self.month_h)
        self.hbox.addWidget(self.year_h)
        self.hbox.addWidget(self.btn_cal)
        # Создание кнопки.
        self.btn = QPushButton('Получить курс валюты')
        self.btn.clicked.connect(self.currency_parsing)

        # Создаем вертикальный контейнер.
        self.vbox = QVBoxLayout()
        # Упаковка вертикального контейнера.
        self.vbox.addLayout(self.hbox_3)
        self.vbox.addLayout(self.hbox_4)
        self.vbox.addLayout(self.hbox_2)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.btn)

        # Отображение контенеров.
        self.setLayout(self.vbox)
        self.show()

    def current_date(self):
        """"
        Получаем текущию дату
        и по умолчанию в параметрах устанавливаем её.
        """
        dt = datetime.now()
        self.date_h.addItem(str(dt.day))
        self.month_h.addItem(str(dt.month))
        self.year_h.addItem(str(dt.year))

    def  filling_in_data(self):
        # Заполняем данными параметры через циклы.
        for i in range(1,32):
            self.date_h.addItem(str(i))

        for i in range(1,13):
            self.month_h.addItem(str(i))

        for i in range(2020,1989,-1):
            self.year_h.addItem(str(i))


    def currency_parsing(self):
        """
        парсим курсы валют по API ЦБ РФ.
        Получаем дату для получения курса валют.
        Если число или месяц от 1-9 тогда мы добавляем значения '0'
        для правильного запроса формата 'dd/mm/yyyy'
        """
        d = self.date_h.currentText()
        if len(d) == 1 :
            d = '0'+ d
        m = self.month_h.currentText()
        if len(m) == 1 :
            m = '0' + m
        y = self.year_h.currentText()

        # Делаем проверку даты,если выбраная дата больше текущей тогда выводим ошибку.
        current_date = datetime.now().strftime('%d%m%Y')
        date_comboBox = datetime(int(y),int(m),int(d)).strftime('%d%m%Y')
        if date_comboBox > current_date:
            QMessageBox.about(self,'Сообщение','Невозможно получить курс валюты\n'
                                               'т.к.выбранная дата больше текущего дня.')
        else:

            # Делаем запрос на сайт,передаем ему параметр.
            url = 'http://www.cbr.ru/scripts/XML_daily.asp?'
            params = {
                'date_req': '{0}/{1}/{2}'.format(d,m,y)
            }

            try:
                try:
                    request = requests.get(url,params)
                    soup = bs(request.content,'xml')
                    find_usd = soup.find(ID='R01235').Value.string
                    self.lcd.setDisabled(False)
                    self.lcd.setNumDigits(7)
                    self.lcd.display(find_usd[:6])
                except AttributeError:
                    self.lcd.display('0')
                    self.lcd.setDisabled(True)
                    self.gfgfg()
                try:
                    find_eur = soup.find(ID='R01239').Value.string
                    self.lcd_2.setDisabled(False)
                    self.lcd_2.setNumDigits(7)
                    self.lcd_2.display(find_eur[:6])
                except AttributeError:
                    self.lcd_2.display('0')
                    self.lcd_2.setDisabled(True)
                    self.gfgfg()
            except AttributeError:
                self.lcd.display('0')
                self.lcd_2.display('0')

    def gfgfg(self):
        QMessageBox.about(self, 'Соощение', 'На данную дату мы не смогли получить курс валют\n'
                                            'At this date we were unable to get the exchange rate')

class Calendar(QDialog):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.main = root
        self.calendar_ui()

    def calendar_ui(self):
        """
        Отрисовываем календарь и получаем выбраное число,
        передаем параметрами в основное окно.
        """
        self.setWindowTitle('Календарь')
        self.vbox = QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.vbox.addWidget(self.calendar)
        self.calendar.clicked[QDate].connect(self.activatel_calendar)

        self.setLayout(self.vbox)


    def activatel_calendar(self,date):
        # Получаем дату ,месяч и год выбраную из календаря.
        self.date_c = date.toString('d')
        self.month_c = date.toString('M')
        self.year_c = date.toString('yyyy')
        print(self.date_c,self.month_c,self.year_c)
        self.push()

    def push(self):
        # Заполняем дату из календаря,и закрываем календарь.
        self.main.date_h.setItemText(0,str(self.date_c))
        self.main.month_h.setItemText(0,str(self.month_c))
        self.main.year_h.setItemText(0, str(self.year_c))
        self.close()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())