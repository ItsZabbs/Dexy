from ujson import load
from . import converters,autocomplete

def load_files_into_variable(file_path:str):
    with open(file_path,mode='r',encoding='utf-8') as file:
        return load(file)