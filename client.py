
import os
import time
import socket
import argparse

MAX_PACKET = 2048

def write_file(file_name, content):
    html = ''
    for i in range(1,len(content)):
        html += content[i]

    file = open(file_name, 'w')

    for i in html:
        file.write(i)

    file.close()

def handle_server(server):
    total_data = [];
    data = '';
    timeout = 2
    begin = time.time()

    while True:
        if time.time() - begin > timeout:
            break

        try:
            data = server.recv(MAX_PACKET).decode('utf8')
            if data:
                total_data.append(data)
                begin = time.time()
        except:
            pass

    server.close()

    content = ''.join(total_data).split('\n\n')

    return content
    

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('port')
    parser.add_argument('file_name')
    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((socket.gethostbyname(args.host), int(args.port)))

    request = "GET / HTTP/1.1\nHost: {0}:{1}\nConnection: close\n\n".format(args.host, args.port).encode('utf8')

    server.send(request)

    content = handle_server(server)
    write_file(args.file_name, content)

run()