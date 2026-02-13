#1
list1 = range(2, 20, 2)
list1_len=len(list1)
print(list1_len)
list1=range(2,20,3)
list1_len=len(list1)
print(list1_len)

#2
shopping_list = ['яйца', "масло","молоко","огурцы","сок","хлопья"]
last_element = shopping_list[-1]
element5 = shopping_list[5]
print(element5, last_element)


#3
suitcase = ['рубашка', "рубашка", "брюки","брюки","пижамы","книги"]
beginning=suitcase[0:2]
print(beginning)
print(len(beginning))
beginning=suitcase[0:4]
print(beginning)
middle=beginning[(len(suitcase)//2-1):(len(suitcase)//2+2)]
print(middle)

#4
suitcase = ['рубашка',"футболка","носки","очки","пижама","книги"]
start = suitcase[:3]
print(start)


#5
votes = ["Jake", "Jake", "Laurie", "Laurie", "Laurie", "Jake", "Jake", "Jake", "Laurie",
         "Cassie", "Cassie",
         "Jake", "Jake", "Cassie", "Laurie", "Cassie", "Jake","Jake", 'Cassie', "Laurie"]
jake_votes=votes.count("Jake")
print(jake_votes)

#6
addresses = ['221 B Baker St.', '42 wallaby Way', '12 Grimmauld Place', '742 Evergreen Terrace',
             '1600 Pennsylvania Ave', '10 Downing St.']
addresses.sort()
print(addresses)

#7
games= ["Portal", 'Minecraft', "Pacman",'Tetris',"The Sims","Pokemon"]
games_sorted = sorted(games)
print(games,games_sorted)

#8
inventory =  ['двухспальная кровать', 'двухспальная кровать', 'изголовье'
    , 'двуспальная кровать', 'двуспальная кровать', 'комод', 'комод',
              'стол', 'стол', 'тумбочка', 'тумбочка', 'королевский кровать',
              'двуспальная кровать', 'две односпальные кровати', 'две односпальные кровати',
              'простыни', 'простыни', 'подушка', 'подушка']
inventory_len=len(inventory)
first = inventory[0]
last=inventory[-1]
inventory_2_6= inventory[2:6]
first_3=inventory[:3]
twin_beds = 2*inventory.count('две односпальные кровати')
inventory.sort()
print(first, last, inventory_2_6, first_3, twin_beds, inventory)