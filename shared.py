#Alan Chen 16976197

import connectfour

            
            
def new_game_sequence() -> ('GameState', int):
    '''
    Used at the begginning of each new game, creates
    a new game, prints the empty board and shows the input directions
    '''
    print_input_directions()
    game, user_col_rows = _get_new_game()
    print_board(game)
    print_game_directions(game)
    
    return game, user_col_rows

    
def get_next_GameState(current_GameState: 'GameState', action_col: ('action', int)) -> 'GameState':
    '''
    Returns the next GameState given the move of the player on what column
    if the move is invalid, the InvalidMoveError exception will be catched
    here as well. The Original gamestate will be returned.
    '''
    action = action_col[0]
    column = action_col[1]
    if action == 'DROP':
        next_GameState = connectfour.drop(current_GameState, column)
        return next_GameState
    if action == 'POP':
        next_GameState = connectfour.pop(current_GameState, column)
        return next_GameState

    
def get_move(GameState: 'GameState') -> ('action', int):
    
    '''
    Returns a tuple of size 2 that contains the
    users action(pop or drop), and the column number
    that they want to do said action.
    '''
    while True:
        move = _ask_move()
        action_col = move.split()
        if _check_valid(GameState, action_col) == True:
            action = action_col[0].upper()
            column = int(action_col[1]) - 1
            return action, column


def is_stalemate(GameState: 'GameState') -> bool:
    '''
    Checks for a stalemate by checking to
    see if the board is completely filled by either
    a Red marker or a Yellow marker, if it is
    this function returns True, else returns False
    '''
    num_rows = connectfour.rows(GameState)
    num_col = connectfour.columns(GameState)
    counter = 0
    if num_rows == 1 and num_col == 4:
        return False
    pop_impossible_count = 0
    for row_num in range(num_rows):
        for col_num in range(num_col):
            if GameState.board[col_num][row_num] == connectfour.YELLOW:
                counter += 1
            if GameState.board[col_num][row_num] == connectfour.RED:
                counter += 1
            if GameState.turn == connectfour.RED:
                if row_num == num_rows - 1:
                    if GameState.board[col_num][row_num] != connectfour.RED:
                        pop_impossible_count += 1
            if GameState.turn == connectfour.YELLOW:
                if row_num == num_rows - 1:
                    if GameState.board[col_num][row_num] != connectfour.YELLOW:
                        pop_impossible_count += 1
                        
    if counter == num_rows * num_col and pop_impossible_count == num_col:
        return True
    else:
        return False

    
def stalemate_message()-> str:
    '''
    Message used for Stalemates
    '''
    print('')
    print('---S T A L E M A T E---')


def print_input_directions() ->None:
    print('')
    print('Directions:')
    print('+------------------------------------------+')
    print('The number of columns and rows you input')
    print('must be larger than 0 but no larger than 20.')
    print('+------------------------------------------+\n')

def print_game_directions(GameState: 'GameState') -> None:
    '''
    Prints the directions of how input should be typed
    '''
    print('')
    print('Directions:')
    print('+-------------------------------------------------------+')
    print("-  When it is your turn, please type 'drop' or 'pop'")
    print(f"   followed by a space then a column number from 1 -> {connectfour.columns(GameState)}.")
    print("-  Example: drop 7, Drop 1, drOp 2, PoP 2, pop 19")
    print("- 'drop': drops a piece at the column you indicate.")
    print("- 'pop': removes a colored piece if you have a")
    print("   piece sitting at the last row of your indicated column.")
    print('+--------------------------------------------------------+ \n')
        
def print_board(GameState: 'GameState'):
    '''
    Prints the board out by going through the list found in
    Gamestate.board, 0's are respresented as '.', 1's are
    represented as 'R', and 2's are represented as 'Y'
    '''
    num_rows = connectfour.rows(GameState)
    num_col = connectfour.columns(GameState)
    print(_print_column_labels(num_col))
    
    for row_num in range(num_rows):
        row = ''
        for col_num in range(num_col):
            if GameState.board[col_num][row_num] == connectfour.YELLOW:
                row += 'Y' + '  '
            elif GameState.board[col_num][row_num] == connectfour.RED:
                row += 'R' + '  '
            else:
                row += '.  '
        print(row.strip())

    print(_seperator(num_col)) 

#Private Functions
#Printing the board
def _print_column_labels(columns: int) -> str:
    '''
    Used in print_board(), returns a string of numbers
    that represent the column labels
    '''
    labels = ''
    for col_number in range(1, 1+columns):
        if col_number >= 9:
            labels += str(col_number) + ' '
        else:
            labels += str(col_number) + '  '
        
    return labels.strip()


def _seperator(columns: int) -> str:
    '''
    Used in print_board(), returns a string of
    underscores used for styling the board.
    '''
    seperator = ''
    for col_number in range(1, 1+columns):
        seperator += '___'
    return seperator


#helper functions for starting a game
def _ask_rows_columns() -> str:
    '''
    Used in get_new_game(), asks user their desired board columsn
    and rows,  returns a string that contains the columns and
    rows(in that order), if input was not an iteger a
    message will be printed to the shell.
    '''
    while True:
        game_columns = input('How many columns?: ').strip()
        game_rows = input('How many rows?: ').strip()
        print('')
        if game_columns.isdigit() and game_rows.isdigit():
            columns_and_rows = f"{game_columns} {game_rows}"
            return columns_and_rows
        else:
            print('---columns and rows must be Integers!--- \n')

            
def _create_new_game(game_columns_and_rows: str) -> 'GameState':
    '''
    Used in get_new_game(), attempts to create a
    connectfour.new_game GameState with the columns
    and rows passed to it.
    '''
    columns_and_rows = game_columns_and_rows.split()
    columns = int(columns_and_rows[0])
    rows = int(columns_and_rows[1]) 
    try:
        new_gamestate = connectfour.new_game(columns, rows)
        return new_gamestate
    except ValueError:
        if int(columns) > connectfour.MAX_COLUMNS:
            print('---Too many columns! Max number of columns is 20--- \n')
        if int(columns) < 1:
            print('---Too little columns! Must be greater than 1--- \n')
        if int(rows) > connectfour.MAX_ROWS:
            print('---Too many rows! Max number of rows is 20--- \n')
        if int(rows) < 1:
            print('---Too little rows! Must be greater than 1--- \n')

def _get_new_game() -> ('GameState', 'col_row'):
    '''
    Returns a tuple with a GameState tuple found in
    connectfour.py and the user's board column number.
    '''
    while True:
        columns_rows = _ask_rows_columns()
        new_game = _create_new_game(columns_rows)
        if type(new_game) == connectfour.GameState:
            
            return new_game, columns_rows
        
#Helper functions for getting the next gamestate during a game
def _ask_move() -> str:
    '''
    Used in get_move(), asks the user
    for their next move.
    '''
    move = input('>Pop or Drop?: ')
    print()
    return move

def _check_valid(GameState: 'GameState', user_input: ['move', 'column']) -> bool:
    '''
    Used in get_move(), checks to see if input from _ask_move()
    is formatted correctly, and if the move is valid
    if it is, this function returns True.
    If not a message will be printed to the shell and returns False.
    '''
    if len(user_input) == 2:
        action = user_input[0].upper()
        column = user_input[1]
        if column.isdigit() == True:
            if action == 'POP' or action == 'DROP':
                try:
                    if action == 'DROP':
                        test = connectfour.drop(GameState, int(column)-1)
                        return True
                    if action == 'POP':
                        test = connectfour.pop(GameState, int(column)-1)
                        return True
                except connectfour.InvalidMoveError:
                    print(f"---Invalid Move! Can't do that on column {column}---")
                except ValueError:
                    print(f"---Column {column} not on board!---")
            else:
                print('---Drop or Pop was not indicated--- \n')
                return False
            
        else:
            print('---Column indication was not an Integer!--- \n')
            return False
    else:
        print('---Format not followed!--- \n')
        return False


            
    
    
