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
class Target:
    def __init__(self, game, me, target_type = random.randint(0, 7)):
        self.game = game
        self.me_index = me
        self.count = game.count
        self.target_type = target_type
    
    def get_target_index_list(self):
        match self.target_type:
            case 0:   # I
                return [self.me_index]
            case 1:   # everybody
                return [i for i in range(self.count)]
            case 2:   # everybody else
                return [i for i in range(self.count)].remove(self.me_index)
            case 3:   # neighbors
                if self.me_index == 0 or self.me_index == self.count - 1:
                    raise "Neighbors target_type don't have edge me_index"
                return [self.me_index - 1, self.me_index + 1]
            case 4:   # left
                return [i for i in range(self.me_index - 1)]
            case 5:   # right
                return [i + self.me_index for i in range(self.count - self.me_index)]
            case 6:   # edge
                return [0, self.count - 1]


class Rule:
    def __init__(self, game, target, rule_type = 0):
        self.game = game
        self.target = target
        self.rule_type = rule_type
        # todo : dont overlap menu 
        self.menu = random.choice(random.choice([list(Drink), list(Dish), list(Dessert)]))
        # self.menu = [game.people[i] for i in target.get_target_index_list()]
    
    def set_menu_list(self):
        people = self.game.people
        match self.rule_type:
            case 0: # want
                for index in self.target.get_target_index_list():
                    people[index].set_like([self.menu])
                return True
            case 1: # don't want
                for index in self.target.get_target_index_list():
                    people[index].set_dislike([self.menu])
                return True







# class Rule(Enum):
#     I_dont_want_this_food = auto()
#     Nobody_wants_this_food = auto()
#     My_neighbors_both_food = auto()
#     Everybody_else_wants_food = auto()
#     Im_the_only_one_who_wants_food = auto()

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
    
    def set_like(self, foodList):
        print("test")
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

    def add_rule(self, rule):
        self.rules.append(rule)
    
    def run_rule(self):
        for rule in self.rules:
            rule.set_menu_list()
            

class Game():
    def __init__(self):
        self.count = 6
        self.people = [Person(i) for i in range(self.count)]

        for person in self.people:
            person.add_rule(Rule(self, Target(self, person.index)))
        
        for person in self.people:
            person.run_rule()
        
        for person in self.people:
            print(repr(person))

Game()

# print(repr(Person()))



# 정답이 하나만 나오게 해야하니까 흠 
# 규칙은 인당 하나씩 말하는거 맞죠?
# 규칙을 랜덤하게 6개 정했을 때 경우의 수가 한 가지만 나오는 함수를 짜야겠네요 ㅋㅋㅋㅋ 수학적으로 계산하다보면 알고리즘은 많이 안 어려울지도?
# 일단 명세는 6명이 각각 한 가지의 조건을 말했을 때, 3가지 메뉴가 정해지는 조건의 조합인데 readme에서 조건을 좀 나눠볼게요