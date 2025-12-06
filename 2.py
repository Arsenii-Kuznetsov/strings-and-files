import re
from datetime import datetime


def statistics(logs):
    average_response_size = dict()
    count_errors = 0
    for log in logs:
        status = int(re.findall(' [1-9][0-9]{2} ', log)[0])
        if re.fullmatch('[45][0-9]{2}', str(status)):
            count_errors += 1
        bytes = int(re.findall(' [1-9][0-9]*$', log)[0])
        if status in average_response_size.keys():
            average_response_size[status] += [bytes]
        else:
            average_response_size[status] = [bytes]
    for status, list_bytes in average_response_size.items():
        average_response_size[status] = sum(list_bytes) / len(list_bytes)
    return average_response_size, count_errors


try:
    with open(input('Введите путь к файлу access.log: ')) as logs:
        logs = logs.readlines()
        average_response_size, count_errors = statistics(logs)
        log_time_pattern = '\[[1-3][0-9]?/(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/[0-9]*:[0-2][0-9]:[0-5][0-9]:[0-5][0-9] \+0300]'
        time_start = input(
            'Введите дату и время начала временного диапазона в формате [день/месяц/год:час:минута:секунда часовой пояс]: ')
        if not re.fullmatch(log_time_pattern, time_start):
            exit('Некорректное время начала')
        time_end = input(
            'Введите дату и время конца временного диапазона в формате [день/месяц/год:час:минута:секунда зона]: ')
        if not re.fullmatch(log_time_pattern, time_end):
            exit('Некорректное время окончания')
        try:
            time_start_dt = datetime.strptime(time_start[1:-1], '%d/%b/%Y:%H:%M:%S %z')
        except ValueError:
            exit('некорректное время начала')
        try:
            time_end_dt = datetime.strptime(time_end[1:-1], '%d/%b/%Y:%H:%M:%S %z')
        except ValueError:
            exit('некорректное время окончания')
        if min(time_start, time_end, key=lambda x: datetime.strptime(re.findall(log_time_pattern, x)[0][1:-1],
                                                                     '%d/%b/%Y:%H:%M:%S %z')) == time_end:
            exit('Время начала должно быть меньше времени окончания')
        logs.sort(key=lambda x: datetime.strptime(re.findall(log_time_pattern, x)[0][1:-1], '%d/%b/%Y:%H:%M:%S %z'))
        logs = [log for log in logs if max(time_start, re.findall(log_time_pattern, log)[0],
                                           key=lambda x: datetime.strptime(re.findall(log_time_pattern, x)[0][1:-1],
                                                                           '%d/%b/%Y:%H:%M:%S %z')) == min(time_end,
                                                                                                           re.findall(
                                                                                                               log_time_pattern,
                                                                                                               log)[0],
                                                                                                           key=lambda
                                                                                                               x: datetime.strptime(
                                                                                                               re.findall(
                                                                                                                   log_time_pattern,
                                                                                                                   x)[
                                                                                                                   0][
                                                                                                               1:-1],
                                                                                                               '%d/%b/%Y:%H:%M:%S %z'))]
        average_response_size_time, count_errors_time = statistics(logs)
except FileNotFoundError:
    exit('Файл не найден')
except PermissionError:
    exit('Ошибка доступа')
results = open('result.txt', 'w', encoding='windows-1251')
results.writelines(
    [f'Средний размер ответа по коду состояния: {average_response_size}\n', f'Количество ошибок: {count_errors}\n',
     f'Статистика с {time_start[1:-1]} до {time_end[1:-1]}\n',
     f'Средний размер ответа по коду состояния: {average_response_size_time}\n',
     f'Количество ошибок: {count_errors_time}\n'])
