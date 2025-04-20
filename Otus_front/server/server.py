import socket
from http import HTTPStatus
from urllib.parse import parse_qs, urlparse


def run_server(host='127.0.0.1', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Server started on http://{host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(4096)  # Увеличиваем буфер для больших заголовков
                if not data:
                    continue

                request = data.decode('utf-8')
                request_lines = request.split('\r\n')

                # Парсинг метода и пути
                method, path, _ = request_lines[0].split(' ', 2)

                # Парсинг статуса
                status_code = 200
                query = urlparse(path).query
                params = parse_qs(query)
                if 'status' in params:
                    try:
                        status_code = int(params['status'][0])
                        if status_code not in [s.value for s in HTTPStatus]:
                            status_code = 200
                    except (ValueError, IndexError):
                        status_code = 200

                status_phrase = HTTPStatus(status_code).phrase

                # Формируем тело ответа
                response_body = [
                    f"Request Method: {method}",
                    f"Request Source: {addr}",
                    f"Response Status: {status_code} {status_phrase}"
                ]

                # Добавляем ВСЕ заголовки запроса в тело ответа
                for line in request_lines[1:]:
                    if ':' in line:  # Это заголовок
                        header_name, header_value = line.split(':', 1)
                        response_body.append(f"{header_name.strip()}: {header_value.strip()}")

                # Формируем полный HTTP-ответ
                response = (
                    f"HTTP/1.1 {status_code} {status_phrase}\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {len('\r\n'.join(response_body))}\r\n"
                    f"Connection: close\r\n\r\n"
                    f"{'\r\n'.join(response_body)}"
                )

                conn.sendall(response.encode('utf-8'))
if __name__ == '__main__':
    run_server()