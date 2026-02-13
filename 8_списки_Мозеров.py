#1
product = ["торт", 1]
print(product)

#2
household_chemicals = [["стиральный порошок",1], ["средство для мытья посуды", 1]]
print(household_chemicals)

#3
names = ["Ben", "Holly", "Ann"]
dogs_names = ["Sharik", "Gab", "Beethoven"]
names_and_dogs_names = zip(names, dogs_names)
list_of_names_and_dogs_names = list(names_and_dogs_names)
print(list_of_names_and_dogs_names)

#4
orders=['маргаритки', 'васильки']
orders.append("тюльпаны")
orders.append("розы")
print(orders)

#5
orders = ['маргаритка', "лютик", "львиный зев", "гардения", "лилия"]
new_orders = orders + ["сирень", "ирис"]
broken_prices = [5, 3, 4, 5, 4] + [4]
print(new_orders, broken_prices)

#6
list1=[1, 8]
list1=range(9)
print(list(list1))
list2=range(7)
print(list(list2))


#7
list1= range(6,15,2)
list1=range(5,16,3)
print(list(list1))

list2= range(0,40,5)
print(list(list2))

#8
first_names = ["Эйнсли", "Бен", "Чани", "Депак"]
age=[]
age.append(42)
all_ages = [32, 41, 29] + age
name_and_age= zip(first_names, all_ages)
ids = range(0,3)
name_and_ages_and_ids= zip(name_and_age, list(ids))
print(list(name_and_ages_and_ids))