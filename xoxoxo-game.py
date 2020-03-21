#!/usr/bin/env python

GAME_NAME = "❌⭕❌⭕❌⭕"

ROWS = list("abcdefghij")
COLUMNS = [i for i in range(1,11)]

CELL_EMPTY = "E"
CELL_X = "X"
CELL_O = "O"

PLAYER_SYMBOLS = {1: 'X', 2: 'O'}

current_player = 1
winner = 0
board_state = dict()

def print_welcome_message():
    print()
    print("👋 Welcome to {}!".format(GAME_NAME))
    print()

def draw_board():
    global board_state
    BOARD_HEAD_BORDER = "┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐"
    BOARD_SEPARATOR   = "├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤"
    BOARD_FOOT_BORDER = "└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘"
    BOARD_ROW          = "│ {} │   │   │   │   │   │   │   │   │   │   │"
    BOARD_HEADER = BOARD_HEAD_BORDER + "\n" + \
                   "│   │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 10│\n" + \
                   BOARD_SEPARATOR

    print(BOARD_HEADER) 
    for r_index, r in enumerate(ROWS):
        print("│ {} │".format(r), end='')
        for c_index, c in enumerate(COLUMNS):
            if c_index < len(COLUMNS) - 1:
                print(" {} │".format(format_cell_content(board_state[r][c])), end = '')
            else:
                print(" {} │".format(format_cell_content(board_state[str(r)][c])))
        if r_index < len(ROWS)-1:
            print(BOARD_SEPARATOR)
    print(BOARD_FOOT_BORDER) 
    print()

def format_cell_content(cell_content):
    if cell_content == CELL_EMPTY:
        return ' '
    elif cell_content == CELL_O:
        return 'O'
    elif cell_content == CELL_X:
        return 'X'

def print_players():
    print("👉  Player 1: {}".format(get_player_symbol(1)))
    print("👉  Player 2: {}".format(get_player_symbol(2)))
    print("👉  Current player: {}".format(current_player))
    print("👉  Select move example: 'a1' means row a, column 1. 'd7' means row d column 7.")
    print("👉  Type 'exit' and press enter to quit the game.")
    print("👉 (Enter the input without the apostrophes.)")

def get_move():
    return input("❓ Move: ")

def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True

def user_wants_to_exit(move):
    if move == 'exit':
        return True
    return False

def validate_move(move):
    move_list = list(move)
    if len(move_list) < 2:
        print("❗ Wrong format: length of {} is lower than 2".format(move))
        return False
    elif len(move_list) > 3:
        print("❗ Wrong format: length of {} is larger than 3".format(move))
        return False
    elif move_list[0] not in ROWS:
        print("❗ Wrong format: row '{}' does not exist".format(move_list[0]))
        return False
    else:
        if len(move_list) == 2 and not is_int(move_list[1]):
            print("❗ Wrong format: column '{}' is invalid".format(move_list[1]))
            return False
        elif len(move_list) == 2 and int(move_list[1]) not in COLUMNS:
            print("❗ Wrong format: column '{}' does not exist".format(move_list[1]))
            return False
        elif len(move_list) == 3 and not is_int(''.join(move_list[1:3])):
            print("❗ Wrong format: column '{}' is invalid".format(''.join(move_list[1:3])))
            return False
        elif len(move_list) == 3 and int(''.join(move_list[1:3])) not in COLUMNS:
            print("❗ Wrong format: column '{}' does not exist".format(''.join(move_list[1:3])))
            return False
        else:
            move_r = move_list[0]
            if len(move_list) == 2: 
                move_c = int(move_list[1])
            else: 
                move_c = int(''.join(move_list[1:3]))
            if board_state[move_r][move_c] != CELL_EMPTY:
                print("❗ Cell '{}' is already occupied".format(move))
            else:
                return True

def initialize_board():
    for r in ROWS:
        board_state[r] = dict()
        for c in COLUMNS:
            board_state[r][c] = CELL_EMPTY

def update_board(move):
    global current_player
    move_list = list(move)
    if len(move_list) == 2:
        board_state[move_list[0]][int(move_list[1])] = get_player_symbol(current_player)
    else:
        board_state[move_list[0]][int(''.join(move_list[1:3]))] = get_player_symbol(current_player)
    return

def is_game_ended():
    # Check player 1
    if is_winner(1):
        set_winner(1)
        return True
    elif is_winner(2):
        set_winner(2)
        return True
    else:
        return False

def is_winner(player):
    player_symbol = get_player_symbol(player)
    for r in ROWS:
        subsequent_player_symbols = 0
        for c in COLUMNS:
            if board_state[r][c] == player_symbol:
                subsequent_player_symbols += 1
                if c+4<=len(COLUMNS) and board_state[r][c+4] == player_symbol:
                    subsequent_player_symbols += 1
                    if board_state[r][c+3] == player_symbol:
                        subsequent_player_symbols += 1
                        if board_state[r][c+2] == player_symbol:
                            subsequent_player_symbols += 1
                            if board_state[r][c+1] == player_symbol:
                                subsequent_player_symbols += 1
                if subsequent_player_symbols == 5:
                    return True
    for c in COLUMNS:
        subsequent_player_symbols = 0
        for r_index, r in enumerate(ROWS):
            if board_state[r][c] == player_symbol:
                subsequent_player_symbols += 1
                if r_index+4<=len(ROWS) and board_state[ROWS[r_index+4]][c] == player_symbol:
                    subsequent_player_symbols += 1
                    if board_state[ROWS[r_index+3]][c] == player_symbol:
                        subsequent_player_symbols += 1
                        if board_state[ROWS[r_index+2]][c] == player_symbol:
                            subsequent_player_symbols += 1
                            if board_state[ROWS[r_index+1]][c] == player_symbol:
                                subsequent_player_symbols += 1
                if subsequent_player_symbols == 5:
                    return True
    return False

def set_winner(w):
    global winner
    winner = w

def update_current_player():
    global current_player
    if current_player == 1:
        current_player = 2
    else:
        current_player = 1

def get_player_symbol(player):
    return PLAYER_SYMBOLS[player]

def start_game():
    print_welcome_message()
    initialize_board()
    while(not is_game_ended()):
        draw_board()
        print_players()
        is_valid_move = False
        while not is_valid_move:
            move = get_move()
            if user_wants_to_exit(move):
                print("👋 Bye!")
                return
            is_valid_move = validate_move(move)
        update_board(move)
        update_current_player()
    print("🏆 Game ended.")
    print()
    print("🏆🏆🏆🏆🏆🏆🏆🏆")
    print("┌──────────────┐")
    print("│  Game Over   │")
    print("│ Winner is: {} │".format(winner))
    print("└──────────────┘")
    print("🏆🏆🏆🏆🏆🏆🏆🏆")
    print()
    draw_board()
    return

if __name__ == "__main__":
    start_game()