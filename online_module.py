#Alan Chen 16976197

from collections import namedtuple
import socket

CFConnection = namedtuple('CFConnection', ['socket', 'input', 'output'])
_SHOW_DEBUG_TRACE = False

class CFProtocolError(Exception):
    '''
    Raised when Connectfour server does not follow protocol
    '''
    pass
class WrongServerError(Exception):
    '''
    Raised when we are connected to a server that does not follow
    connectfour's hello message protocol
    '''
    pass
class ServerInvalidMove(Exception):
    '''
    Raised when the server sends an invalid move to us
    '''
    pass

def connect_to_cf(host: str, port: int) -> CFConnection:
    '''
    Creates a CFConnection named Tuple given a host and port
    '''
    cf_socket = socket.socket()
    cf_socket.connect((host, port))
    cf_input = cf_socket.makefile('r')
    cf_output = cf_socket.makefile('w')
            
    return CFConnection(socket = cf_socket,
                        input = cf_input,
                        output = cf_output)


def disconnect(connection: CFConnection) -> None:
    '''
    Closes the input, output, and socket in that order
    '''
    connection.input.close()
    connection.output.close()
    connection.socket.close()
    if _SHOW_DEBUG_TRACE:
        print('Everything is closed')



def send_player_move(connection, player_move) -> None:
    '''
    Sends the player move to the connectfour server
    '''
    _write_line(connection, player_move)

    
def get_AI_move(connection) -> ['move', 'column']:
    '''
    Reads output from server and determines if output from server is
    following expected protocol. If all goes well, this function
    returns a list that contains the AI's move as a string in index 0 and
    their column as an integer into index 1
    '''
    ai_move = []
    for num in range(3):
        server_response = _read_line(connection).split()
        if num == 0:
            if server_response[0] != 'READY':
                raise CFProtocolError
        if num == 1:
            if server_response[0] != 'OKAY':
                raise CFProtocolError
        if num == 2:
            if server_response[0] == 'DROP' or server_response[0] == 'POP':
                ai_move.append(server_response[0])
                ai_move.append(int(server_response[1])-1)
                if _SHOW_DEBUG_TRACE:
                    print(ai_move)
            else:
                raise CFProtocolError
            
    return ai_move


def check_right_server(connection: CFConnection, username) -> bool:
    '''
    Checks to see if the server we connected to is a connectfour server
    If the server follows the same hello protocl as we would expect
    from the server, function returns True. Otherwise returns False.
    '''
    _write_line(connection, f"I32CFSP_HELLO {username}")
    connection.output.flush()
    reply = _read_line(connection)
    if reply == f"WELCOME {username}":
        if _SHOW_DEBUG_TRACE:
            print(reply)
        return True
    else:
        disconnect(connection)
        raise WrongServerError


            
def _read_line(connection: CFConnection) -> str:
    '''
    Function used to read output from server
    '''
    line = connection.input.readline().rstrip('\n')
    if _SHOW_DEBUG_TRACE:
        print(f"RECIEVED: {line}")
    return line

def _write_line(connection: CFConnection, line: str) -> None:
    '''
    Function used to send strings to server
    '''
    connection.output.write(line + "\r\n")
    connection.output.flush()
    if _SHOW_DEBUG_TRACE:
        print(f"SENT: {line}")

