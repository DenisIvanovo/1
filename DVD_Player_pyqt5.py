import time
import datetime
import sys
import os

from PyQt5 import QtCore, QtGui
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QHBoxLayout,
                             QVBoxLayout, QLabel, QSlider, QSizePolicy, QFileDialog, QSplashScreen,
                             )
from PyQt5.QtGui import (QIcon, QPalette, QFont)
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize

# Глобальные переменные.
time_ = 0  # Начальное значение таймера.
version_of_the_script = '1.0'  # Версия скрипта.
speed = 2  # Обычная скорость возпроиведения видео.
time_spees = 1000  # Скорость отсчета таймера (1 секунда)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('DVD player')  # Заголовок окна.
        self.setGeometry(120, 120, 1070, 580)  # Размер окна и расположение окна на мониторе.
        self.setWindowIcon(QIcon('logo.jpg'))
        # Выполняем заливку виджета черным цветом.
        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.init_ui()

    def time_display(self, time_):
        # Отображение пройденого времени видео.
        a = str(datetime.timedelta(seconds=time_))  # Переводим секунды в формат
        # 'Час:минута:секунда'
        self.time_video_on.setText(a)  # Отображаем время видео.
        self.time_video_on.setFont(QFont('Ubuntu', 10))

    def start_time(self):
        # Старт отчет времени.
        self.timer.start()

    def stop_time(self):
        # Останавливает таймер.
        self.timer.stop()

    def pause_time(self):
        # Пауза таймера.
        self.isRunning = False
        self.timer.stop()

    def time_report(self):
        # Счетчик.
        global time_
        time_ += 1
        self.time_display(time_)

    def open_file(self):
        global time_
        """
        Диалоговое окно,для выбора файла.
        """
        try:
            user = os.getlogin()  # Запрашиваем имя пользователя пк.
            filename, _ = QFileDialog.getOpenFileName(self, 'Выберите файл',
                                                      directory="/Users/{0}/Documents".format(user),
                                                      filter= 'Видеофайлы (*.avi *.mp4)')

            if filename != '':
                self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
                self.playBtn.setEnabled(True)  # Делаем кнопку плей акттивной.
                self.rewindBtn.setEnabled(True)
                self.forwardBtn.setEnabled(True)

            self.stop_time()
            time_ = 0  # Обнуляем таймер.
            self.time_display(time_)
        except:
            self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile('mideo-logo.png')))


    def play_video(self):
        # Реагируем на нажатие кнопок(play, stop, pause)
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.mediaplayer.pause()

            self.pause_time()  # Ставим таймер на паузу.
            self.mediastate()
        else:
            self.mediaplayer.play()
            self.start_time()  # Запускаем отсчет времени.
            self.mediastate()

    def mediastate(self):
        # Изменяем вид кнопок в проигрователе.
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(QIcon('play-on.png'))
            self.stopBtn.setEnabled(False)
        else:
            self.playBtn.setIcon(QIcon('pause-on.png'))
            self.stopBtn.setIcon(QIcon('stop-on.png'))
            self.stopBtn.setEnabled(True)


    def position_chander(self, position):
        # Работаем с позицией ползунка в плеере.
        self.slider.setValue(position)

    def duration_chander(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        global time_
        # Включаем видео в точке позиции ползунка.
        self.mediaplayer.setPosition(position)
        # Получаем время просмотра видео при перемищении ползунка.
        slider_now = self.slider.value() // 1000
        self.pause_time()  # На время перемищения таймер ставим на паузу.
        time_ = slider_now  # В глобальную переменую помещаем значения времени ползунка.
        self.start_time()  # Снимаем с паузы таймер.

    def sound_volume(self):
        # Обрабатываем действия с громкостью.
        self.mediaplayer.setVolume(self.slider_sound.value())

    def volume_muted(self):
        # Выключаем и включаем звук.
        if self.mediaplayer.isMuted():
            self.mediaplayer.setMuted(False)  # Включаем звук.
            self.soundBtn.setIcon(QIcon('sound-on.png'))
        else:
            self.mediaplayer.setMuted(True)  # Отключаем звук.
            self.soundBtn.setIcon(QIcon('sound.png'))

    def fast_forward(self):
        # Управляем скоростью перемотки вперед.
        global speed, time_spees
        if speed > 4:  # Если скорость перемотки больше 4 скорости,
            self.mediaplayer.setPlaybackRate(1)  # устанавливаем стандартное возпроизведение видео.
            self.forwardBtn.setToolTip('Стандартная скорость.')
            speed = 2  # Устанавливаем 2 скорость.
            self.timer.setInterval(time_spees)  # Стандартный отсчет счетчика.
            self.forwardBtn.setIcon(QIcon('forward.png'))
        else:
            self.mediaplayer.setPlaybackRate(speed)  # Перематываем видео .
            self.forwardBtn.setToolTip('Стандартная скорость * {0}'.format(speed))
            self.timer.setInterval(time_spees // speed)
            speed += 2  # Увеличиваем скорость перемотки.
            self.forwardBtn.setIcon(QIcon('forward-on.png'))
        #self.mediaplayer.setPosition(self.mediaplayer.position() + 10000)



    def stop(self):
        global time_
        # Останавливаем воспроизведения видео.Перемищяем позицию ползунка на начало.
        self.mediaplayer.stop()
        self.playBtn.setIcon(QIcon('play-button.png'))  # Изменяем картинку на кнопке.
        self.stopBtn.setIcon(QIcon('stop.png'))  # Изменяем картинку на кнопке.

        time_ = 0  # Обнуляем таймер.
        self.time_display(time_)  # Отображаем время.


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.labei.setText('ERROR ^  ' + self.mediaplayer.errorString())

    def info_video(self, state):
        try:
            # Получаем информаию о видео файле.
            if state == QMediaPlayer.LoadedMedia:
                self.info_time = (self.mediaplayer.metaData('Duration') // 1000)
                a = str(datetime.timedelta(seconds=self.info_time))  # Переводим секунды в формат
            # 'Час:минута:секунда'
                self.time_video.setText(a)  # Отображаем время.
                self.time_video.setFont(QFont('Ubuntu', 10))

            # Получаем название видео.
            try:
                self.info_title_video.setText(self.mediaplayer.metaData('Title'))
                self.info_title_video.setStyleSheet('color: white ')  # Установливаем цвет виджета.
            except:
                self.info_title_video.setText('Нет информации.')
                self.info_title_video.setStyleSheet('color: white ')  # Установливаем цвет виджета.
        except:
            pass

    def load_data(self, sp):
        # Заставка.
        data_sp = ['', '', '', '', '']
        ind = 0
        for i in range(1, 11):
            if i % 2 == 0:
                # Имитируем загрузку
                sp.showMessage('{0} .... {1}%'.format(data_sp[ind], i * 10),
                               QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom, QtCore.Qt.red)
                ind += 1
                time.sleep(0.5)
            else:
                sp.showMessage('{0} .... {1}%'.format(data_sp[ind], i * 10),
                               QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom, QtCore.Qt.red)
                time.sleep(0.5)

    def init_ui(self):
        global version_of_the_script, time_spees
        """"
        Создаем дизайн видео плеера.
        """
        # Дизайн видео плеера.
        self.mediaplayer = QMediaPlayer()
        # Объект видео виджет.
        self.videowidget = QVideoWidget()
        self.videowidget.setMinimumHeight(
            self.window().size().height() - 50)  # Высота видео виджета.
        self.videowidget.setMinimumWidth(
            self.window().size().width() - 10)  # Ширина видео виджета.

        #  Создаем кнопки открыть и плей.
        self.openBtn = QPushButton('Open video')  # Кнопка выбора файла для просмотра.
        self.openBtn.setIcon(QIcon('btn_open.jpg'))  # Картинка кнопки openBtn
        self.openBtn.clicked.connect(self.open_file)

        # Комплект кнопок video player.
        self.playBtn = QPushButton()  # Кнопка плей.
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(QIcon('play-button.png'))
        self.playBtn.setIconSize(QSize(64, 64))
        self.playBtn.setMaximumSize(40, 40)
        self.playBtn.clicked.connect(self.play_video)

        self.rewindBtn = QPushButton()  # Кнопка перемотка назад.
        self.rewindBtn.setEnabled(False)
        self.rewindBtn.setIcon(QIcon('rewind.png'))
        self.rewindBtn.setIconSize(QSize(64, 64))
        self.rewindBtn.setMaximumSize(40, 40)
        self.rewindBtn.clicked.connect(self.play_video)

        self.forwardBtn = QPushButton()  # Кнопка перемотка вперед.
        self.forwardBtn.setEnabled(False)
        self.forwardBtn.setIcon(QIcon('forward.png'))
        self.forwardBtn.setIconSize(QSize(64, 64))
        self.forwardBtn.setMaximumSize(40, 40)
        self.forwardBtn.clicked.connect(self.fast_forward)

        self.stopBtn = QPushButton()  # Кнопка стоп.
        self.stopBtn.setEnabled(False)
        self.stopBtn.setIcon(QIcon('stop.png'))
        self.stopBtn.setIconSize(QSize(64, 64))
        self.stopBtn.setMaximumSize(40, 40)
        self.stopBtn.clicked.connect(self.stop)

        self.soundBtn = QPushButton()  # Кнопка включить или отклычить звук.
        self.soundBtn.setIcon(QIcon('sound-on.png'))
        self.soundBtn.setIconSize(QSize(64, 64))
        self.soundBtn.setMaximumSize(40, 40)
        self.soundBtn.clicked.connect(self.volume_muted)
        self.soundBtn.setEnabled(True)

        # горизонтальный ползунок времени.
        self.slider = QSlider(Qt.Horizontal)  # Горизонтальное расположение.
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # Горизонтальный ползунок громкости.
        self.slider_sound = QSlider()
        self.slider_sound.setRange(0, 100)  # Минимальное и максимальное начение.
        self.slider_sound.setTickInterval(5)
        self.slider_sound.setValue(30)
        self.slider_sound.setMaximumHeight(40)
        self.slider_sound.setMaximumWidth(20)
        self.slider_sound.sliderMoved.connect(self.sound_volume)

        # Виджет отображает длительность видео.
        self.time_video = QLabel('00:00:00')  # Начальное показание.
        self.time_video.setFont(QFont('Ubuntu', 10))
        self.time_video.setStyleSheet('color: white ')  # Установливаем цвет виджета.
        # Виджет отображает время просмотреного видео.
        self.time_video_on = QLabel('00:00:00')  # Начальное показание.
        self.time_video_on.setFont(QFont('Ubuntu', 10))
        self.time_video_on.setStyleSheet('color: white ')  # Установливаем цвет виджета.
        # Разделитель.
        self.raz = QLabel('/')
        self.raz.setFont(QFont('Ubuntu', 10))
        self.raz.setStyleSheet('color: white ')  # Установливаем цвет виджета.
        # Отображаем название видео.
        self.info_title_video = QLabel()
        # Отображаем версию скрипта.
        self.script = QLabel('Версия ' +version_of_the_script)
        self.script.setAlignment(Qt.AlignHCenter)
        self.script.setStyleSheet('color: white ')  # Установливаем цвет виджета.
        #
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Создаем горизонтальный контейнер.
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        # Добавлям виджеты в горизонтальный контейнер.
        self.hboxlayout.addWidget(self.openBtn)
        self.hboxlayout.addWidget(self.slider)
        self.hboxlayout.addWidget(self.time_video_on)
        self.hboxlayout.addWidget(self.raz)
        self.hboxlayout.addWidget(self.time_video)

        # Содаем горизонтальный контейнер кнопок video player.
        self.hboxBtn = QHBoxLayout()
        self.hboxBtn.setAlignment(Qt.AlignHCenter)
        # Добавляем кнопки в горинтальный контейнер.
        self.hboxBtn.addWidget(self.rewindBtn)
        self.hboxBtn.addWidget(self.stopBtn)
        self.hboxBtn.addWidget(self.playBtn)
        self.hboxBtn.addWidget(self.forwardBtn)
        self.hboxBtn.addWidget(self.soundBtn)
        self.hboxBtn.addWidget(self.slider_sound)

        # Создаем вертикальный контейнер.
        self.vbox = QVBoxLayout()
        # Добавляем виджеты в вертикальный контейнер.
        self.vbox.addWidget(self.info_title_video)
        self.vbox.addWidget(self.videowidget)
        self.vbox.addLayout(self.hboxlayout)
        self.vbox.addLayout(self.hboxBtn)
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.script)

        self.setLayout(self.vbox)

        self.mediaplayer.setVideoOutput(self.videowidget)

        # media player signals
        self.mediaplayer.positionChanged.connect(self.position_chander)
        self.mediaplayer.durationChanged.connect(self.duration_chander)
        self.mediaplayer.mediaStatusChanged.connect(self.info_video)

        # Время просмотренного видео.
        self.timer = QTimer()
        self.timer.setInterval(time_spees)

        self.timer.timeout.connect(self.time_report)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    # Загружаем заставку.
    splash = QSplashScreen(QtGui.QPixmap('mideo-logo.png'))
    splash.showMessage('Проверка обновлений .... 0%',
                       QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom, QtCore.Qt.red)
    splash.setGeometry(450, 200, 320, 320)
    splash.pixmap()
    # ОТображаем заставку
    splash.show()
    # Запускаем оборотный цикл
    App.processEvents()

    window = Window()
    window.load_data(splash)
    window.show()
    splash.finish(window)

    sys.exit(App.exec_())
