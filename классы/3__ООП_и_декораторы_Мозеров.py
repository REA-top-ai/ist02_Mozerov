def is_alive(func):
    def wrapper(*args, **kwargs):
        hero = args[0]
        if hero.health <= 0:
            print(f'{hero.name} мёртв и не может действовать!')
            return None
        return func(*args, **kwargs)
    return wrapper

def log_action(func):
    def wrapper(*args, **kwargs):
        print(f'[LOG] Начало действия: {func.__name__}')
        result = func(*args, **kwargs)
        print('[LOG] Действие завершено')
        return result
    return wrapper

# Увеличиваем здоровье и ману на время ивента
def bonus(func):
    def wrapper(*args, **kwargs):
        hero = args[0]

        old_health = hero.health
        old_mana = hero.mana

        hero.health = hero.health * 2
        hero.mana = hero.mana * 1.5

        result = func(*args, **kwargs)

        hero.health = old_health
        hero.mana = old_mana
        return result
    return wrapper

# Добавляем бонусный предмет на время ивента
def item_bonus(func):
    def wrapper(*args, **kwargs):
        hero = args[0]
        if hero.hero_class == 'Волшебник':
            old_mana = hero.mana
            hero.items['Священный посох'] = {'mana': 5}
            hero.mana += 5

            result = func(*args, **kwargs)

            hero.mana = old_mana
            del hero.items['Священный посох']
            return result
        return func(*args, **kwargs)
    return wrapper

# Декоратор "Двойной урон" - временно увеличивает урон героя в 2 раза
def double_damage(func):
    def wrapper(*args, **kwargs):
        hero = args[0]
        damage = args[1]

        new_damage = damage * 2

        return func(hero, new_damage)

    return wrapper

class Hero:
    def __init__(self, name, hero_class):
        self.name = name
        self.hero_class = hero_class

        if self.hero_class == 'Волшебник':
            self.health = 60
            self.mana = 50
        elif self.hero_class == 'Воин':
            self.health = 100
            self.mana = 10
        else:
            raise ValueError('Такого класса не существует!')

        self.spells_names = {}
        self.items = {}

    @is_alive
    def attack(self, damage):
        print(f'Герой нанес урон: {damage}')

    @log_action
    def heal(self, amount):
        self.health += amount
        print(f'Герой восстановил {amount} здоровья. Сейчас хп: {self.health}')

    @is_alive
    def cast_spell(self, spell_name):
        spell = self.spells_names[spell_name]
        self.mana -= spell['mana_cost']
        print(spell_name)
    def add_spell(self, spell_name, mana_cost, attack_damage, health_increase):
        self.spells_names[spell_name] = {
            'mana_cost': mana_cost,
            'attack_damage': attack_damage,
            'health_increase': health_increase
        }
    def add_item(self, item_name, parameter, value):
        if len(self.items) < 6:
            self.items[item_name] = {parameter: value}

    @bonus
    def easter_event(self):
        print(f'{self.name}: Здоровье = {self.health}, мана = {self.mana}')

    @item_bonus
    def bonus_item(self):
        print(f'{self.name}: мана = {self.mana}')

    @double_damage
    def strong_attack(self, damage):
        print(f"Герой нанес урон: {damage}")
