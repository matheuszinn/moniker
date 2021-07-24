import os
import shutil

from slugify import slugify
from wand.image import Image
from wand.display import display
from itertools import product

# Function to rename the files


def file_renamer(directory: str, filename: str = 'Turma da Mônica - ') -> None:
    os.chdir(directory)

    for file in os.listdir():
        print(f'{file} -> {filename + file}')
        os.rename(
            directory + file,
            directory + filename + file
        )


# Function to save the files with the correct sequence
def save_images(target_folder, image_sequence):
    index = 0
    for img in image_sequence.sequence:
        img_page = Image(image=img)

        if index < 10:
            suffix = "00{0}".format(index)
        elif index >= 10 and index < 100:
            suffix = "0{0}".format(index)
        else:
            suffix = index

        img_page.save(filename=f"{target_folder}/img{suffix}.jpg")
        index += 1


# Function to create a cbz file from pdf
def pdf2cbz(pdf_files_directory: str, cbz_files_directory: str):
    os.chdir(pdf_files_directory)

    files = [file for file in os.listdir()]
    for file in files:
        filename, extension = os.path.splitext(file)
        slg_filename = f'{slugify(filename)}{extension}'

        shutil.copyfile(f'{pdf_files_directory}/{file}',
                        f'{pdf_files_directory}/{slg_filename}')

        target_folder = os.path.join(
            cbz_files_directory, slg_filename.split('.')[0])

        print(f'Lendo: {file}')
        pages = Image(filename=slg_filename)
        print(f'Lido: {file}\n{len(pages.sequence)} páginas encontradas')

        os.mkdir(target_folder)

        save_images(target_folder, pages)
        print('Imagens salvas')

        print('Zipando..')
        shutil.make_archive(f'{target_folder}', 'zip', target_folder)
        print(f'{file} foi zipado')

        shutil.rmtree(target_folder)
        os.rename(f"{target_folder}.zip",
                  f"{target_folder}.cbz")
        print("Criado o .cbz")

        os.remove(f'{pdf_files_directory}/{slg_filename}')

        print(f'Arquivo {file} terminado')
