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

def get_list_combination(targets):
    if len(targets) <= 1:
        return [targets]
    else:
        l = []
        for i in range(1, len(targets)):
            for ex in combinations(targets, i):
                l.append(list(ex))
        
        random.shuffle(l)

        return l

def get_target_name(target_type):
    name_list = ["I", "everybody", "everybody else", "neighbors", "left", "right", "edge"]
    return name_list[target_type]

def get_rule_name(rule_type):
    name_list = ["like", "hate"]
    return name_list[rule_type]


def set_target_rule_menu(game, index, target_type, rule_type):

    candidates = [list(Drink), list(Dish), list(Dessert)]
    menu = None
    targets = get_target(target_type, index, game.count)

    match rule_type:
        case 0: #like
            all_like_menus = []
            for target in targets:
                likes = game.people[target].get_like()
                dislikes = game.people[target].get_dislike()

                for i in range(3):
                    like = likes[i]
                    dislike = dislikes[i]
                    candidate = candidates[i]

                    # 후보군 중 하나라도 싫어하는 메뉴들은 제거
                    for d in dislike:
                        if d in candidate:
                            candidate.remove(d)

                    # 후보군 중 하나라도 좋아하는 것이 정해졌을 때 좋아하는 리스트로 선정되는 것 방지
                    if len(like) == 1 and like[0] in candidate:
                        all_like_menus.append(like[0])
            
            menus = [*candidates[0], *candidates[1], *candidates[2]]

            # print(targets)
            # print(all_like_menus)
            # print(menus)

            menus = list(filter(lambda m:all_like_menus.count(m) < len(targets), menus))
            
            if not menus:
                return None
            
            menu = random.choice(menus)

            for index in targets:
                game.people[index].set_like([menu])

        case 1: #hate
            all_unlike_menus = []
            for target in targets:
                likes = game.people[target].get_like()
                dislikes = game.people[target].get_dislike()

                for i in range(3):
                    like = likes[i]
                    dislike = dislikes[i]
                    candidate = candidates[i]

                    # 후보군 중 하나라도 좋아하는 게 정해졌을 때 그 메뉴의 모든 경우의 수 제거
                    if len(like) == 1 and like[0] in candidate:
                        candidate.remove(like[0])
                        for d in dislike:
                            if d in candidate:
                                candidate.remove(d)
                    
                    if len(dislike) != 0:
                        for d in dislike:
                            all_unlike_menus.append(d)

            menus = [*candidates[0], *candidates[1], *candidates[2]]

            menus = list(filter(lambda m:all_unlike_menus.count(m) < len(targets), menus))

            if not menus:
                return None

            # print(all_unlike_menus)
            # print(menus)
            
            menu = random.choice(menus)            

            for index in targets:
                game.people[index].set_dislike([menu])

    return menu

def rule(game, index):
    # todo : dont have subset rule menu
    target_type_list = list(range(7))

    # neighbors except
    if index == 0 or index == game.count - 1:
        target_type_list.remove(3)
    if index == 0:
        target_type_list.remove(4)
    if index == game.count - 1:
        target_type_list.remove(5)
    
    set_rule_list = [0, 1]

    target_rule_type_list = []

    for target in target_type_list:
        for rule in set_rule_list:
            target_rule_type_list.append((target, rule))
    
    random.shuffle(target_rule_type_list)

    for target_rule in target_rule_type_list:
        menu = set_target_rule_menu(game, index, target_rule[0], target_rule[1])
        if menu:
            return (target_rule[0], target_rule[1], menu)

    # wrong test case 1 - clear
    # [Dish.Salad] everybody like Salad
    # [Dish.Salad] I like Salad
    # [Dish.Salad]

    # wrong test case 2 - todo 
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] I like Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] everybody like Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]

    # wrong test case 3
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] everybody unlike Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] I unlike Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]

    # right test case 4 - clear
    # [Dish.Salad]
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] Neighbors like Salad
    # [Dish.Salad]
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] Neighbors like Salad
    # [Dish.Salad

    # wrong test case 5 - clear
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] everybody like Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] I unlike Fish

    # right test case 6
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] Neighbors unlike Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] Neighbors unlike Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]


    return None

class Person:
    def __init__(self, index = -1):
        self.index = index
        self.rules = []
        self.drink = list(Drink)
        self.dish = list(Dish)
        self.dessert = list(Dessert)
        print(self)
    
    # log what person want and rules
    def __repr__(self):
        drink = self.drink[0] \
            if len(self.drink) == 1 else "undefined"
        dish = self.dish[0] \
            if len(self.dish) == 1 else "undefined"
        dessert = self.dessert[0] \
            if len(self.dessert) == 1 else "undefined"
        return f"{drink}, {dish}, {dessert} / " +\
                ", ".join([f"{get_target_name(rule[0])} {get_rule_name(rule[1])} {str(rule[2])}" for rule in self.rules])
    
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
        if not rule:
            return None
        self.rules.append(rule)
        return True
        
    def is_set_all_like(self):
        return all([len(like) == 1 for like in self.get_like()])


class Game:
    def __init__(self):
        self.count = 6
        self.people = [Person(i) for i in range(self.count)]

        while True:
            created_rule = self.set_rule()
            if not created_rule:
                break
            
            person = self.people[created_rule[0]]

            for person in self.people:
                print(person)
            print()

            # person = random.choice(self.people)

            # person.add_rule(rule(self, person.index))

            # print()
            # for person in self.people:
            #     print(person)

            # if all([person.is_set_all_like() for person in self.people]):
            #     # todo : remove 
            #     print()
            #     for person in self.people:
            #         print(person)
            #     break
    
    def set_rule(self):
        # todo : dont have subset rule menu

        target_type_list = [0, 3, 6]

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
        
        # random.shuffle(rule_list)

        rule_list.sort(key=sort_func)

        for rule in rule_list:
            menu = set_target_rule_menu(self, rule[0], rule[1], rule[2])
            if menu:
                self.people[rule[0]].add_rule((rule[1], rule[2], menu))
                return (rule[0], rule[1], rule[2], menu)
    
    def get_all_rule(self):
        return [rule for person in self.people for rule in person.get_rule()]
        

# Game()
