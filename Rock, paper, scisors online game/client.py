import pygame
from network import Network
from player import Player

width = 500
height = 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        window.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redrawWindow(window, game, p):
    window.fill((128, 128, 128))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for player...", 1, (255,0,0), True)
        window.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your move", 1, (0,255,255))
        window.blit(text, (80, 200))

        text = font.render("Opponent's", 1, (0,255,255))
        window.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0,0,0))
        else:
            if game.p1Went() and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went():
                text1 = font.render("Locked move", 1, (0,0,0))
            else:
                text1 = font.render("Waiting", 1, (0,0,0))
            
            if game.p2Went() and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went():
                text2 = font.render("Locked move", 1, (0,0,0))
            else:
                text2 = font.render("Waiting", 1, (0,0,0))

        if p == 1:
            window.blit(text2, (100, 350))
            window.blit(text1, (400, 350))
        else:
            window.blit(text1, (100, 350))
            window.blit(text2, (400, 350))
        
        for btn in btns:
            btn.draw(window)
    pygame.display.update()
                


btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scisors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = n.getP()
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        
        if game.bothWent():
            redrawWindow(window, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't reset game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("It's a tie!", 1, (255,0,0))
            else:
                text = font.render("You lost!", 1, (255,0,0))

            window.blit(text, (width/2 - text.get_width()/2), height/2 - text.get_height()/2)
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(window, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        window.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to play!", 1, (255,0,0))
        window.blit(text, (100,200))
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()