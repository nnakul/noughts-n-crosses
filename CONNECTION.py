
import socket
import pickle

class Connection :
    def __init__ ( self, ipv4, port ) :
        self.server = ipv4
        self.port = port
        self.address = ( ipv4, port )
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect ( self ) :
        self.client.connect(self.address)
        return int(self.client.recv(2048).decode()) # player id
        
    def get_game ( self ) :
        self.client.send( str.encode('get') )
        return pickle.loads( self.client.recv(4096) )
        
    def send_move ( self, pos, width, game ) :
        pos = int(pos[0]/width) , int(pos[1]/width)
        if not pos in game.p1Moves and not pos in game.p2Moves :
            self.client.send( str.encode('sending') )
            info = str(pos[0]) + ',' + str(pos[1])
            self.client.send( str.encode(info) )
        
    def reset_turn ( self ) :
        self.client.send( str.encode('reset') )
        
        
