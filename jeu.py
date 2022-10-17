import pygame
from sons import son_jeu
from barre import barre
from balls import balle
from bricks import bricks
from pygame.locals import *
from menu import Menu, Menu_Level, Niveau
from niveaux import liste_level_0


class souris:
    '''calcul les coordonnées de la souris dans la fenêtre à chaque frame'''

    def __init__(self):
        self.press = False
        self.position()

    def position(self):
        self.pos = pygame.mouse.get_pos()


class jeu:
    '''
    fps = nombre de frame par seconde
    fond écran = définition du fond de la fenêtre pygame
    fpsclock = définie le nombre d'image par seconde de la fenêtre
    angle_base = angle de la balle au lancement
    son_jeu = utilise le fichier sons pour lancer l'instance de pygame des sons
    menu = appel de la classe Menu
    background = définition de l'arrière plan du jeu
    '''

    def __init__(self):
        self.run = True
        self.fps = 60
        self.fond_ecran = (255, 255, 255)
        self.fpsClock = pygame.time.Clock()
        self.largeur_ecran = 1080
        self.hauteur_ecran = 720
        self.surface = pygame.display.set_mode((self.largeur_ecran, self.hauteur_ecran))
        self.angle_base = 45
        self.font = pygame.font.SysFont('Linux Biolinum G', 55)
        self.Son_Jeu = son_jeu()
        self.menu = Menu(self.surface, self.font, souris())
        self.menu_niveau = Menu_Level(self.surface, self.font, souris())
        self.reset()
        self.background = pygame.image.load(r"textures\wallpaper.png")

    def reset(self):
        self.Bricks = None
        self.Barre = None
        self.balls = set()

    def frame(self):
        '''actualise les éléments du jeu chaque frame ( 60 par seconde en l'occurence )'''
        self.Son_Jeu.joue()
        pygame.display.flip()
        self.fpsClock.tick(self.fps)
        self.surface.blit(self.background, (0, 0))

    def add_ball(self, valeur):
        '''définition des paramètres de la balle'''
        self.balls.add(
            balle(self.largeur_ecran, self.hauteur_ecran, self.Barre, self.Bricks, self.surface, self.Son_Jeu,
                  valeur.angle, valeur.vitesse, valeur.taille_barre))

    def partie(self, valeur):
        '''lance la partie de jeu avec les paramètres nécessaires'''
        hp = valeur.hp_ball
        self.Bricks = bricks(self.surface, valeur.hp_brique, valeur.pattern)
        self.Barre = barre(self.surface)
        self.add_ball(valeur)
        en_vie = True
        nb = last_nb = len(self.Bricks)
        p1, p2, p3, p4 = nb // 5, nb // 5 * 2, nb // 5 * 3, nb // 5 * 4

        while en_vie:
            nb = len(self.Bricks)
            self.Barre.tp_souris()

            for event in pygame.event.get():
                if event.type == QUIT:
                    en_vie = False
                    self.run = False

            self.Bricks.dessine_moi()

            for ball in self.balls:
                morts = False
                if ball.mort:
                    morts = ball
                else:
                    ball.colibrique()
                    ball.deplacement()
            if morts:
                self.balls.discard(morts)
            self.Barre.affiche()

            if self.balls == set():
                hp -= 1
                if hp >= 0:
                    self.add_ball(valeur)
                else:
                    en_vie = False
            if nb == 0:
                en_vie = False
            else:
                if nb == p1 and not last_nb == p1:
                    last_nb = p1
                    self.add_ball(valeur), self.add_ball(valeur)
                elif nb == p2 and not last_nb == p2:
                    last_nb = p2
                    self.add_ball(valeur), self.add_ball(valeur)
                elif nb == p3 and not last_nb == p3:
                    last_nb = p3
                    self.add_ball(valeur), self.add_ball(valeur)
                elif nb == p4 and not last_nb == p4:
                    last_nb = p4
                    self.add_ball(valeur), self.add_ball(valeur)

            self.surface.blit(self.font.render(f"{hp}", True, (0, 0, 255)), (0, 0))
            self.frame()
        self.reset()

    def menu_principal(self):
        '''contrôle l'execution du menu principal avant le lancement d'une partie ou d'un autre menu'''
        while self.run:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.menu.souris.press = True
                else:
                    self.menu.souris.press = False
                if event.type == QUIT or self.menu.end:
                    self.run = False
            if self.menu.jeu:
                self.partie(Niveau(liste_level_0, 7, -2, 45, 1, 0))
                self.menu.reset()
            if self.menu.level:
                self.menu_level()
                self.menu_niveau.reset()
                self.menu.reset()
            if self.menu.credit:
                self.background = pygame.image.load(r"textures\credits.png")
                while self.run:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            self.run = False
                    self.frame()

            self.menu.next_frame()
            self.frame()

    def menu_level(self):
        '''execute le menu level et affiche les boutons nécessaires'''
        en_cours = True
        valeur = False
        while en_cours and self.run:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.menu_niveau.souris.press = True
                else:
                    self.menu_niveau.souris.press = False
                if event.type == QUIT:
                    self.run = False
                    en_cours = False

            if self.menu_niveau.end:
                en_cours = False

            if not valeur == False:
                self.partie(valeur)
                self.menu_niveau.reset()

            self.menu_niveau.next_frame()
            valeur = self.menu_niveau.click()
            self.frame()
