#Alan Chen 16976197

import connectfour
import shared

def start_local_game() -> None:
    '''
    Local connectfour code. Asks user what size board they
    want then prints empty board with directions on what to
    indicate for moves. Then a loop of asking for their next
    move and printing out the board after the move is executed
    until a someone wins a game.
    '''
    game = shared.new_game_sequence()[0]
    while connectfour.winner(game) == connectfour.EMPTY:
        _player_turn_message(game)
        player_move = shared.get_move(game)
        game = shared.get_next_GameState(game, player_move)
        shared.print_board(game)
        if shared.is_stalemate(game) == True:
            shared.stalemate_message()
            break
        if connectfour.winner(game) == connectfour.RED:
            print('')
            print('---R e d   w o n!---')
        if connectfour.winner(game) == connectfour.YELLOW:
            print('')
            print('---Y e l l o w   w o n!---')
            
def _player_turn_message(GameState: 'GameState') -> None:
    '''
    Prints the current player's turn -> Red or Yellow
    '''
    print(f">It is {_get_player(GameState)}'s turn!")

def _get_player(GameState: 'GameState') -> str:
    '''
    Returns a string stating which player's turn it is
    '''
    if GameState.turn == connectfour.RED:
        return 'Red'
    if GameState.turn == connectfour.YELLOW:
        return 'Yellow'
    
if __name__ == '__main__':
    start_local_game()
