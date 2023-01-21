from collections import Counter


class Game(object):

    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()

    def play(self, player1, player2):
        weight = [[0, 3], [-1, 2]]
        for n in range(self.matches):
            candy_1 = player1.move()
            candy_2 = player2.move()
            self.registry[player1.name()] += weight[candy_1][candy_2]
            self.registry[player2.name()] += weight[candy_2][candy_1]
            player1.remember(candy_2)
            player2.remember(candy_1)
        player1.clear()
        player2.clear()

    def top3(self):
        for i in self.registry.most_common(3):
            print(i[0], ":", i[1])


class Player():

    def __init__(self):
        self.memory = []

    def remember(self, candies):
        self.memory.append(candies)

    def clear(self):
        self.memory.clear()

    def name(self):
        raise NotImplementedError

    def move(self):
        raise NotImplementedError


class Cheater(Player):

    def __init__(self):
        super().__init__()

    def name(self):
        return "Cheater"

    def move(self):
        return 0


class Cooperator(Player):

    def __init__(self):
        super().__init__()

    def name(self):
        return "Cooperator"

    def move(self):
        return 1


class Copycat(Player):

    def __init__(self):
        super().__init__()

    def name(self):
        return "Copycat"

    def move(self):
        if not self.memory:
            return 1
        return self.memory[-1]


class Grudger(Player):

    def __init__(self):
        super().__init__()

    def name(self):
        return "Grudger"

    def move(self):
        if 0 in self.memory:
            return 0
        return 1


class Detective(Player):

    def __init__(self):
        super().__init__()

    def name(self):
        return "Detective"

    def move(self):
        if len(self.memory) in [0, 2, 3]:
            return 1
        elif len(self.memory) == 1:
            return 0
        if 0 in self.memory:
            return self.memory[-1]
        else:
            return 0


if __name__ == "__main__":
    game = Game()
    cooperator = Cooperator()
    cheater = Cheater()
    copycat = Copycat()
    grudger = Grudger()
    detective = Detective()
    characters = [cooperator, cheater, copycat, grudger, detective]

    for n in characters:
        next = characters.index(n) + 1
        while (next < len(characters)):
            game.play(n, characters[next])
            next += 1

    game.top3()
