import socket
import threading

exit_all = False

debug_prints = True

lock = threading.Lock()


def safe_prints(to_print):
    global lock
    lock.acquire()
    print(to_print)
    lock.release()


def dns_recv(sock, tid):
    msg_title = sock.recv(12)
    msg_question = sock.recv(1)
    while msg_question[len(msg_question) - 1] != b'\x00':
        msg_question += sock.recv(msg_question[len(msg_question) - 1] + 1)
    msg_question += sock.recv(4)

    safe_prints(f"RECEIVED: f{msg_title + msg_question}, from client number {tid}")
    return msg_title, msg_question


def handle_client(s_clint_sock, tid, addr):
    global exit_all
    safe_prints(f'new client arrive {tid} {addr}')
    while not exit_all:
        msg_title, msg_question = dns_recv(s_clint_sock, tid)
        if b"MyFakeDomain" not in msg_question:
            break

    safe_prints(f"Client {tid} Closing")
    s_clint_sock.close()


def main():
    global exit_all
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 53))
    server_socket.listen(5)
    threads = []
    tid = 1
    while True:
        try:
            client_socket, addr = server_socket.accept()
            t = threading.Thread(target=handle_client, args=(client_socket, tid, addr))
            t.start()
            threads.append(t)
            tid += 1
        except socket.error as err:
            print('socket error', err)
            break
    exit_all = True
    for t in threads:
        t.join()

    server_socket.close()
    print('server will die now')


if __name__ == '__main__':
    main()
