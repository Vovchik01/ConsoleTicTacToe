import random


def start_game():
    order = first_settings_set()
    gaming_field = generate_empty_field()
    show_field(gaming_field)
    order_making(gaming_field, order)


def first_settings_set():
    order = who_is_first_choosing()
    order_with_symbols = symbols_choosing(order)
    return order_with_symbols


def symbols_choosing(players_order):
    players_symbols = dict()
    key = False
    while not key:
        pl1 = input(f"{players_order[0]} - which symbol do you choose? X or O: ").upper()
        if pl1 == 'X':
            pl2 = 'O'
            print(f"{players_order[0]} will be - {pl1}, and {players_order[1]} - {pl2}")
            players_symbols = dict(first={players_order[0]: pl1}, second={players_order[1]: pl2})
            key = True
        elif pl1 == 'O':
            pl2 = 'X'
            print(f"{players_order[0]} will be - {pl1}, and {players_order[1]} - {pl2}")
            players_symbols = dict(first={players_order[0]: pl1}, second={players_order[1]: pl2})
            key = True
        else:
            print("Wrong symbol, try again")
    return players_symbols


def nickname_input():
    user_input = ""
    key = False
    while not key:
        user_input = input("Please input your nickname (any string without spaces and no 50 symbols longer): ")
        if " " in user_input and len(user_input) > 50 or " " in user_input or len(user_input) > 50:
            print("No-no-no! Try again!")
        else:
            key = True
    return user_input


def input_for_choosing_order(nickname):
    user_input = ""
    key = False
    while not key:
        user_input = input(f"{nickname}, please enter number form 0 to 100: ")
        if user_input.isdigit() and 0 < int(user_input) <= 100:
            user_input = int(user_input)
            key = True
        else:
            print("Try again (not a number or not in a range)")
    return user_input


def who_is_first_choosing():
    players_pos = []
    rnd = random.Random()
    first_player_name = nickname_input()
    second_player_name = nickname_input()
    key = False
    while not key:
        pl1_input = input_for_choosing_order(first_player_name)
        pl2_input = input_for_choosing_order(second_player_name)
        number = rnd.randrange(101)
        print(f"{first_player_name} - {pl1_input}, {second_player_name} - {pl2_input}, Random number - {number}")
        if abs(number - pl1_input) < abs(number - pl2_input):
            print(f"{first_player_name} closer to random number - first move")
            players_pos = [first_player_name, second_player_name]
            key = True
        elif abs(number - pl1_input) == abs(number - pl2_input):
            print("It's a tie. Let's go again")
        else:
            print(f"{second_player_name} closer to random number - first move")
            players_pos = [second_player_name, first_player_name]
            key = True
    return players_pos


def show_field(field):
    for line in field:
        for item in line:
            print(item, end=' ')
        print()


def generate_empty_field():
    field_len = 0
    i = False
    while not i:
        field_len = input("what size of field do you want? (enter one number): ")
        if field_len.isdigit():
            field_len = int(field_len)
            i = True
        else:
            print("Wrong. try again.")
    empty_field = []
    for i in range(field_len):
        line_of_field = [0 for _ in range(field_len)]
        empty_field.append(line_of_field)
    return empty_field


def mover_line(mover, mover_symbol, field):
    print(f"now {mover} is making move")
    making_a_move(field, mover_symbol)
    if game_status_checking(field, mover_symbol):
        show_field(field)
        return True
    show_field(field)
    return False


def order_making(field, order: dict):
    max_possible_moves = len(field) * len(field[0])
    players = list(order.values())
    first_mover = str(list(players[0].keys())[0])
    first_mover_symbol = str(list(players[0].values())[0])
    second_mover = str(list(players[1].keys())[0])
    second_mover_symbol = str(list(players[1].values())[0])
    i = 1
    while i <= max_possible_moves:
        if i % 2 != 0:
            if mover_line(first_mover, first_mover_symbol, field):
                break
            i += 1
        else:
            if mover_line(second_mover, second_mover_symbol, field):
                break
            i += 1

def making_a_move(field, mover):
    changed_field = field
    user_input = list(map(int, input("Enter coords via space: ").split()))
    for item in user_input:
        if item > len(changed_field[0]) or item < 1:
            print(f"Too big number(or negative). Field is only this long {len(changed_field[0])}")

    if changed_field[user_input[0] - 1][user_input[1] - 1] == 0:
        if mover == 'X':
            changed_field[user_input[0] - 1][user_input[1] - 1] = "X"
        else:
            changed_field[user_input[0] - 1][user_input[1] - 1] = "O"
    elif changed_field[user_input[0] - 1][user_input[1] - 1] != 0:
        print("There is already something.")
    return changed_field


def game_status_checking(field, mover):
    if diagonal_win_checking(field, mover, lambda g: g):
        return True
    elif diagonal_win_checking(field, mover, lambda g: (len(field) - 1) - g):
        return True
    elif row_win_checking(field, mover):
        return True
    elif column_win_checking(field, mover):
        return True


def column_win_checking(field, mover):
    counter = 0
    for a in range(len(field)):
        string_column = ""
        for i in range(len(field)):
            for j in range(len(field[i])):
                if j == counter:
                    string_column += str(field[i][j])
        if string_column.count(mover) == len(field):
            print(f"{mover} is winner!")
            return True
    counter += 1


def row_win_checking(field, mover):
    for i in field:
        string_row = ""
        for j in i:
            string_row += str(j)
        if string_row.count(mover) == len(field):
            print(f"{mover} is winner!")
            return True


def diagonal_win_checking(field, mover, rule):
    """ Rule - sets which diagonal will be checking
        Ex. if points where i == j - it's straight diagonal (points in 1:1,2:2,3:3 for 3x3 field)
    """
    string_diagonal = ""
    for i in range(len(field)):
        for j in range(len(field[i])):
            if rule(j) == i:
                string_diagonal += str(field[i][j])
    if string_diagonal.count(mover) == len(field):
        print(f"{mover} is winner!")
        return True
    return False


if __name__ == '__main__':
    start_game()
