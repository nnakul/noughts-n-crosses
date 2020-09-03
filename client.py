
from connection import Connection
from random import randint
import pygame
import time

pygame.init()

CELL_WIDTH = 150
SCREEN_WIDTH = CELL_WIDTH * 3
root = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption('TIC-TAC-TOE')


COLORS = {
            'white' : (255, 255, 255) ,
            'black' : (0, 0, 0) ,
            'red' : (255, 0, 0) ,
            'green' : (0, 255, 0) ,
            'grey' : (47, 79, 79) ,
            'pink' : (255, 20, 147) ,
            'orange' : (255, 69, 0)
         }



def draw_screen( window, game, player ) :
    window.fill(COLORS['white'])
    for pos in game.p1Moves :
        text = 'X'
        custom_font = pygame.font.Font('freesansbold.ttf', 60)
        textsurface = custom_font.render(text, True, COLORS['grey'])
        textrect = textsurface.get_rect()
        textrect.center = pos[0]*CELL_WIDTH + CELL_WIDTH/2 , pos[1]*CELL_WIDTH + CELL_WIDTH/2
        window.blit(textsurface, textrect)
        
    for pos in game.p2Moves :
        text = 'O'
        custom_font = pygame.font.Font('freesansbold.ttf', 60)
        textsurface = custom_font.render(text, True, COLORS['grey'])
        textrect = textsurface.get_rect()
        textrect.center = pos[0]*CELL_WIDTH + CELL_WIDTH/2 , pos[1]*CELL_WIDTH + CELL_WIDTH/2
        window.blit(textsurface, textrect)
        
    for x in ( 0, CELL_WIDTH, CELL_WIDTH*2, CELL_WIDTH*3) :
        pygame.draw.line(window, COLORS['black'], (x,0), (x,SCREEN_WIDTH), 3)
        pygame.draw.line(window, COLORS['black'], (0,x), (SCREEN_WIDTH,x), 3)
        
    if game.quit :
        text = 'OPPONENT DISCONNECTED'
        custom_font = pygame.font.Font('freesansbold.ttf', 30)
        textsurface = custom_font.render(text, True, COLORS['red'])
        textrect = textsurface.get_rect()
        textrect.center = SCREEN_WIDTH/2 , SCREEN_WIDTH/2
        window.blit(textsurface, textrect)
        pygame.display.update()
        return
        
    if game.finish :
        if game.winner == -1 :
            text = 'TIE GAME'
            color = COLORS['green']
        elif game.winner == player :
            text = 'YOU WON'
            color = COLORS['green']
        else :
            text = 'YOU LOST'
            color = COLORS['red']
            
        custom_font = pygame.font.Font('freesansbold.ttf', 60)
        textsurface = custom_font.render(text, True, color)
        textrect = textsurface.get_rect()
        textrect.center = SCREEN_WIDTH/2 , SCREEN_WIDTH/2
        window.blit(textsurface, textrect)
        
    if not ( game.p1Conn and game.p2Conn ) :
        text = 'WAITING...'
        custom_font = pygame.font.Font('freesansbold.ttf', 60)
        textsurface = custom_font.render(text, True, COLORS['grey'])
        textrect = textsurface.get_rect()
        textrect.center = SCREEN_WIDTH/2 , SCREEN_WIDTH/2
        window.blit(textsurface, textrect)
            
    pygame.display.update()
    


def mainOnline(window) :
    conn = Connection('***********', ****)  # Fill in appropriate values before running
    player = conn.connect()
    
    game = None
    run = True
    
    while run :
        game = conn.get_game()
        
        if game.turn == player and not game.finish and game.p1Conn and game.p2Conn and not game.quit :
            pygame.display.set_caption('TIC-TAC-TOE             YOUR TURN')
        elif game.turn != player and not game.finish and game.p1Conn and game.p2Conn and not game.quit :  
            pygame.display.set_caption('TIC-TAC-TOE         OPPONENT\'S TURN')
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.MOUSEBUTTONUP and game.turn == player and not game.finish and game.p1Conn and game.p2Conn and not game.quit :
                conn.send_move( pygame.mouse.get_pos(), CELL_WIDTH, game )
                
        draw_screen(window, game, player)
        if game.quit : 
            run = False
            time.sleep(0.5)
            return
        if game.finish : 
            run = False
            time.sleep(1.5)
            return
    
    pygame.quit()
    


def mainOffline(window) :
    turn = 'c' if randint(0,1) else 'p'
    playerMoves = set()
    computerMoves = set()
    available = set()
    
    for x in range(0,3) :
        for y in range(0,3) :
            available.add((x,y))
    
    run = True
    winner = None
    
    while run :
        draw_screen_offline(window, playerMoves, computerMoves, winner)
        if turn == 'p' : pygame.display.set_caption('TIC-TAC-TOE            YOUR TURN')
        else :  pygame.display.set_caption('TIC-TAC-TOE         COMPUTER\'S TURN')
        
        if turn == 'c' :
            time.sleep(0.5)
            move = optimalMove( playerMoves, computerMoves, available, 'c' )[1]
            if move :
                available.remove(move)
                computerMoves.add(move)
                turn = 'p'
            pygame.event.clear(pygame.MOUSEBUTTONUP) #important

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.MOUSEBUTTONUP and turn == 'p' :
                pos = pygame.mouse.get_pos()
                pos = int(pos[0]/CELL_WIDTH) , int(pos[1]/CELL_WIDTH)
                if pos in available :
                    available.remove(pos)
                    playerMoves.add(pos)
                    turn = 'c'
        
        winner = check_winner( playerMoves, computerMoves )
        if winner or not len(available) :
            run = False
            draw_screen_offline(window, playerMoves, computerMoves, winner)
            time.sleep(2)
            return
        
    pygame.quit()



def main(window) :
    run = True
    
    while run :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.MOUSEBUTTONUP :
                mouse_pos = pygame.mouse.get_pos()
    
                if 60<mouse_pos[0]<160 and 300<mouse_pos[1]<325 :
                    mainOffline(window)
                    pygame.display.set_caption('TIC-TAC-TOE')
                
                if SCREEN_WIDTH-160<mouse_pos[0]<SCREEN_WIDTH-60 and 300<mouse_pos[1]<325 :
                    mainOnline(window)
                    pygame.display.set_caption('TIC-TAC-TOE')
                
        draw_menu(window)
        
    pygame.quit()
 


def draw_menu(window) :
    window.fill(COLORS['white'])
    text = 'TIC - TAC - TOE'
    custom_font = pygame.font.Font('freesansbold.ttf', 50)
    text_surface = custom_font.render(text, True, COLORS['pink'])
    text_rect = text_surface.get_rect()
    text_rect.center = SCREEN_WIDTH/2 , 100
    window.blit(text_surface, text_rect)
    
    mouse_pos = pygame.mouse.get_pos()
    
    if 60<mouse_pos[0]<160 and 300<mouse_pos[1]<325 :
        colorOff = (COLORS['black'], COLORS['orange'])
    else :  colorOff = (COLORS['orange'], COLORS['black'])
    text = 'OFFLINE'
    custom_font = pygame.font.Font('freesansbold.ttf', 32)
    text_surface = custom_font.render(text, True, colorOff[1])
    text_rect = text_surface.get_rect()
    text_rect.center = 110 , 312.5
    window.blit(text_surface, text_rect)
    
    if SCREEN_WIDTH-160<mouse_pos[0]<SCREEN_WIDTH-60 and 300<mouse_pos[1]<325 :
        colorOn = (COLORS['black'], COLORS['orange'])
    else :  colorOn = (COLORS['orange'], COLORS['black'])
    text = 'ONLINE'
    custom_font = pygame.font.Font('freesansbold.ttf', 32)
    text_surface = custom_font.render(text, True, colorOn[1])
    text_rect = text_surface.get_rect()
    text_rect.center = SCREEN_WIDTH-110 , 312.5
    window.blit(text_surface, text_rect)
    
    pygame.display.update()
 
 
 
def draw_screen_offline(window, playerMoves, computerMoves, winner) :
    
    window.fill(COLORS['white'])
    for pos in playerMoves :
        text = 'X'
        custom_font = pygame.font.Font('freesansbold.ttf', 60)
        textsurface = custom_font.render(text, True, COLORS['grey'])
        textrect = textsurface.get_rect()
        textrect.center = pos[0]*CELL_WIDTH + CELL_WIDTH/2 , pos[1]*CELL_WIDTH + CELL_WIDTH/2
        window.blit(textsurface, textrect)
        
    for pos in computerMoves :
        text = 'O'
        custom_font = pygame.font.Font('freesansbold.ttf', 60)
        textsurface = custom_font.render(text, True, COLORS['grey'])
        textrect = textsurface.get_rect()
        textrect.center = pos[0]*CELL_WIDTH + CELL_WIDTH/2 , pos[1]*CELL_WIDTH + CELL_WIDTH/2
        window.blit(textsurface, textrect)
        
    for x in ( 0, CELL_WIDTH, CELL_WIDTH*2, CELL_WIDTH*3) :
        pygame.draw.line(window, COLORS['black'], (x,0), (x,SCREEN_WIDTH), 3)
        pygame.draw.line(window, COLORS['black'], (0,x), (SCREEN_WIDTH,x), 3)
    
    color = COLORS['green']
    
    if winner :
        if winner == 'p' :
            text = 'YOU WON'
        else : 
            text = 'YOU LOST'
            color = COLORS['red']
        custom_font = pygame.font.Font('freesansbold.ttf', 60)
        textsurface = custom_font.render(text, True, color)
        textrect = textsurface.get_rect()
        textrect.center = SCREEN_WIDTH/2 , SCREEN_WIDTH/2
        window.blit(textsurface, textrect)
        
    elif len(playerMoves) + len(computerMoves) == 9 :
        text = 'TIE GAME'
        custom_font = pygame.font.Font('freesansbold.ttf', 60)
        textsurface = custom_font.render(text, True, color)
        textrect = textsurface.get_rect()
        textrect.center = SCREEN_WIDTH/2 , SCREEN_WIDTH/2
        window.blit(textsurface, textrect)
        
    pygame.display.update()



def optimalMove( playerMoves, computerMoves, available, turn ) :
    
    winner = check_winner( playerMoves, computerMoves )
    if winner :
        if winner == 'c' : return -1, None
        elif winner == 'p' : return 1, None
        
    if not len(available) : return 0, None
    
    if turn == 'c' : 
        score = float('inf')
        next_turn = 'p'
    if turn == 'p' : 
        score = -1*float('inf')
        next_turn = 'c'
        
    preferred_move = None
    
    for position in available :
        if turn == 'c' :
            returned_score, garbage = optimalMove( playerMoves, computerMoves.union({position}), available.difference({position}), next_turn)
            if returned_score < score : 
                score = returned_score
                preferred_move = position
        if turn == 'p' :
            returned_score, garbage = optimalMove( playerMoves.union({position}), computerMoves, available.difference({position}), next_turn)
            if returned_score > score : 
                score = returned_score
                preferred_move = position

    return score, preferred_move



def check_winner( playerMoves, computerMoves ) :
    if len(playerMoves) >= 3 :
        for row in range(0,3) :
            if (row,0) in playerMoves and (row,1) in playerMoves and (row,2) in playerMoves :
                return 'p'
        for col in range(0,3) :
            if (0,col) in playerMoves and (1,col) in playerMoves and (2,col) in playerMoves :
                return 'p'
        if (0,0) in playerMoves and (1,1) in playerMoves and (2,2) in playerMoves :
            return 'p'
        if (0,2) in playerMoves and (1,1) in playerMoves and (2,0) in playerMoves :
            return 'p'
            
    if len(computerMoves) >= 3 :
        for row in range(0,3) :
            if (row,0) in computerMoves and (row,1) in computerMoves and (row,2) in computerMoves :
                return 'c'
        for col in range(0,3) :
            if (0,col) in computerMoves and (1,col) in computerMoves and (2,col) in computerMoves :
                return 'c'
        if (0,0) in computerMoves and (1,1) in computerMoves and (2,2) in computerMoves :
            return 'c'
        if (0,2) in computerMoves and (1,1) in computerMoves and (2,0) in computerMoves :
            return 'c'
    
    return None



main(root)

