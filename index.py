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

class Game():
    def __init__(self):
        count = 6
        people = [Person() for i in range(count)]

# class Rule(Enum):
#     I_dont_want_this_food = auto()
#     Nobody_wants_this_food = auto()
#     My_neighbors_both_food = auto()
#     Everybody_else_wants_food = auto()
#     Im_the_only_one_who_wants_food = auto()

class Person:
    def __init__(self):
        # f = lambda xs :random.choice(list(xs))

        self.rule = None
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
    
    # remove dislike foods
    def dislike(self, foodList):
        for food in foodList:
            if self.drink in food:
                self.drink.remove(food)
            if self.dish in food:
                self.dish.remove(food)
            if self.dessert in food:
                self.dessert.remove(food)
            

# print(repr(Person()))

# 디코 봐주세요

# 네 잘 되네요 일단

# 근데 보니까 규칙을 먼저 만든 다음에 그에 맞춰 메뉴를 정하는 편이 쉬워보이네요
# 많이 어렵겠는데요 ㅋㅋㅋㅋㅋㅋㅋㅋㅋ 감도 안잡히네 

# 정답이 하나만 나오게 해야하니까 흠 
# 규칙은 인당 하나씩 말하는거 맞죠?
# 규칙을 랜덤하게 6개 정했을 때 경우의 수가 한 가지만 나오는 함수를 짜야겠네요 ㅋㅋㅋㅋ 수학적으로 계산하다보면 알고리즘은 많이 안 어려울지도?
# 일단 명세는 6명이 각각 한 가지의 조건을 말했을 때, 3가지 메뉴가 정해지는 조건의 조합인데 readme에서 조건을 좀 나눠볼게요