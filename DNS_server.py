https://github.com/Jonthan1192/DNS-server-16.git
import socket


def main():
    server_ip = '0.0.0.0'
    port = 53
    default_size = 1024
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, port))
    print("Started\n")
    while True:
        try:
            data, addr = server_socket.recvfrom(default_size)
            if b"Close" in data:
                break
            if b"MyFakeDomain" in data:
                print(f"RECIEVED: {data}, from {addr}")
                title = data[:2] + b'\x81\x80' + b'\x00\x01' + b'\x00\x01' + b'\x00\x00' + b'\x00\x00'
                question = data[12:]
                answer = b'\xc0\x0c' + b'\x00\x01' + b'\x00\x01' + b'\x00\x00\x00\x41' + b'\x00\x04' + b'\x45\x45\x45\x45'
                response = title + question + answer
                server_socket.sendto(response, addr)
                print(f"SENT: {response}, to {addr}")

        except Exception as err:
            print('error: ', err)

    server_socket.close()
    print("Closing...")


if __name__ == '__main__':
    main()
