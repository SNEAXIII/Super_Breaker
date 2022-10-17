import pygame

## Class Bricks
'''Création des briques dans la fenêtre du jeu'''
class bricks:

    '''
    img = chargement des images utilisables pour les textures des bricks en jeu
    fissure = chargement des images overlays pour les cassures des bricks
    hp_brique = nombre de choc avec la balle avant que la brique soit cassé
    pattern_base = liste de 0 et de 1 en fonction de l'existance de brique à chaque coordonnée
    self.bricks = création de la liste utilisable pour le code du pattern
    '''
    def __init__(self, surface, hp, pattern):
        self.img = {
            "blue" :pygame.image.load(r"textures\brick\blue_brick.png"),
            "green" :pygame.image.load(r"textures\brick\green_brick.png")
                    }
        self.fissures = {
            "fissure1" : pygame.image.load(r"textures\crack\layer_crack_phase1.png"),
            "fissure2" : pygame.image.load(r"textures\crack\layer_crack_phase2.png"),
            "fissure3" : pygame.image.load(r"textures\crack\layer_crack_phase3.png")
                    }
        self.surface = surface
        self.hp_brique = hp
        self.pattern_base = pattern
        self.bricks = [[],[],[],[],[],[],[],[],[],[],[]]
        self.reset_()



    def reset_(self):
        """replace toutes briques selon leur situation initiale"""
        self.liste_briques()


    def dessine_moi(self):
        """affiche les textures de toutes briques à leurs coordonnées"""
        for ligne in self.bricks:
            for brique in ligne:
                brique.affiche()


    def liste_briques(self):
        x_base = 45
        y_base = 82
        for a in range(len(self.pattern_base)):
            for b in range(len(self.pattern_base[a])):
                if self.pattern_base[a][b] == 1:
                    self.bricks[a].append(brick(x_base + 90*b, y_base + 28*a, self.img["blue"], self.surface, self.hp_brique))
        return self.bricks

    def __str__(self):
        """affiche la liste des briques dans la console"""
        str_ = ""
        for ligne in self.bricks:
            for brique in ligne:
                str_ += f"{brique.x, brique.y} "
            str_ += "\n"
        return str_

    def __len__(self):
        """affiche les textures de toutes briques à leurs coordonnées"""
        len = 0
        for ligne in self.bricks:
            for brique in ligne:
                len += brique.alive
        return len

## Class Brick
"""définition d'une brique avec sa texture, ces variations et sa position"""

class brick:
    def __init__(self, x, y, img, surface, hp = 1):
        self.taille_x = 43
        self.taille_y = 12
        self.x = x
        self.y = y
        self.x_min = self.x - self.taille_x
        self.x_max = self.x + self.taille_x
        self.y_min = self.y - self.taille_y
        self.y_max = self.y + self.taille_y
        self.hp = self.max_hp = hp
        self.en_vie = True
        self.img = img
        self.surface = surface
        self.layer_cassure = None
        self.alive = 1

    def hp_add(self, nb):
        '''actualise le nombre de points de vie que possède la brique et retourne False si elle n'a plus de vie'''
        if self.en_vie:
            self.hp += nb
        if self.hp < 1:
            self.en_vie = False
            self.alive = 0

    def kill(self):
        '''tue la brique'''
        self.en_vie = False
        self.alive = 0

    def cassure(self, liste_fissure):
        '''application des différentes textures de fissures sur les briques après un choc avec la balle'''
        if self.en_vie :
            if (self.max_hp//3)*2 < self.hp <= self.max_hp :
                self.layer_cassure = liste_fissure["fissure1"]
            elif self.max_hp//3 < self.hp <= (self.max_hp//3)*2 :
                self.layer_cassure = liste_fissure["fissure2"]
            elif 0 < self.hp <= self.max_hp//3 :
                self.layer_cassure = liste_fissure["fissure3"]

    def affiche(self):
        '''affiche les textures des briques si elles sont encore "vivante" ( self.hp_brique positif )'''
        if self.en_vie:
            self.surface.blit(self.img, (self.x - self.taille_x, self.y - self.taille_y))
            if not self.layer_cassure is None:
                self.surface.blit(self.layer_cassure, (self.x - self.taille_x, self.y - self.taille_y))
