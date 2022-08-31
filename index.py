from enum import Enum, auto
from itertools import combinations
import random

class Drink(Enum):
    Milk = 1
    Coffee = 2
    OrangeJuice = 3

class Dish(Enum):
    Salad = 1
    Sandwich = 2
    Fish = 3

class Dessert(Enum):
    Watermelon = 1
    Icecream = 2
    Fruitpie = 3

# - I : 0
# - Everybody
# - Everybody else
# - Neighbors 
# - Everybody over left
# - Everybody over right
# - The two person sitting at each edge of the table
def get_target(target_type, target_index, size):
    match target_type:
        case 0:   # I
            return [target_index]
        case 1:   # everybody
            return [i for i in range(size)]
        case 2:   # everybody else
            return [i for i in range(size) if target_index != i]
        case 3:   # neighbors
            if target_index == 0 or target_index == size - 1:
                raise "Neighbors target_type don't have edge me_index"
            return [target_index - 1, target_index + 1]
        case 4:   # left
            if target_index == 0:
                raise "Left edge"
            return [i for i in range(target_index)]
        case 5:   # right
            if target_index == size - 1:
                raise "Right edge"
            return [i + target_index for i in range(1, size - target_index)]
        case 6:   # edge
            return [0, size - 1]

def get_target_name(target_type):
    name_list = ["I", "Everybody", "Everybody else", "Neighbors", "Left", "Right", "Edge"]
    return name_list[target_type]

def get_rule_name(rule_type):
    name_list = ["like", "hate"]
    return name_list[rule_type]

def set_menus(game, candidates, people_menus, targets, rule_type):
    for target in targets:
        likes = game.people[target].get_like()
        dislikes = game.people[target].get_dislike()

        for i in range(3):
            like = likes[i]
            dislike = dislikes[i]
            candidate = candidates[i]

            if rule_type == 0:
                # 후보군 중 하나라도 싫어하는 메뉴들은 제거
                for d in dislike:
                    if d in candidate:
                        candidate.remove(d)

                # 후보군 중 하나라도 좋아하는 것이 정해졌을 때 좋아하는 리스트로 선정되는 것 방지
                if len(like) == 1 and like[0] in candidate:
                    people_menus.append(like[0])
            elif rule_type == 1:
                # 후보군 중 하나라도 좋아하는 게 정해졌을 때 그 메뉴의 모든 경우의 수 제거
                if len(like) == 1 and like[0] in candidate:
                    candidate.remove(like[0])
                    for d in dislike:
                        if d in candidate:
                            candidate.remove(d)
                
                for d in dislike:
                    people_menus.append(d)


def set_target_rule_menu(game, index, target_type, rule_type):
    # 후보군
    candidates = [list(Drink), list(Dish), list(Dessert)]
    menu = None
    targets = get_target(target_type, index, game.count)

    people_menus = []

    set_menus(game, candidates, people_menus, targets, rule_type)

    # all targets like or dislike same menu, then remove element in menus
    menus = [*candidates[0], *candidates[1], *candidates[2]]
    menus = list(filter(lambda m:people_menus.count(m) < len(targets), menus))
    
    if not menus:
        return (None, None)
    
    menu = random.choice(menus)
    
    return (menu, targets)


class Person:
    def __init__(self, index = -1):
        self.index = index
        self.rules = []
        self.drink = list(Drink)
        self.dish = list(Dish)
        self.dessert = list(Dessert)
    
    # log what person want and rules
    def __str__(self):
        drink = self.drink[0] \
            if len(self.drink) == 1 else "undefined"
        dish = self.dish[0] \
            if len(self.dish) == 1 else "undefined"
        dessert = self.dessert[0] \
            if len(self.dessert) == 1 else "undefined"
        return f"{drink}, {dish}, {dessert} / " +\
                ", ".join([f"{get_target_name(rule[0])} {get_rule_name(rule[1])} {str(rule[2])} {str(rule[3])}" for rule in self.rules])
    
    def __repr__(self):
        return ", ".join([f"{get_target_name(rule[0])} {get_rule_name(rule[1])} {str(rule[2])}" for rule in self.rules])

    def get_like(self):
        return [self.drink, self.dish, self.dessert]
    
    def get_dislike(self):
        drink = [d for d in list(Drink) if not d in self.drink]
        dish = [d for d in list(Dish) if not d in self.dish]
        dessert = [d for d in list(Dessert) if not d in self.dessert]
        return [drink, dish, dessert]
    
    def set_like(self, foodList):
        for food in foodList:
            if food in self.drink:
                self.drink.clear()
                self.drink.append(food)
            if food in self.dish:
                self.dish.clear()
                self.dish.append(food)
            if food in self.dessert:
                self.dessert.clear()
                self.dessert.append(food)

    # remove dislike foods
    def set_dislike(self, foodList):
        for food in foodList:
            if food in self.drink:
                self.drink.remove(food)
            if food in self.dish:
                self.dish.remove(food)
            if food in self.dessert:
                self.dessert.remove(food)

    def get_rule(self):
        return self.rules

    def add_rule(self, rule):
        self.rules.append(rule)
        
    def is_set_all_like(self):
        return all([len(like) == 1 for like in self.get_like()])


class Game:
    def __init__(self):
        self.count = 6
        self.people = [Person(i) for i in range(self.count)]

        while self.set_rule():
            pass
    
    def __str__(self):
        return_str = []
        for person in self.people:
            return_str.append(f"{str(person.index + 1)} : {str(person)}.\n")

        return "".join(return_str)

    def __repr__(self):
        return_str = []
        for person in self.people:
            return_str.append(f"{str(person.index + 1)} : {repr(person)}.\n")

        return "".join(return_str)


    def set_rule(self):
        target_type_list = [0, 2, 3, 6]

        set_rule_list = [0, 1]

        rule_list = []

        for index in range(self.count):
            for target in target_type_list:
                # neighbors except
                if target == 3 and (index == 0 or index == self.count - 1):
                    continue
                if target == 4 and index == 0:
                    continue
                if target == 5 and index == self.count - 1:
                    continue

                for rule in set_rule_list:
                    rule_list.append((index, target, rule))
        
        def sort_func(r):
            return len(self.people[r[0]].get_rule()) * 2 + random.random()
        
        rule_list.sort(key=sort_func)

        for rule in rule_list:
            menu, target_list = set_target_rule_menu(self, rule[0], rule[1], rule[2])
            if menu:
                if self.check_subset_rule(target_list, rule[2], menu):
                    continue

                # make it rule enable
                if rule[2] == 0:
                    for index in target_list:
                        self.people[index].set_like([menu])
                elif rule[2] == 1:
                    for index in target_list:
                        self.people[index].set_dislike([menu])
                
                self.people[rule[0]].add_rule((rule[1], rule[2], menu, target_list))  # target, rule, menu
                return  # index, target, rule, menu

    def check_subset_rule(self, target_list, rule_type, menu):
        for (index, rule) in self.get_all_rule():
            is_subset = True
            for sub_target in get_target(rule[0], index, self.count):  # [0, 1]
                if rule[1] == 0:
                    sub_target_likes = self.people[sub_target].get_like()
                    sub_target_like = [like for like in sub_target_likes]
                    sub_target_like_list = [l for l in sub_target_like]

                    if not menu in sub_target_like_list:
                        is_subset = False
                        break
                elif rule[1] == 1:
                    sub_target_dislikes = self.people[sub_target].get_dislike()
                    sub_target_dislike = [dislike for dislike in sub_target_dislikes]
                    sub_target_dislike_list = [d for d in sub_target_dislike]

                    if not menu in sub_target_dislike_list:
                        is_subset = False
                        break
            
            if is_subset:
                return True
                
        return False
    
    def get_all_rule(self):
        return [(person.index, rule) for person in self.people for rule in person.get_rule()]
        

g = Game()

# print(str(g))
# print(repr(g))