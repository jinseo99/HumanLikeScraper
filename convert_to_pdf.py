from PIL import Image
import os
from zipfile import ZipFile

def open_zip(path, save_folder):
    archive =  ZipFile(path, 'r')
    image_files = []
    for entry in archive.infolist():
        file_ =  archive.open(entry) 
        image_files.append(Image.open(file_).convert('RGB'))
    image_files[0].save(save_folder, save_all=True, append_images=image_files)


folder = 'YacStorage/webtoon'
filename = ""

save_folder = 'YacStorage/webtoon'
save_path = filename[:-4] + ".pdf"

path = folder + filename
open_zip(path, save_path)
