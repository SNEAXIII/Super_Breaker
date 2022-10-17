import pygame

## Class Barre
'''définition de la barre du joueur dans la fenêtre du jeu'''

class barre:
    '''
    x / y = coordonnées d'origine en X et Y dans la fenêtre
    taille_x / taille_y = longueur et largeur de la barre depuis le point d'origine (x,y)
    taille_x_mini / taille_x_maxi = longueur x minimum et maximum de la barre depuis l'origine (x,y)
    img_gauche / img_droite = chargement des textures des deux cotés de la barre
    '''

    def __init__(self,  surface):
        self.x = 1080 / 2
        self.y = 660
        self.taille_x = self.taille_x_base = 75
        self.taille_y = 5
        self.taille_x_mini = 35
        self.taille_x_maxi = 150
        self.surface = surface
        self.img_gauche = pygame.image.load(r"textures\stick\left_player_stick.png")
        self.img_droite = pygame.image.load(r"textures\stick\right_player_stick.png")

    def tp_souris(self):
        '''déplace la barre du joueur à la position en x de la souris dans la fenêtre'''
        self.x = self.pos_souris()

    def pos_souris(self):
        '''retourne la position de la souris en x dans la fenêtre'''
        return pygame.mouse.get_pos()[0]

    def augmente_taile_x(self, nb):
        '''augmente ou diminue la taille de la barre en jeu en fonction de nb dans un interval limité'''
        if self.taille_x_mini < self.taille_x + nb < self.taille_x_maxi:
            self.taille_x += nb

    def affiche(self):
        '''place les textures des deux cotés de la barre à chaque frame'''

        pygame.draw.rect(self.surface, (237, 190, 82),
                         pygame.Rect(self.x - self.taille_x, self.y - self.taille_y,
                                     self.taille_x * 2, self.taille_y * 2))
        pygame.draw.rect(self.surface, (0, 0, 0),
                         pygame.Rect(self.x - self.taille_x, self.y - self.taille_y,
                                     self.taille_x * 2, self.taille_y * 2), 1)
        self.surface.blit(self.img_gauche, (self.x-self.taille_x-4, self.y-5))
        self.surface.blit(self.img_droite, (self.x+self.taille_x-75, self.y-5))