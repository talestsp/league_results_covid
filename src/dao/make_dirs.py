import os

def mk_general_data_dir():
    try:
        os.mkdir("data/")
    except FileExistsError:
        pass

def mkdir(dir_name):
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass
