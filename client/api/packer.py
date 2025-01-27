"""API Module to pack games and other data in an efficient and quickshare way."""

import os
import shutil
from alive_progress import alive_it

def _bytes(file):
    return file[1]

def generate_data_dir_tree(data_dir: str):
    """Module to create an Filetree for use in the packer.

    Args:
        data_dir (str): Path to the Data Directory (direct directory ex. "games/Minecraft")

    Returns:
        data_dir_tree: list with lists for every file, showing file path and size in Bytes
    """
    data_dir_tree = []
    for root,directories,files in os.walk(data_dir):
        for file in files:
            file_path = f'{root}/{file}'.replace('\\', '/')
            file_size = os.path.getsize(file_path)
            data_dir_tree.append([file_path, int(file_size)])
    return data_dir_tree


def create_packets(data_dir: str):
    files = generate_data_dir_tree(data_dir)
    files.sort(key=_bytes, reverse=True)
    max_file_size = (files[0][1])
    max_packet_size = int(max_file_size + 50)
    half_file_size = int(max_file_size / 2)
    packets = []

    big_files = [file for file in files if file[1] >= half_file_size]
    small_files = [file for file in files if file[1] <= half_file_size]
    small_files.sort(key=_bytes)

    while True:
        packet_size = int(0)
        packet = []
        while True:
            while big_files:
                file = big_files[0]
                if (packet_size+file[1]) >= max_packet_size: break
                packet.append(file[0])
                packet_size += file[1]
                big_files.remove(file)
            
            while small_files:
                file = small_files[0]
                if (packet_size+file[1]) >= max_packet_size: break
                packet.append(file[0])
                packet_size += file[1]
                small_files.remove(file)
            
            packets.append({'files': packet, 'size': packet_size, 'delta': max_packet_size - packet_size})
            break
        if not small_files and not big_files: break

    return packets


def zip_packets(data_dir: str):
    packets = create_packets(data_dir)
    pid = 0
    for packet in packets:
        packet_path = str('./temp/packet_' + str(pid))
        if not os.path.isdir(packet_path): os.makedirs(packet_path)
        files = packet['files']
        for file in alive_it(files):
            dst_file = file.split('/')[-1]
            shutil.copy2(file, f'{packet_path}/{dst_file}')
        pid += 1
        

if __name__ == '__main__':
    zip_packets('./client/test')
