#1
import datetime
current_time = datetime.datetime.now()
print(current_time)


#2
import random
random_list = [random.randint(1,100) for _ in range(101)]
random_number = random.choice(random_list)


#3
import matplotlib.pyplot as plt
import random
number_a= range(1,13)
number_b = random.sample(range(1000), 12)
plt.plot(number_a, number_b)
plt.show()


#задание 1
from datetime import datetime
def premiya_programmistam(x):
    prem = []
    for sotrudnik in x:
        if "программист" in sotrudnik[1].lower():
            premia = sotrudnik[3] * 0.03
            prem.append([sotrudnik[0], sotrudnik[1], premia])
    return prem


def premiya_k_prazdnikam(x):
    prem8 = []
    prem23 = []

    for sotrudnik in x:
        fio = sotrudnik[0]
        if fio.endswith(('а', 'я')) or 'на' in fio.split()[-1]:
            prem8.append([sotrudnik[0], sotrudnik[1], 2000])
        else:
            prem23.append([sotrudnik[0], sotrudnik[1], 2000])

    return prem8, prem23


def indeksac(x):
    indeksirovannye = []
    current_date = datetime.now()

    for sotrudnik in x:
        date_prem = datetime.strptime(sotrudnik[2], "%d.%m.%Y")
        years_worked = (current_date - date_prem).days / 365

        if years_worked > 10:
            indeks = sotrudnik[3] * 1.07
        else:
            indeks = sotrudnik[3] * 1.05

        indeksirovannye.append([sotrudnik[0], sotrudnik[1], sotrudnik[2], round(indeks)])

    return indeksirovannye


def graf(x):
    grafik = []
    current_date = datetime.now()
    for sotrudnik in x:
        prem = datetime.strptime(sotrudnik[2], "%d.%m.%Y")
        months_worked = (current_date - prem).days / 30
        if months_worked > 6:
            grafik.append([sotrudnik[0], sotrudnik[1], sotrudnik[2]])
    return grafik
employees = [["Иванов Иван Иванович", "Менеджер", "22.10.2013", 250000],
["Сорокина Екатерина Матвеевна", "Аналитик", "12.03.2020", 75000],
["Струквов Иван Сергеевич", "Старший программист", "23.04.2012", 150000],
["Корнеева Анна Игоревна", "Ведущий программист", "22.02.2015", 120000],
["Старчиков Сергей Анатольевич", "Младший программист", "12.11.2021", 50000],
["Бутенко Артем Андреевич", "Архитектор", "12.02.2010", 200000],
["Савченко Алина Сергеевна", "Старший аналитик", "13.04.2016", 100000]]

#задание 2
import random
admin_number = random.randint(1, 9)
print("Загаданное число администрации:", admin_number)
players = []
for i in range(100):
    players.append(random.randint(1, 999))
winners = []
count = 0
for player in players:
    if count >= 5:
        break
    num = player
    summa = 0
    while num > 0:
        summa = summa + (num % 10)
        num = num // 10
    if summa % admin_number == 0:
        winners.append(player)
        print("Выигрышный номер:", player)
        count = count + 1


#задания для самостоятельной работы
import random

# Задание 1
n = int(input("Количесво попыток: "))
print("Результаты бросков монеты:")
for i in range(n):
    coin = random.randint(0, 1)
    if coin == 0:
        print("Орел")
    else:
        print("Решка")
print()

# Задание 2
n = int(input("Количесво попыток: "))
print("Результаты бросков кубика:")
for i in range(n):
    cube = random.randint(1, 6)
    print(cube)
print()

# Задание 3
length = int(input("Длина пароля: "))
password = ""
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(length):
    password = password + random.choice(letters)
print("Случайный пароль:", password)