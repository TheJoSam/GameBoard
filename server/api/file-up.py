import socket
import hashlib
import tqdm

def file_up2(connection, instruction):
    project_name = hashlib.sha1(instruction[0].encode()).hexdigest()
    path = instruction[1]
    size = instruction[2]
    progress = tqdm.tqdm(range(size), f"Receiving {path}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(path, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = connection.recv(4096)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))