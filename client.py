
import os
import time
import socket
import argparse

MAX_PACKET = 2048

def is_url_ok(url):
    protocol = ''
    host = ''
    port = ''
    file = ''

    list = url.split('://')
    if len(list) > 1:
        protocol = list[0]
        host = list[1]
    else:
        host = list[0]

    list = host.split('/')
    if len(list) > 1:
        print(list)
        host = list[0]

        for i in range(1, len(list)):
            print(i)
            file += '/' + list[i]

    list = host.split(':')
    if len(list) > 1:
        host = list[0]
        port = list[1]
    else:
        host = list[0]
        port = '80'

    if file != '':
        host += file

    if protocol != '' and protocol != 'http':
        print('Protocolo nao suportado')
        return False, host, port
    
    return True, host, port

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
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('file_name')
    args = parser.parse_args()

    is_ok, host, port = is_url_ok(args.url)

    if not is_ok:
        return

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((socket.gethostbyname(host), int(port)))

    request = "GET / HTTP/1.1\nHost: {0}:{1}\nConnection: close\n\n".format(host, port).encode('utf8')

    server.send(request)

    content = handle_server(server)
    write_file(args.file_name, content)

if __name__ == '__main__':
    main()