
class Game :
	
    def __init__ ( self , id ) :
        self.id = id
        self.p1Conn = False
        self.p2Conn = False
        self.turn = 1
        self.p1Moves = set()
        self.p2Moves = set()
        self.winner = None
        self.finish = False
        self.quit = False
        
    def check_winner ( self ) :
        if len(self.p1Moves) >= 3 :
            for row in range(0,3) :
                if (row,0) in self.p1Moves and (row,1) in self.p1Moves and (row,2) in self.p1Moves :
                    self.winner = 1
                    self.finish = True
                    return
            for col in range(0,3) :
                if (0,col) in self.p1Moves and (1,col) in self.p1Moves and (2,col) in self.p1Moves :
                    self.winner = 1
                    self.finish = True
                    return
            if (0,0) in self.p1Moves and (1,1) in self.p1Moves and (2,2) in self.p1Moves :
                self.winner = 1
                self.finish = True
                return
            if (0,2) in self.p1Moves and (1,1) in self.p1Moves and (2,0) in self.p1Moves :
                self.winner = 1
                self.finish = True
                return
                
        if len(self.p2Moves) >= 3 :
            for row in range(0,3) :
                if (row,0) in self.p2Moves and (row,1) in self.p2Moves and (row,2) in self.p2Moves :
                    self.winner = 2
                    self.finish = True
                    return
            for col in range(0,3) :
                if (0,col) in self.p2Moves and (1,col) in self.p2Moves and (2,col) in self.p2Moves :
                    self.winner = 2
                    self.finish = True
                    return
            if (0,0) in self.p2Moves and (1,1) in self.p2Moves and (2,2) in self.p2Moves :
                self.winner = 2
                self.finish = True
                return
            if (0,2) in self.p2Moves and (1,1) in self.p2Moves and (2,0) in self.p2Moves :
                self.winner = 2
                self.finish = True
                return
        if self.check_finish() :    self.winner = -1
                    
    def reset_turn ( self ) :
        self.turn = 1 if self.turn == 2 else 2
        
    def check_finish ( self ) :
        if len(self.p1Moves) + len(self.p2Moves) == 9 :
            self.finish = True
            return True