SIZE_HEADER_FORMAT = "0000|"  # n digits for data size + one delimiter
size_header_size = len(SIZE_HEADER_FORMAT)
VER = 'Python3'


def receive_by_size(sock):
    size_header = b''
    data_length = 0
    while len(size_header) < size_header_size:
        length = sock.recv(size_header_size - len(size_header))
        if length == b'':
            break
        else:
            size_header += length

    data = b''
    if size_header != b'':
        data_length = int(size_header[:size_header_size - 1])
        while len(data) < data_length:
            char = sock.recv(data_length - len(data))
            if char == b'':
                break
            else:
                data += char

    if data_length != len(data):
        data = b''  # Partial data is like no data !
    return data


def send_by_size(sock, binary_data):
    header_data = str(len(binary_data)).zfill(size_header_size - 1) + "|"
    byte_array = bytearray(header_data, encoding='utf8') + binary_data
    sock.send(byte_array)
