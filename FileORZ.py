# -*- coding: utf-8 -*-
import os
import time

# pasta de downloads e extenção de arquivo
def organize_files():
    path = "C:\\Users\\UserName\\Downloads"
    files = os.listdir(path)
    extensions_to_include = {
        'Documentos': ['.pdf', '.doc', '.txt', '.pptx', '.docx', '.xlsx', '.xlsm', '.csv', '.xls', '.dotm', '.ponto', '.dotx', '.htm', '.html', '.doc', '.docx', '.cfg', '.alg'],
        'Vídeos': ['.mov', '.mp4', '.avi', '.av1', '.mpeg-2', '.avchd', '.aac', '.mkv', '.divx', '.h.264', '.mpeg-1', '.wmv'],
        'Áudios': ['.mp3', '.wav', '.flac', '.3GP', '.M4A', '.ogg', '.wma', '.m4a', '.webm'],
        'Compactos': ['.rar', '.zip', '.zpix', '.7z', '.rar5', '.iso', '.gzip', '.7-zip', '.tar'],
        'Fontes': ['.ttf', '.eot', '.woff', '.woff2',],
        'Setups': ['.exe', '.msi', '.appx', '.appxbundle', 'msix', '.appxbundle', '.appx', ,'apk'],
        'Imagens':['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.cr3','.cr2', '.exif', 
        '.psd', '.eps', '.ai', '.svg', '.webp', '.heic', '.heif', '.raw', 'af'] 
    }

    #verificar se o arquivo ja existe
    found_files = {}
    #Mover os arquivos para a pasta referente ao tipo de arquivo e a extenção
    for file in files:
        filename, file_extension = os.path.splitext(file)
        for folder, extensions in extensions_to_include.items():
            if file_extension.lower() in extensions:
                new_folder = os.path.join(path, folder, file_extension.upper()[1:])
                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)

                # Mudar nome do arquivo para evitar erro
                destination_file = os.path.join(new_folder, file)
                counter = 1
                while os.path.exists(destination_file):
                    new_filename = f"{filename}_{counter}{file_extension}"
                    destination_file = os.path.join(new_folder, new_filename)
                    counter += 1

                    os.rename(os.path.join(path, file), destination_file)


                if filename in found_files:
                    os.remove(os.path.join(path, file))
                else:
                    found_files[filename] = True
                    os.rename(os.path.join(path, file), destination_file)
                    break
#verificar a pasta a cada 5 segundos
while True:
    organize_files()
    time.sleep(5)
