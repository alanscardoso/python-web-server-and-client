import os
import socket
import argparse
import mimetypes

MAX_PACKET = 2048

def handle_client(client, folder):
    """ recebe os dados do client e retorna os devidos status e informacoes solicitadas """
    request = client.recv(MAX_PACKET)
    request = request.decode('utf8')
    is_request_ok = True
    status = ''
    content_type = ''
    response = ''

    # verifica o request que deve conter um metodo e um arquivo solicitado
    try:
        method = request.split(' ')[0]
        file = request.split(' ')[1]

        # verifica se o metodo e o GET, unico metodo suportado
        # retorna um 400(bad request) caso nao seja
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

    # se o request nao estiver certo, retorna um 400(bad request)
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
    
    # se tudo estiver certo com o request retorna 200(OK)
    if is_request_ok:
        files = os.listdir(folder)

        # se nao ha arquivo discriminado no get, procura pelo index.html
        if file == '/':
            # retorna o index.html caso exista
            if 'index.html' in files:
                status = 'HTTP/1.1 200 OK\n'
                contet_type = 'Content-Type: text/html\n'

                response = open(folder + 'index.html', 'r').read().encode('utf8')
            # se nao existir o index.html, retorna a listagem de arquivos do diretorio
            else:
                status = 'HTTP/1.1 200 OK\n'
                contet_type = 'Content-Type: text/html\n'

                files_str = ''

                for file in files:
                    # so adiciona arquivos que nao sejam invisiveis na listagem
                    if file[0] != '.':
                        size = os.path.getsize(folder+file)
                        files_str += """<tr>
                                            <td><a href=/{0}><li>{1}</li></a></td>
                                            <td>{2} bytes</td>
                                          </tr>""".format(file, file, size)


                response = """
                    <!DOCTYPE html>
                    <html lang='pt-br'>
                    <meta charset="UTF-8">
                    <body>
                    <h2>Listing Files</h2>
                    <table style="width:40%">
                        {0}
                        </table>
                        </body>
                        </html>""".format(files_str).encode('utf8')
        # se houver arquivo discriminado no request, realiza o tratamento adequado
        else:
            file = file[1:]
            # verifica se o arquivo solicitado existe no diretorio
            if file in files:        
                extension = file.split('.')[1]
                # se for text le o arquivo normalmente
                if extension in ['css','htm','html','txt']:
                    status = 'HTTP/1.1 200 OK\n'
                    contet_type = 'Content-Type: text/html\n'

                    response = open(folder + file, 'r').read().encode('utf8')
                # se nao le o arquivo no modo binario
                else:
                    status = 'HTTP/1.1 200 OK\n'
                    contet_type = 'Content-Type: {0}\n'.format(mimetypes.guess_type(folder + file)[0])
                    print(mimetypes.guess_type(folder + file)[0])

                    response = open(folder + file, 'rb').read() # rb = read binary
            # se o arquivo solicitado nao existir no diretorio, retorna 404(not found)
            else:
                status = 'HTTP/1.1 404 ERROR\n'
                contet_type = 'Content-Type: text/html\n'

                response = """
                    <!DOCTYPE html>
                    <html lang='pt-br'>
                    <meta charset="UTF-8">
                    <body>
                    <h1>404 file not found</h1>
                    O arquivo {0} não existe no servidor.
                    </body>
                    </html>
                """.format(file).encode('utf8')
            
    # envia os dados ao client
    try:
        client.send(status.encode('utf8'))
        client.send(content_type.encode('utf8'))
        client.send('\n'.encode('utf8'))
        client.send(response)
        client.close()
    except Exception as e:
        print(e)

def main():
    #valida argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument('port')
    parser.add_argument('folder')
    args = parser.parse_args()

    # verifica se existe folder e se está correta
    folder = ''
    if args.folder[-1] != '/':
        folder = args.folder + '/'
    else:
        folder = args.folder

    # configuracoes do socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', int(args.port)))
    server.listen(1) # permite apenas uma conexao por vez, esse parametro pode ser aumentado
	
    print('Server running...')
    
    while True:
        client, address = server.accept()
        handle_client(client, folder)
        
if __name__ == '__main__':
    main()
