import random


def start_game():
    order = first_settings_set()
    gaming_field = generate_empty_field()
    show_field(gaming_field)
    order_making(gaming_field, order)


def first_settings_set():
    sides = sides_choosing()
    order = who_is_first_choosing(sides)
    return order


def sides_choosing():
    pl1 = ""
    pl2 = ""
    i = False
    while not i:
        pl1 = input("First player - which symbol do you choose? X or O: ").upper()
        if pl1 == 'X':
            pl2 = 'O'
            print(f"First player will be - {pl1}, and Second - {pl2}")
            i = True
        elif pl1 == 'O':
            pl2 = 'X'
            print(f"First player will be - {pl1}, and Second - {pl2}")
            i = True
        else:
            print("Wrong symbol, try again")
    players_symbols = dict(pl1=f"{pl1}", pl2=f"{pl2}")
    return players_symbols


def who_is_first_choosing(sides):
    players_pos = dict()
    rnd = random.Random()
    ii = False
    i = False
    while not ii:
        while not i:
            pl1_input = input("First player, please enter number form 0 to 100: ")
            if pl1_input.isdigit() and 0 < int(pl1_input) <= 100:
                pl1_input = int(pl1_input)
            else:
                print("Try again (not a number or not in a range)")
                continue
            pl2_input = input("Second player, please enter number form 0 to 100: ")
            if pl2_input.isdigit() and 0 < int(pl2_input) <= 100:
                pl2_input = int(pl2_input)
                ii = True
            else:
                print("Try again (not a number or not in a range)")

            number = rnd.randrange(101)
            print(f"First player - {pl1_input}, Second player - {pl2_input}, Random number - {number}")
            if abs(number - pl1_input) < abs(number - pl2_input):
                players_pos = {'first move': sides['pl1'], 'second move': sides['pl2']}
                print("First player closer to random number - first move")
                i = True
            elif abs(number - pl1_input) == abs(number - pl2_input):
                continue
            else:
                players_pos = {'first move': sides['pl2'], 'second move': sides['pl1']}
                print("Second player closer to random number - first move")
                i = True
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


def order_making(field, order):
    total_moves = len(field) * len(field[0])
    i = 1
    while i <= total_moves:
        if i % 2 != 0:
            print(f"now {order['first move']} is making move")
            making_a_move(field, order['first move'])
            if game_status_checking(field, order['first move']):
                break
            show_field(field)
            i += 1
        else:
            print(f"now {order['second move']} is making move")
            making_a_move(field, order['second move'])
            if game_status_checking(field, order['second move']):
                break
            show_field(field)
            i += 1


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


start_game()
