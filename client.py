
import os
import sys
import time
import socket
import argparse

MAX_PACKET = 2048

def is_url_ok(url):
    """ Verifica se a url solicitada possui a formatacao correta. A url pode ou nao conter o protocolo e porta."""
    protocol = ''
    host = ''
    port = ''
    file = ''

    # verifica se existe protocolo discriminado
    list = url.split('://')
    if len(list) > 1:
        protocol = list[0]
        host = list[1]
    else:
        host = list[0]

    # verifica se existe algum arquivo discriminado
    list = host.split('/')
    if len(list) > 1:
        print(list)
        host = list[0]

        for i in range(1, len(list)):
            print(i)
            file += '/' + list[i]

    # verifica se existe porta discriminada
    list = host.split(':')
    if len(list) > 1:
        host = list[0]
        port = list[1]
    else:
        host = list[0]
        port = '80'

    # recupera o ip do host
    host = socket.gethostbyname(host)
    if file != '':
        host += file

    # somente o protocolo HTTP e suportado
    if protocol != '' and protocol != 'http':
        print('Protocolo nao suportado')
        return False, host, port
    
    return True, host, port

def write_file(file_name, content):
    """ grava arquivo de saida """
    html = ''
    for i in range(1,len(content)):
        html += content[i]

    file = open(file_name, 'w')

    for i in html:
        file.write(i)

    file.close()
    print('Arquivo gerado')

def handle_server(server):
    """ recebe os dados do servidor """
    total_data = [];
    data = '';
    timeout = 2
    begin = time.time()

    # mantem um loop aberto por tempo limitado para recuperar todos os dados
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
    # valida argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('file_name')
    args = parser.parse_args()

    # valida se a url inserida segue os padrões
    is_ok, host, port = is_url_ok(args.url)
    if not is_ok:
        return

    # configuracoes do socket e do request
    request = "GET / HTTP/1.1\nHost: {0}:{1}\nConnection: close\n\n".format(host, port).encode('utf8')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, int(port)))
    server.send(request)
    # recupera dados da pagina e salva em um arquivo
    content = handle_server(server)
    #print(content)
    status = content[0].split(' ')[1]
    print('Status da requisição: ' + str(status))
    # se nao houve erro o arquivo e gerado
    if status != '200':
        print('Houve um erro e o arquivo não foi gerado')
        sys.exit()
	
    write_file(args.file_name, content)

if __name__ == '__main__':
    main()