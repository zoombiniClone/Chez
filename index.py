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
    name_list = ["I", "everybody", "everybody else", "neighbors", "left", "right", "edge"]
    return name_list[target_type]

def get_rule_name(rule_type):
    name_list = ["like", "hate"]
    return name_list[rule_type]

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
    
    target_type = random.choice(target_type_list)

    set_rule_list = [0, 1]

    rule_type = random.choice(set_rule_list)

    # wrong test case 1
    # [Dish.Salad] everybody like Salad
    # [Dish.Salad] I like Salad
    # [Dish.Salad]

    # wrong test case 2 - solve
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] I like Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] everybody like Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]

    # wrong test case 3
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] everybody unlike Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] I unlike Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]

    # right test case 4
    # [Dish.Salad]
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] Neighbors like Salad
    # [Dish.Salad]
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] Neighbors like Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]

    # wrong test case 5 - solve
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] everybody like Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] I hate Fish

    # right test case 6
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] Neighbors unlike Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]
    # [Dish.Fish, Dish.Salad, Dish.Sandwich] Neighbors unlike Salad
    # [Dish.Fish, Dish.Salad, Dish.Sandwich]
    

    

    candidates = [list(Drink), list(Dish), list(Dessert)]
    
    menu = None

    match rule_type:
        case 0: #like
            # todo : 후보군 모두 좋아하는 것이 정해졌을 때 예외처리
            for target in get_target(target_type, index, game.count):
                likes = game.people[target].get_like()
                dislikes = game.people[target].get_dislike()

                for i in range(3):
                    like = likes[i]
                    dislike = dislikes[i]
                    candidate = candidates[i]

                    # 후보군 중 하나라도 싫어하는 메뉴들은 제거
                    if dislike in candidate:
                        candidate.remove(dislike)
                    # 후보군 중 하나라도 좋아하는 것이 정해졌을 때 좋아하는 리스트로 선정되는 것 방지
                    if len(like) == 1 and like in candidate:
                        candidate.remove(like)
            
            menu = random.choice(random.choice(candidates))
            # menu = random.choice(candidates[1])

            for index in get_target(target_type, index, game.count):
                game.people[index].set_like([menu])
                
        case 1: #hate
            # todo : 후보군 모두 싫어하는 메뉴는 제거
            for target in get_target(target_type, index, game.count):
                likes = game.people[target].get_like()
                dislikes = game.people[target].get_dislike()

                for i in range(3):
                    like = likes[i]
                    dislike = dislikes[i]
                    candidate = candidates[i]

                    # 후보군 중 하나라도 좋아하는 게 정해졌을 때 그 메뉴의 모든 경우의 수 제거
                    if len(like) == 1 and like in candidate:
                        candidate.remove(like)
                        if dislike in candidate:
                            candidate.remove(dislike)
                
            menu = random.choice(random.choice(candidates))
            # menu = random.choice(candidates[1])
            

            for index in get_target(target_type, index, game.count):
                game.people[index].set_dislike([menu])

    
    return (target_type, rule_type, menu)


class Person:
    def __init__(self, index = -1):
        self.index = index
        self.rules = []
        self.drink = list(Drink)
        self.dish = list(Dish)
        self.dessert = list(Dessert)
    
    # log what person want and rules
    def __repr__(self):
        drink = self.drink[0] \
            if len(self.drink) == 1 else "undefined"
        dish = self.dish[0] \
            if len(self.dish) == 1 else "undefined"
        dessert = self.dessert[0] \
            if len(self.dessert) == 1 else "undefined"
        return f"{drink}, {dish}, {dessert} /\
 {[(get_target_name(rule[0]), get_rule_name(rule[1]), rule[2]) for rule in self.rules]}"
    
    def get_like(self):
        return [self.drink, self.dish, self.dessert]
    
    def get_dislike(self):
        drink = [d for d in list(Drink) if not d in self.drink]
        dish = [d for d in list(Drink) if not d in self.dish]
        dessert = [d for d in list(Drink) if not d in self.dessert]
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
        

class Game:
    def __init__(self):
        self.count = 6
        self.people = [Person(i) for i in range(self.count)]

        def get_min_rule_people(people):
            candidates = []
            diff = 0
            for person in people:
                if candidates:
                    diff = len(person.get_rule()) - len(candidates[0].get_rule())
                    if diff < 0:
                        candidates.clear()
                if not candidates or diff == 0:
                    candidates.append(person)
            
            return random.choice(candidates)


        for _ in range(2):
            person = get_min_rule_people(self.people)
            person.add_rule(rule(self, person.index))

        # while True:
        #     person = get_min_rule_people(self.people)
        #     if not person.add_rule(rule(self, person.index, random.choice(set_rule_list))):
        #         break
        
        for person in self.people:
            print(person)

Game()


