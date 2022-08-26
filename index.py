# 일단은 6명으로 정해놓고 나중에 확장이 쉽게 되게끔 해보죠

# 음료 : 우유, 커피, 오렌지 주스
# 음식 : 샐러드, 빵(샌드위치?), 생선
# 디저트 : 수박, 아이스크림, 과일파이

from enum import Enum, auto
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
                raise "Neighbors target_type don't have edge me_inex"
            return [target_index - 1, target_index + 1]
        case 4:   # left
            if target_index == 0:
                raise "Left edge"
            return [i for i in range(target_index)]
        case 5:   # right
            if target_index == size - 1:
                raise "Right edge"
            return [i + target_index for i in range(size - target_index)]
        case 6:   # edge
            return [0, size - 1]

def get_target_name(target_type):
    name_list = ["I", "everybody", "everybody else", "neighbors", "left", "right", "edge"]
    return name_list[target_type]

def get_rule_name(rule_type):
    name_list = ["like", "hate"]
    return name_list[rule_type]

# todo : convert function
class Rule:
    def __init__(self, game, index, rule_type = 0):
        self.game = game
        # todo : dont have subset rule menu
        target_type_list = list(range(7))

        # neighbors except
        if index == 0 or index == game.count - 1:
            target_type_list.remove(3)
        if index == 0:
            target_type_list.remove(4)
        if index == game.count - 1:
            target_type_list.remove(5)

        self.target_type = random.choice(target_type_list)
        # self.target_type = 0
        self.target_index = index

        self.rule_type = rule_type

        # todo : dont overlap menu, prevent making empty list (ex. I like __ , everybody hate __ => make list empty)

        # wrong test case:
        # I 3 like Dish.Fish
        # right 1 hate Dish.Fish

        self.menu = random.choice(
            random.choice(
                random.choice(
                    [self.game.people[i].get_like() for i in get_target(self.target_type, self.target_index, self.game.count)]
                )
            )
        )
        print(get_target_name(self.target_type), self.target_index, get_rule_name(self.rule_type), self.menu)


    # todo : delete this method & merge rule init function
    def set_menu_list(self):
        people = self.game.people
        match self.rule_type:
            case 0: # want
                for index in get_target(self.target_type, self.target_index, self.game.count):
                    people[index].set_like([self.menu])
                return True
            case 1: # don't want
                for index in get_target(self.target_type, self.target_index, self.game.count):
                    people[index].set_dislike([self.menu])
                return True


class Person:
    def __init__(self, index = -1):
        # f = lambda xs :random.choice(list(xs))
        self.index = index
        self.rules = []
        self.drink = list(Drink)
        self.dish = list(Dish)
        self.dessert = list(Dessert)
    
    # log what person want
    def __repr__(self):
        drink = self.drink[0] \
            if len(self.drink) == 1 else "undefined"
        dish = self.dish[0] \
            if len(self.dish) == 1 else "undefined"
        dessert = self.dessert[0] \
            if len(self.dessert) == 1 else "undefined"
        return f"{drink}, {dish}, {dessert}"
    
    def get_like(self):
        return [self.drink, self.dish, self.dessert]
        # return [
        #     self.drink[0] if len(self.drink) == 1 else None, 
        #     self.dish[0] if len(self.dish) == 1 else None,
        #     self.dessert[0] if len(self.dessert) == 1 else None,
        # ]
    
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
        rule.set_menu_list()
        

class Game:
    def __init__(self):
        self.count = 6
        self.people = [Person(i) for i in range(self.count)]

        def get_min_rule_people(people):
            candidates = []
            for person in people:
                if candidates == [] or len(person.get_rule()) < len(candidates[0].get_rule()):
                    candidates.clear()
                candidates.append(person)
            
            return random.choice(candidates)

        set_rule_list = [0, 1]

        # for _ in range(10):
        #     person = get_min_rule_people(self.people)
        #     Rule(self, person.index, random.choice(set_rule_list))

        for _ in range(2):
            person = get_min_rule_people(self.people)
            person.add_rule(Rule(self, person.index, random.choice(set_rule_list)))
        
        for person in self.people:
            print(person)

Game()


