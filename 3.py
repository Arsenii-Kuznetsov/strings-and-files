import os
import re


def search_py_files(list_files_directories):
    files = []
    for path in list_files_directories:
        if os.path.isfile(path):
            files += [path]
        else:
            files += search_py_files([os.path.join(path, x) for x in os.listdir(path)])
    return [path for path in files if os.path.splitext(path)[1] == '.py']


path = input('Введите путь до директории: ')
if not os.path.isdir(path):
    exit('Путь не является директорией')
list_files_directories = [os.path.join(path, x) for x in os.listdir(path)]
list_py_files = search_py_files(list_files_directories)
if len(list_py_files) == 0:
    exit('В директории нет файлов .py')
modules = dict()
for file in list_py_files:
    with open(file) as file_py:
        file_py = file_py.readlines()
        for line in file_py:
            if re.search('from (.)* import', line):
                line = line.replace('from', ' ').replace('import', ' ').replace(',', ' ')
                line_split = line.split()
                if line_split[0] in modules.keys():
                    for func in line_split[1:]:
                        modules[line_split[0]].add(func)
                else:
                    modules[line_split[0]] = set(s for s in line_split[1:])
            if re.search('import', line):
                line = line.replace('import', ' ')
                line_split = line.split()
                if not line_split[0] in modules.keys():
                    modules[line_split[0]] = set()
with open('result3.py', 'w') as result_file:
    for module in modules:
        if len(modules[module]) != 0:
            result_file.write(f"from {module} import {','.join(modules[module])}\n")
        else:
            result_file.write(f'import {module}\n')
