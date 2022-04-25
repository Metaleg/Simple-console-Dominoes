from random import shuffle


class Dominoes:
    count = 0
    stock = []
    snake = []
    status = None
    player_set = []
    computer_set = []

    def __new__(cls):  # for using singleton
        if cls.count == 0:
            cls.count += 1
            return object.__new__(cls)

    def __init__(self):
        while True:
            self.generate_full_set()
            shuffle(self.stock)
            if self.init_game():
                break

    def generate_full_set(self):
        temp_set = set()
        for i in range(7):
            for j in range(7):
                if j not in temp_set:
                    self.stock.append([i, j])
            temp_set.add(i)

    def generate_player_set(self):
        return [self.stock.pop() for _ in range(7)]

    def init_game(self):
        self.player_set = self.generate_player_set()
        self.computer_set = self.generate_player_set()
        for i in range(6, -1, -1):
            if [i, i] in self.player_set:
                self.snake.append([i, i])
                self.player_set.remove([i, i])
                self.status = 'computer'
                return True
            if [i, i] in self.computer_set:
                self.snake.append([i, i])
                self.computer_set.remove([i, i])
                self.status = 'player'
                return True
        return False

    def print_status(self):
        print('=' * 70, f'Stock size: {len(self.stock)}',
              f'Computer pieces: {len(self.computer_set)}\n', sep='\n')
        if len(self.snake) <= 6:
            print(f"{''.join([str(i) for i in self.snake])}\n")
        else:
            print(f"{''.join([str(i) for i in self.snake[:3]])}"
                  + "..."
                  + f"{''.join([str(i) for i in self.snake[-3:]])}\n")
        print("Your pieces:\n" +
              '\n'.join([f'{i + 1}:{str(self.player_set[i])}' for i in range(len(self.player_set))]), '\n')

        message = 'Status: '
        if self.status == 'player':
            message += "It's your turn to make a move. Enter your command."
        elif self.status == 'computer':
            message += "Computer is about to make a move. Press Enter to continue..."
        elif self.status == 'player_won':
            message += "The game is over. You won!"
        elif self.status == 'computer_won':
            message += "The game is over. The computer won!"
        elif self.status == 'draw':
            message += "The game is over. It's a draw!"
        print(message)

    def play(self):
        while True:
            self.print_status()
            if self.status == 'player':
                while True:
                    user_input = input()
                    if self.check_user_input(user_input) and self.check_option(int(user_input), self.player_set):
                        break
                user_input = int(user_input)

                self.reorient(user_input, self.player_set)
                self.make_move(self.player_set, user_input)
                self.status = 'computer'
            elif self.status == 'computer':
                input()
                option = self.make_choice()
                self.reorient(option, self.computer_set)
                self.make_move(self.computer_set, option)
                self.status = 'player'
            else:
                break
            self.check_game_status()

    def check_user_input(self, user_input):
        if len(user_input) == 1 and user_input.isdigit():
            if int(user_input) <= len(self.player_set):
                return True
        elif len(user_input) == 2 and user_input[1].isdigit():
            if user_input[0] == '-' and abs(int(user_input[1])) <= len(self.player_set):
                return True
        else:
            print("Invalid input. Please try again.")
            return False

    def make_move(self, pieces, option):
        if option > 0:
            self.snake.append(pieces.pop(option - 1))
        elif option < 0:
            self.snake.insert(0, pieces.pop(abs(option) - 1))
        elif len(self.stock) != 0:
            pieces.append(self.stock.pop())

    def check_game_status(self):
        if len(self.player_set) == 0:
            self.status = 'player_won'
            return
        elif len(self.computer_set) == 0:
            self.status = 'computer_won'
            return

        ends = set(self.snake[0]) & set(self.snake[-1])
        if ends:
            ends = ends.pop()
            cnt = 0
            for i in self.snake:
                cnt += i.count(ends)
            if cnt == 8:
                self.status = 'draw'

    def check_option(self, option, pieces):
        if option > 0 and self.snake[-1][1] in (pieces[option - 1][0], pieces[option - 1][1]):
            return True
        elif option < 0 and self.snake[0][0] in (pieces[abs(option) - 1][0], pieces[abs(option) - 1][1]):
            return True
        elif option == 0:
            return True
        if self.status != 'computer':
            print('Illegal move. Please try again.')
        return False

    def reorient(self, option, pieces):
        if option > 0 and self.snake[-1][1] != pieces[option - 1][0]:
            pieces[option - 1][0], pieces[option - 1][1] = pieces[option - 1][1], pieces[option - 1][0]
        elif option < 0 and self.snake[0][0] != pieces[abs(option) - 1][1]:
            pieces[abs(option) - 1][0], pieces[abs(option) - 1][1] = \
                pieces[abs(option) - 1][1], pieces[abs(option) - 1][0]

    def make_choice(self):
        nums = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for i in self.computer_set + self.snake:
            for j in range(7):
                nums[j] += i.count(j)

        pieces = dict()
        for i in range(len(self.computer_set)):  # count a score
            pieces[i] = nums[self.computer_set[i][0]] + nums[self.computer_set[i][1]]
        sorted_keys = sorted(pieces, key=pieces.get, reverse=True)
        sorted_pieces = {i: pieces[i] for i in sorted_keys}

        for i in sorted_pieces:
            if self.check_option(i + 1, self.computer_set):
                return i + 1
            if self.check_option(-(i + 1), self.computer_set):
                return -(i + 1)
        return 0


domino = Dominoes()
domino.play()
