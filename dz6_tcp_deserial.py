import struct
import datetime
import socket

# Функция вывода результата
def print_result(in_string):

    print(in_string)
    print(len(in_string))

    # Распаковываем байтовый массив
    result = struct.unpack("<BBIhIIIIBbb", in_string)
    print (result)

    reason = result[0]
    charge = result[1]
    t = datetime.datetime.fromtimestamp(result[2])
    temp = result[3] / 10
    in1 = result[4]
    in2 = result[5]
    in3 = result[6]
    in4 = result[7]
    ch_temp = result[8]
    mintemp = result[9]
    maxtemp = result[10]

    print("reason = %d, charge = %d, t = %s, temp = %d, in1 = %d, in2 = %d, "
        "in3 = %d, in4 = %d, ch_temp = %d, min_temp = %d, max_temp = %d"
        % (reason, charge, t, temp, in1, in2, in3, in4, ch_temp, mintemp, maxtemp))



HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

if __name__ == "__main__":
    # Настраиваем сокет, при установке соединения получаем данные и распечатываем в консоль
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as l:
        l.bind((HOST, PORT))
        l.listen()
        while True:
            print("Waiting...")
            conn, addr = l.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                if data:
                    print_result(data)

