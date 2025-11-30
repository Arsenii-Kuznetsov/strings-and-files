from re import fullmatch, findall

input_string = input('Введите строку, состоящую только из букв латинского алфавита: ')
if not fullmatch('[A-Za-z]+', input_string):
    exit('Строка должна состоять только из букв латинского алфавита')
result_string = ''.join([x[1] + str(len(x[0])) for x in findall(r'((.)\2*)', input_string)])
original_string = ''.join([x[0] * int(x[1]) for x in findall(r'\D\d', result_string)])
if input_string == original_string:
    print('Строки совпадают')
else:
    print('Строки не совпадают')
