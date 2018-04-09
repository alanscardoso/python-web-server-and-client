
import os
import time
import socket

file_name = 'result.html'
host = socket.gethostbyname('localhost')
port = 13000
MAX_PACKET = 2048
request = "GET / HTTP/1.1\nHost: {0}:{1}\nConnection: close\n\n".format(host, port).encode('utf8')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((host, port))
server.send(request)

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

    write_file(file_name, content)
    

def run():
    handle_server(server)

run()