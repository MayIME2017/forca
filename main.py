# Based on code by Tim Ruscica
# url: https://replit.com/@TimRuscica/hangmantest

# importing libraries
import pygame
import math
import random
import numpy as np

# setup window display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JOGO DA FORCA")

# loading images
images = []
for i in range(7):
    image = pygame.image.load("forca" + str(i) + ".png")
    images.append(image)

# game variables
FRUITS = ["BANANA", "UVA", "MORANGO", "MELANCIA", "LARANJA", "CAJU", "ABACATE", "ABACAXI", "AMORA", "ACEROLA", "CACAU", "CEREJA"]
MONTHS = ["JANEIRO", "FEVEREIRO", "MARCO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
COLORS = ["VERMELHO", "AZUL", "AMARELO", "BRANCO", "PRETO", "ROSA", "VERDE", "CINZA", "MARROM", "VIOLETA", "CIANO", "TURQUESA"]

COLLECTION = np.vstack([FRUITS, MONTHS, COLORS])


# button variables
RADIUS = 20
GAP = 15

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70, bold=True)
TIP_FONT = pygame.font.SysFont('comicsans', 40, italic=True)

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)

def game_setup():
    global hangman_status, tip, word, letters, already_guessed

    hangman_status = 0

    selection = random.randint(0,2)
    if selection == 0:
        tip = "frutas"
    if selection == 1:
        tip = "meses do ano"
    if selection == 2:
        tip = "cores"
    collection_choice = COLLECTION[selection,:] 
    word = random.choice(collection_choice)
    already_guessed = []

    letters = []
    startx = round((WIDTH-(RADIUS*2 + GAP) * 13)/2)
    starty = 400
    A = 65

    for i in range(26):
        x = startx + GAP*2 + (RADIUS * 2 + GAP) * (i % 13)
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])

def draw():
    win.fill(WHITE)

    # Draw title
    text = TITLE_FONT.render("Jogo da Forca", 1, BLACK)
    win.blit(text, ((WIDTH-text.get_width())/2, 20))

    # Draw tip
    text = TIP_FONT.render("Dica: " + tip, 1, BLACK)
    win.blit(text, ((WIDTH-text.get_width())/2, 70))

    # draw word
    display_word = ""
    for letter in word:
        if letter in already_guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (270, 200))

    # draw buttons 
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status], (50, 100))
    pygame.display.update()

def display_message(message):
    pygame.time.delay(2000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, ((WIDTH - text.get_width())/2, (HEIGHT - text.get_height())/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global hangman_status, game

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                return game
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            already_guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in already_guessed:
                won = False
                break

        if won:
            display_message("PARABÉNS!")
            break


        if hangman_status == 6:
            display_message("VOCÊ PERDEU!")
            break
    

game = True
while game:    
    game_setup()

    main()    
    
pygame.quit()