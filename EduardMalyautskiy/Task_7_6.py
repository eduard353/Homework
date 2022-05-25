from Task_7_5 import *


def isprime(number):
    i = 2
    while (i < number):
        if number % i == 0:
            return False
        i += 1
    return True

def goldbach(number):
    for i in range(2, number):
        if isprime(i) and isprime(number-i):
            print(number, '=', i, '+', number-i)
            return True
    return False

def get_value():
    print('\nГипотеза Гольдбаха: Любое четное число больше 2 можно записать как сумму двух простых чисел.')
    my_num = input("Введите четное число для проверки или символ 'q' для выхода из программы : ")
    return my_num


def main_prog():
    while True:
        my_num = get_value()
        if my_num == 'q':
            print('Работа программы завершена\n\n')
            break
        else:
            try:
                my_num = int(my_num)
            except ValueError as ex:
                print('Вы ввели недопустимые символы, введите четное число. \n')
                continue
        if check_even(my_num):
            goldbach(my_num)
        else:
            print('Введено нечетное число, попробуйте снова. \n')

