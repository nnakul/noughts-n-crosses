
import socket
from _thread import *
import pickle
from game import Game

IPV4 = '***********'    # Fill in appropriate values before running
PORT = ****             # Fill in appropriate values before running
ADDRESS = ( IPV4, PORT )
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

server.listen(2)

print( 'SERVER STARTED !' )
print('WAITING FOR CONNECTIONS ...')

connected = 0
games = {}
count = 0
MAX_CONNECTIONS = 50



def main_threaded(conn, player, gameId) :
    global games, connected
    game = games[gameId]
    
    conn.send( str.encode(str(player)) )
    
    while True :
        try :
            data = conn.recv(2048).decode()
            
            if data == 'get' :
                conn.sendall( pickle.dumps(game) )
                
            elif data == 'sending' :
                move = conn.recv(2048).decode().split(',')
                move = int(move[0]), int(move[1])
                if player == 1 :
                    game.p1Moves.add(tuple(move))
                    game.reset_turn()
                    game.check_winner()
                elif player == 2 :
                    game.p2Moves.add(tuple(move))
                    game.reset_turn()
                    game.check_winner()
                    
            elif data == 'reset' :
                game.reset_turn()
            elif not data :
                break
        except :
            break
    
    connected -= 1
    try :
        game.p1Conn = False
        game.p2Conn = False
        game.quit = True
        del games[gameId]
    except :
        pass
    print('CLIENT DISCONNECTED')
    conn.close()
    


while True :
    conn, addr = server.accept()
    if connected == MAX_CONNECTIONS :
        print('CANNOT BE CONNECTED')
    print( 'CONNECTED TO {}'.format(addr) )
    connected += 1
    
    if connected%2 == 1 :
        games[count] = Game(count)
        count += 1
    
    present_game = count-1
    present_player = 1 if connected%2 == 1 else 2
    
    if connected%2 == 1 :
        games[present_game].p1Conn = True
    else : games[present_game].p2Conn = True
    
    start_new_thread( main_threaded, (conn, present_player, present_game) )
    
    