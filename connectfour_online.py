#Alan Chen 16976197

import online_module
import shared
import connectfour

def online_game()->None:
    '''
    Starts an online game with a connectfour server, asks the user
    for moves and loops until either the AI wins or Player wins.
    '''
    connection = None
    try:
        connection, user_name = get_connection()
        game, user_col_rows = shared.new_game_sequence()
        online_module.send_player_move(connection, f"AI_GAME {user_col_rows}")
        core_loop(game, connection, user_name)
    except online_module.WrongServerError:
        print_wrong_server_message()
        
    finally:
        if connection != None:
            online_module.disconnect(connection)
            
def core_loop(GameState: 'GameState', connection: online_module.CFConnection, user_name: str) -> None:
    '''
    Core loop of gameplay, repeatedly calss to determin_turn function that will
    determine whos turn it is and will send or recieve moves accordingly. Function
    takes GameState that is returned from determine_turn and prints the board out.
    If any exceptions are raised during the call to determin_turn, those are catched
    here as well. This loop is repeated until a winner is found, a stalemate
    is detected, or an execption is raised.
    '''
    while connectfour.winner(GameState) == connectfour.EMPTY:
            try:
                GameState = determine_turn(connection, GameState, user_name)
                shared.print_board(GameState)
                if shared.is_stalemate(GameState) == True:
                    shared.stalemate_message()
                    break
                if connectfour.winner(GameState) == connectfour.RED:
                    print('')
                    print(f'---{user_name} won!---')
                if connectfour.winner(GameState) == connectfour.YELLOW:
                    print('')
                    print('---AI won!---')
            except online_module.CFProtocolError:
                print_protocol_error_message()
                break
            except online_module.ServerInvalidMove:
                print_invalid_move_error_message()
                break

            
def get_connection() -> (online_module.CFConnection, 'username'):
    '''
    Returns a CFConnection namedtuple that passed the
    hello message protocol of connectfour, and valid username
    together in a tuple of size 2.
    '''
    while True:
        connection = _attempt_connection()
        username = _ask_username()
        if online_module.check_right_server(connection, username) == True:
            print('')
            print('+------------------------------+')
            print('Connected to ConnectFour Server!')
            print("+------------------------------+\n")
            return connection, username


def determine_turn(connection: online_module.CFConnection, GameState: 'GameState', user_name:str) -> 'GameState':
    '''
    This function will send the player's move to the connectfour
    server after they had input their move into the game.
    If it is the AI's turn denoted as YELLOW, then we read the output from
    the server and translate that into a move that can be viewed locally
    '''
    if GameState.turn == connectfour.RED:
        print(f"It is {user_name}'s turn!")
        player_move = shared.get_move(GameState)
        player_move_string = f"{player_move[0]} {player_move[1]+1}"
        next_GameState = shared.get_next_GameState(GameState, player_move)
        online_module.send_player_move(connection, player_move_string)
        return next_GameState
    
    if GameState.turn == connectfour.YELLOW:
        print("It is the AI's turn!\n")
        AI_move = online_module.get_AI_move(connection)
        print(f"---AI's move: {AI_move[0]} {AI_move[1] + 1}--- \n")
        try:
            next_GameState = shared.get_next_GameState(GameState, AI_move)
            return next_GameState
        except connectfour.InvalidMoveError:
            raise online_module.ServerInvalidMove
        except ValueError:
            raise online_module.ServerInvalidMove


def print_protocol_error_message()->None:
    '''
    CFProtocl Error Message, printed when Connectfour server
    does not follow expected protocol during the game
    '''
    print('')
    print('+----------------------------------------------+')
    print('Server did not follow protocol, Disconnecting...')
    print('+----------------------------------------------+\n')
    
def print_wrong_server_message()->None:
    '''
    Message to be printed when a WrongServerError is raised 
    '''
    print('')
    print('+--------------------------------------------------------+')
    print('A connection was made but it was not a connect four server')
    print('Disconnecting...')
    print('+--------------------------------------------------------+\n')

def print_invalid_move_error_message()->None:
    '''
    Printed when an ServerInvalidMove exception is raised
    '''
    print('')
    print('+-------------------------------------------+')
    print('Server gave an invalid move, Disconnecting...')
    print('+-------------------------------------------+\n')

            
def _check_port_input(port: str) -> bool:
    '''
    Returns True if port is an integer
    Returns False otherwise
    '''
    if port.isdigit() == True:
        return True
    else:
        return False
            

def _ask_host_port() -> ('host', 'port'):
    '''
    Asks user for a port, and checks to see if it is valid
    if not, asks user for input again
    '''
    while True:
        user_host = input('Enter connectfour Host address: ').strip()
        user_port = input("Enter it's Port: ").strip()
        if _check_port_input(user_port) == True:
            return user_host, int(user_port)
        else:
            print('')
            print('+------------------------+')
            print('Port can only be integers.')
            print('+------------------------+\n')


def _ask_username() -> str:
    '''
    Asks user for a username, if there's a space
    in between their name or if it is blank a message
    gets printed, and they will be asked for input again
    '''
    while True:
        print('')
        print("+-------------------------------------------------+")
        print('Please indicate a username, spaces are not allowed!')
        print("Example usernames: 'user_name', 'bob123'")
        print("+-------------------------------------------------+\n")
        user_name = input("Username: ")
        if ' ' in user_name:
            print('')
            print("+----------------+")
            print("No spaces allowed!")
            print("+----------------+")
        elif user_name == '':
            print('')
            print("+-----------------------+")
            print("Username cannot be blank!")
            print("+-----------------------+")
        else:
            return user_name

        
def _attempt_connection() -> online_module.CFConnection:
    '''
    Attempts to make a CFConnection named tuple given user's input
    host address and port, if CFConnection is created without exceptions
    raised, function will return a CFConnection namedtuple
    If exceptions are raised, a message is printed and user is asked
    to input a new host and port.
    '''
    while True:
        host_and_port = _ask_host_port()
        host = host_and_port[0]
        port = host_and_port[1]
        try:
            connection = online_module.connect_to_cf(host, port)
            return connection
        except ConnectionRefusedError:
            print('')
            print('+-----------------------------------------------+')
            print("Connection Refused, Try a different host or port.")
            print('+-----------------------------------------------+\n')
        except OverflowError:
            print('')
            print('+---------------------------+')
            print("Ports must be between 0-65535")
            print('+---------------------------+\n')
        except OSError:
            print('')
            print('+--------------+')
            print('No route to host')
            print('+--------------+\n')
                      

if __name__ == '__main__':
    online_game()

