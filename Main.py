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
    coords = enter_coords(len(field))
    while coords is None:
        coords = enter_coords(len(field))
    if changed_field[coords[0] - 1][coords[1] - 1] == 0:
        if mover == 'X':
            changed_field[coords[0] - 1][coords[1] - 1] = "X"
        else:
            changed_field[coords[0] - 1][coords[1] - 1] = "O"
    elif changed_field[coords[0] - 1][coords[1] - 1] != 0:
        print("There is already something.")
    return changed_field


def enter_coords(field_len):
    coords = list(map(int, input("Enter coords via space: ").split()))
    if coords_verification(coords, field_len):
        print(coords)
        return coords


def coords_verification(coords, field_len):
    if len(coords) != 2:
        print("You need to enter TWO numbers.")
        return False
    elif (coords[0] > field_len or coords[0] < 1) or (coords[1] > field_len or coords[1] < 1):
        print(f"Too big number(or negative). Field is only this long - {field_len}")
        return False
    else:
        return True


def game_status_checking(field, mover):
    if diagonal_win(field, mover):
        return True
    elif diagonal_win(field, mover):
        return True
    elif row_win(field, mover):
        return True
    elif column_win(field, mover):
        return True


# Below is functions that setting a winning rules
def column_win(field, mover):
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


def row_win(field, mover):
    for i in field:
        string_row = ""
        for j in i:
            string_row += str(j)
        if string_row.count(mover) == len(field):
            print(f"{mover} is winner!")
            return True


def diagonal_win(field, mover):
    first_diagonal = ""
    second_diagonal = ""
    for i in range(len(field)):
        for j in range(len(field[i])):
            if j == i:
                first_diagonal += str(field[i][j])
            if (len(field) - 1) - j == i:
                second_diagonal += str(field[i][j])
    if first_diagonal.count(mover) == len(field) or second_diagonal.count(mover) == len(field):
        print(f"{mover} is winner!")
        return True
    return False


if __name__ == '__main__':
    # field1 = [['X', 'X', 'X'], [0, 0, 0], [0, 0, 0]]
    # field2 = [[0, 0, 0], ['X', 'X', 'X'], [0, 0, 0]]
    # field3 = [[0, 0, 0], [0, 0, 0], ['X', 'X', 'X']]
    # print("first row", end=' ')
    # row_win(field1, 'X')
    # print("second row", end=' ')
    # row_win(field2, 'X')
    # print("third row", end=' ')
    # row_win(field3, 'X')
    # print()

    # field1_2 = [['X', 0, 0], ['X', 0, 0], ['X', 0, 0]]
    # field2_2 = [[0, 'X', 0], [0, 'X', 0], [0, 'X', 0]]
    # field3_2 = [[0, 0, 'X'], [0, 0, 'X'], [0, 0, 'X']]
    # print("first column", end=' ')
    # column_win(field1_2, 'X')
    # print("second column", end=' ')
    # column_win(field2_2, 'X')
    # print("third column", end=' ')
    # column_win(field3_2, 'X')
    # print()
    #
    # field1_22 = [['X', 0, 0, 0], ['X', 0, 0, 0], ['X', 0, 0, 0], ['X', 0, 0, 0]]
    # field2_22 = [[0, 'X', 0, 0], [0, 'X', 0, 0], [0, 'X', 0, 0], [0, 'X', 0, 0]]
    # field3_22 = [[0, 0, 'X', 0], [0, 0, 'X', 0], [0, 0, 'X', 0], [0, 0, 'X', 0]]
    # field4_22 = [[0, 0, 0, 'X'], [0, 0, 0, 'X'], [0, 0, 0, 'X'], [0, 0, 0, 'X']]
    # print("first column", end=' ')
    # column_win(field1_22, 'X')
    # print("second column", end=' ')
    # column_win(field2_22, 'X')
    # print("third column", end=' ')
    # column_win(field3_22, 'X')
    # print("fourth column", end=' ')
    # column_win(field4_22, 'X')
    # print()

    # field1_3 = [['X', 0, 0], [0, 'X', 0], [0, 0, 'X']]
    # field2_3 = [[0, 0, 'X'], [0, 'X', 0], ['X', 0, 0]]
    # print("main diagonal", end=' ')
    # diagonal_win(field1_3, 'X')
    # print("secondary diagonal", end=' ')
    # diagonal_win(field2_3, 'X')
    enter_coords(4)
    # start_game()
