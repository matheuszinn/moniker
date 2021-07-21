import os


def file_renamer(directory: str, filename: str = 'Turma da Mônica - ') -> None:
    os.chdir(directory)

    for file in os.listdir():
        print(f'{file} -> {filename + file}')
        os.rename(
            directory + file,
            directory + filename + file
        )
