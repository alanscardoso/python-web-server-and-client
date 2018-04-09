import os
import socket
import argparse

MAX_PACKET = 2048

def handle_client(client):
    request = client.recv(MAX_PACKET)
    request = request.decode('utf8')
    is_request_ok = True
    status = ''
    content_type = ''
    response = ''

    try:
        method = request.split(' ')[0]
        file = request.split(' ')[1]

        if method != 'GET':
            is_request_ok = False
            status = 'HTTP/1.1 400 ERROR\n'
            contet_type = 'Content-Type: text/html\n'
            
            response = """
                <!DOCTYPE html>
                <html lang='pt-br'>
                <meta charset="UTF-8">
                <body>
                <h1>400 bad request</h1>
                Apenas o metodo GET e suportado
                </body>
                </html>
            """.encode('utf8')

    except:
        is_request_ok = False
        status = 'HTTP/1.1 400 ERROR\n'
        contet_type = 'Content-Type: text/html\n'
        
        response = """
            <!DOCTYPE html>
            <html lang='pt-br'>
            <meta charset="UTF-8">
            <body>
            <h1>400 bad request</h1>
            </body>
            </html>
        """.encode('utf8')
        print(request)
    
    if is_request_ok:
        files = os.listdir()

        if file == '/':
            if 'index.html' in files:
                status = 'HTTP/1.1 200 OK\n'
                contet_type = 'Content-Type: text/html\n'

                response = open('index.html', 'r').read().encode('utf8')
            else:
                status = 'HTTP/1.1 200 OK\n'
                contet_type = 'Content-Type: text/html\n'

                files_str = ''

                for file in files:
                    if file[0] != '.':
                        files_str +="<a href=/{0}><li>{0}</li></a>".format(file)

                response = """
                    <!DOCTYPE html>
                    <html lang='pt-br'>
                    <meta charset="UTF-8">
                    <body>
                    <ul>
                    {0}
                    </ul>
                    </body>
                    </html>
                """.format(files_str).encode('utf8')
        else:
            file = file[1:]
            if file in files:
                extension = file.split('.')[1]
                if extension in ['png','jpg','gif','ico','pdf']:
                    status = 'HTTP/1.1 200 OK\n'
                    contet_type = 'Content-Type: text/html\n'

                    response = open(file, 'rb').read()
                else:
                    status = 'HTTP/1.1 200 OK\n'
                    contet_type = 'Content-Type: text/html\n'

                    response = open(file, 'r').read().encode('utf8')
            else:
                status = 'HTTP/1.1 404 ERROR\n'
                contet_type = 'Content-Type: text/html\n'

                response = """
                    <!DOCTYPE html>
                    <html lang='pt-br'>
                    <meta charset="UTF-8">
                    <body>
                    <h1>404 file not found</h1>
                    O arquivo {0} não existe não existe no servidor.
                    </body>
                    </html>
                """.format(file).encode('utf8')
            
    try:
        client.send(status.encode('utf8'))
        client.send(content_type.encode('utf8'))
        client.send('\n'.encode('utf8'))
        client.send(response)
        client.close()
    except Exception as e:
        print(e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('port')
    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((args.host, int(args.port)))
    server.listen(1)
    
    while True:
        client, address = server.accept()
        handle_client(client)
        
if __name__ == '__main__':
    main()
