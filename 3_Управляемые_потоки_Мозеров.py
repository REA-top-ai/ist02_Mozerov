#1
print((6*6)-1 == 8+1)
print(13 - 7 != (3*2) + 1)
print(3*(2-1) == 4-1)

#2
print((6*6)-1 >= 8+1)
print(13 - 7 <= (3*2) + 1)
print(3*(2-1) > 4-1)

#3
bool_variable = "true"
print(bool_variable, type(bool_variable))
bool_variable_2 = True
print(bool_variable_2, type(bool_variable_2))

#4
user_name = input("Введите имя: ")
Dmitriy_check = 'Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!'
worker_message = "Добро пожаловать"
if user_name == "Дмитрий":
    print(Dmitriy_check)
if user_name != "Дмитрий":
    print(worker_message)

#5
enter_number = 3
if enter_number < 3:
    print(f"Попробуйте еще раз. У вас осталось {3- enter_number}  попыток")
if enter_number >= 3:
    print("Вы превысили максимальное число попыток. Ваша учетная запись заблокирована. Для разблокировки обратитесь в службу поддержки.")

#6
statement_one = (2+2+2 >= 6) and (-1 * -1 < 0)
statement_two = (4*2 <= 8) and (7 - 1 == 6)
print(statement_one, statement_two)

#7
name = input("Введите имя: ")
arm = int(input("Введите APM: "))
if (name == "Дмитрий" and arm == 1) or (name=="Ангелина" and arm == 2) or (name == "Василий" and arm == 3) or (name == "Екатерина" and arm == 4):
    print("Добро пожаловать!")
elif name == "Дмитрий" and arm != 1:
    print("Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!")
else:
    print("Логин или пароль не верный, попробуйте еще раз")

#8
statement_one = (2-1 > 3) or (-5 * 2 == -10)
statement_two = (9+5 <= 15) or (7 != 4+3)
print(statement_one, statement_two)

#9
user_name = input("Введите имя: ")
Dmitriy_check = 'Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!'
worker_message = "Добро пожаловать"
if user_name == "Дмитрий":
    print(Dmitriy_check)
else:
    print(worker_message)

#10
grade = 4.6
if grade >= 4.0:
    print("A")
elif grade >= 3.0:
    print("B")
elif grade >= 2.0:
    print("C")
elif grade >= 1.0:
    print("D")
elif grade >= 0.0:
    print("F")

