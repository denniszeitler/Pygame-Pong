
# Importieren der Pygame-Bibliothek
import pygame, math, shelve

# initialisieren von pygame
pygame.init()
pygame.font.init()

# shelve
d = shelve.open('score.txt')
highscore = d['score']
highscore = int(highscore)
print(type(highscore))


# genutzte Farbe

ORANGE  = ( 255, 140, 0)
ROT     = ( 255, 0, 0)
GRUEN   = ( 0, 255, 0)
BLAU    = ( 0, 0, 205)
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)

Colors = [
    (255, 140, 0),  # ORANGE
    (255, 0, 0),    # ROT
    (0, 255, 0),    # GRUEN
    (0, 0, 205),    # BLAU
    (255, 255, 255) # WEISS
]


FENSTERBREITE = 640
FENSTERHOEHE = 480

# Fenster öffnen
screen = pygame.display.set_mode((FENSTERBREITE, FENSTERHOEHE))

# Titel für Fensterkopf
pygame.display.set_caption("PONG")


# solange die Variable True ist, soll das Spiel laufen
spielaktiv = True

# Bildschirm Aktualisierungen einstellen
clock = pygame.time.Clock()

# Definieren der Variablen/Konstanten
ballpos_x = 300
ballpos_y = 150

BALL_DURCHMESSER = 20

bewegung_x = 4
bewegung_y = 4
ballwechsel = 0

spielfigur_1_x = 20
spielfigur_1_y = 20
spielfigur_1_bewegung = 0

spielfigur_2_x = FENSTERBREITE - (2*20)
spielfigur_2_y = 20
spielfigur_2_bewegung = 0

schlaegerhoehe = 100


gameover = False

#soundeffekte laden
#Royalty-free game-over sound effects from pixabay.com
getroffen = pygame.mixer.Sound('sound/tennis-smash.mp3')
negative = pygame.mixer.Sound('sound/negative_beeps.mp3')

#Score Text
my_font = pygame.font.SysFont("Arial", 36)

#Startbildschirm
start_text = my_font.render("Drücke eine Taste zum Starten", True, WEISS)
start_score = my_font.render (f'Highscore: {highscore}', True, WEISS)
start_end = my_font.render("Spiel beenden", True, SCHWARZ)

start_player1 = my_font.render("Spieler 1", True, WEISS)
start_player2 = my_font.render("Spieler 2", True, WEISS)

global end_clicked

def start_screen():
    global player1_color
    global player2_color
    player1_colorindex = 0
    player1_color = Colors[player1_colorindex]
    player2_colorindex = 2
    player2_color = Colors[player2_colorindex]
    start = True
    while start:
        screen.fill(SCHWARZ)

        #Text Positionen berechnen

        player1_rect = start_player1.get_rect(center=(FENSTERBREITE /4, FENSTERHOEHE/4))
        pygame.draw.rect(screen, player1_color, player1_rect)
        screen.blit(start_player1, player1_rect.topleft)

        player2_rect = start_player2.get_rect(center=(FENSTERBREITE /1.33, FENSTERHOEHE/4))
        pygame.draw.rect(screen, player2_color, player2_rect)
        screen.blit(start_player2, player2_rect.topleft)

        score_rect = start_score.get_rect()
        score_rect.center = (FENSTERBREITE / 2, FENSTERHOEHE / 4)
        screen.blit(start_score, score_rect)
        
        text_rect = start_text.get_rect()
        text_rect.center = (FENSTERBREITE / 2, FENSTERHOEHE / 2)
        screen.blit(start_text, text_rect)

        button_rect = start_end.get_rect(center=(FENSTERBREITE/2,FENSTERHOEHE/1.2))
        pygame.draw.rect(screen, WEISS, button_rect)
        screen.blit(start_end, button_rect.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                start = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player1_rect.collidepoint(event.pos):

                    if player1_colorindex == len(Colors) -1:
                        player1_colorindex = 0
                    else:
                        player1_colorindex += 1
                    
                    player1_color = Colors[player1_colorindex]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player2_rect.collidepoint(event.pos):

                    if player2_colorindex == len(Colors) -1:
                        player2_colorindex = 0
                    else:
                        player2_colorindex += 1
                    
                    player2_color = Colors[player2_colorindex]



                    


def reset_game():
    start_screen()
    global score, ballpos_x, ballpos_y, gameover
    score = 0
    ballpos_x = 300
    ballpos_y = 150
    gameover = False

# Startbildschirm anzeigen
start_screen()
reset_game()


# Schleife Hauptprogramm
while spielaktiv:
    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktiv = False
            print("Spieler hat Quit-Button angeklickt")
            
        elif event.type == pygame.KEYDOWN:
            print("Spieler hat Taste gedrückt")

            if event.key == pygame.K_UP:
                print("Spieler hat Pfeiltaste hoch gedrückt")
                spielfigur_1_bewegung = -6

            elif event.key == pygame.K_DOWN:
                print("Spieler hat Pfeiltaste runter gedrückt")
                spielfigur_1_bewegung = 6

            elif event.key == pygame.K_w:
                print("Spieler hat w für gedrückt")
                spielfigur_2_bewegung = -6
            elif event.key == pygame.K_s:
                print("Spieler 2 hat  s für runter gedrückt")
                spielfigur_2_bewegung = 6

        # Bewegung stoppen
        if event.type == pygame.KEYUP:
            print("Spieler hat Taste losgelassen")

            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                print("Spieler 1 stoppt Bewegung")
                spielfigur_1_bewegung = 0
        
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                print("Spieler 2 stoppt Bewegung")
                spielfigur_2_bewegung = 0



    # Spiellogik hier integrieren
    if spielfigur_1_bewegung != 0:
        spielfigur_1_y += spielfigur_1_bewegung

    if spielfigur_1_y < 0:
        spielfigur_1_y = 0

    if spielfigur_1_y > FENSTERHOEHE - schlaegerhoehe:
        spielfigur_1_y = FENSTERHOEHE - schlaegerhoehe

    if spielfigur_2_bewegung != 0:
        spielfigur_2_y += spielfigur_2_bewegung

    if spielfigur_2_y < 0:
        spielfigur_2_y = 0

    if spielfigur_2_y > FENSTERHOEHE - schlaegerhoehe:
        spielfigur_2_y = FENSTERHOEHE - schlaegerhoehe


    # Spielfeld löschen
    screen.fill(SCHWARZ)


    # Spielfeld/figuren zeichnen
    # rect 1 -> x achse, rect 2 -> y achse, rect 3 -> x größe, rect 4 -> y größe
    ball = pygame.draw.ellipse(screen, WEISS, [ballpos_x, ballpos_y, BALL_DURCHMESSER, BALL_DURCHMESSER])

    player1 = pygame.draw.rect(screen, player1_color, [spielfigur_1_x, spielfigur_1_y, 20, 100])
    player2 = pygame.draw.rect(screen, player2_color, [spielfigur_2_x, spielfigur_2_y, 20, 100])

    ballpos_x += bewegung_x
    ballpos_y += bewegung_y

    if ballpos_y > FENSTERHOEHE - BALL_DURCHMESSER or ballpos_y < 0:
        bewegung_y = bewegung_y * -1
    
    if ballpos_x > FENSTERBREITE - BALL_DURCHMESSER or ballpos_x < 0:
        pygame.mixer.Sound.play(negative)
        gameover = True
        reset_game()

    if player1.colliderect(ball):
        print("Zusammenstoß Spieler 1 und Ball")
        pygame.mixer.Sound.play(getroffen)
        bewegung_x = bewegung_x * -1
        ballpos_x = 40
        ballwechsel += 1
        schlaegerhoehe -= 5
        print("Spieler 1 erzielt einen Punkt!")
        score += 1

        # Highscore aktuallisieren
        if score > highscore:
            highscore = score
            d['score'] = highscore

    if player2.colliderect(ball):
        print("Zusammenstoß Spieler 1 und Ball")
        pygame.mixer.Sound.play(getroffen)
        bewegung_x = bewegung_x * -1
        ballpos_x = 570
        ballwechsel += 1
        schlaegerhoehe -= 5
        print("Spieler 2 erzielt einen Punkt!")
        score += 1

        # Highscore aktuallisieren
        if score > highscore:
            highscore = score
            d['score'] = highscore

        # Text anzeigen
    text_surface = my_font.render(f'Score: {score}', True, WEISS)
    text_rect = text_surface.get_rect()
    text_rect.center = (FENSTERBREITE / 2, FENSTERHOEHE / 10)
    screen.blit(text_surface, text_rect)



    # Fenster aktualisieren
    pygame.display.flip()
    # Refresh-Zeiten festlegen
    clock.tick(60)

d.close()
pygame.quit()
quit()