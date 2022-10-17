from math import sin, cos, pi
import pygame

class balle:

    '''
    skins = texture de la balle importé
    img_base = texture actuellement appliqué à la balle
    sons = importation des sons du fichier son
    change_barre_x = valeur de la taille de la barre
    '''
    def __init__(self, largeur, hauteur, Barre, Bricks, surface, sons, angle=40, vitesse=20, change_barre_x = 0):
        self.pi180 = pi / 180
        self.reset(Barre, vitesse, Bricks, angle)
        self.screen_h = hauteur
        self.screen_l = largeur
        self.surface = surface
        self.skins = {"feu" : pygame.image.load(r"textures\ball\fire_bool.png")}
        self.img_base = self.img_act = self.skins["feu"]
        self.Sons = sons
        self.change_barre_x = change_barre_x

    def tp_souris(self):
        '''appelle les coordonnées de la souris à chaque frame'''
        self.x, self.y = pygame.mouse.get_pos()

    def reset(self, Barre, vitesse, Bricks, angle=45):
        '''réinitialise les paramètres de la balle et ses intéractions avec l'environnement (briques, barre du joueur etc)'''
        self.rayon = 10
        self.angle = angle
        self.vitesse = vitesse
        self.x = Barre.x
        self.y = Barre.y - Barre.taille_y - self.rayon
        self.calc_direction()
        self.Barre = Barre
        self.y_barre = self.Barre.y - self.Barre.taille_y
        self.couleur = (255, 0, 0)
        self.y_dir = 1
        self.x_dir = 1
        self.Barre.taille_x = self.Barre.taille_x_base
        self.Bricks = Bricks
        self.mort = False
        self.lock = False

    def augemente_vitesse(self, nb):
        '''augmente la vitesse de la balle'''
        self.vitesse += nb
        self.calc_direction()

    def calc_coef(self):
        '''calcul le coéfficient directeur de la trajectoire de la balle'''
        self.coef_directeur = self.angle * self.pi180

    def calc_direction(self):
        '''calcul la trajectoire de la balle'''
        self.calc_coef()
        self.vx = self.vitesse * cos(self.coef_directeur)
        self.vy = self.vitesse * sin(self.coef_directeur)

    def deplacement(self):
        '''applique le déplacement de la balle dans l'espace et de sa texture'''
        self.colisions()
        self.x += self.vx * self.x_dir
        self.y -= self.vy * self.y_dir
        self.surface.blit(self.img_act, (int(self.x-self.rayon), int(self.y-self.rayon)))

    def rebond_droite(self):
        '''calcul l'angle de rebond sur la face droite d'un élément'''
        if self.angle >= 90:
            self.x_dir = 1
        else:
            self.x_dir = -1

    def rebond_gauche(self):
        '''calcul l'angle de rebond sur la face gauche d'un élément'''
        if self.angle >= 90:
            self.x_dir = -1
        else:
            self.x_dir = 1

    def rebond_haut(self):
        '''calcul l'angle de rebond sur la face haute d'un élément'''
        self.y_dir, self.lock = -1, False

    def rebond_bas(self):
        '''calcul l'angle de rebond sur la face basse d'un élément'''
        self.y_dir = 1

    def rebond_barre(self, mini=5, maxi=30):
        '''calcul l'angle de rebond sur la barre'''
        O, M, L = self.Barre.x, self.x, self.Barre.taille_x + self.rayon
        A, C, B = O - L, O, O + L

        # Segment [AO]
        if A <= self.x <= O:
            self.contact_barre(((M - A) / (C - A)), 90 + mini, 180 - maxi)

        # segment ]OB]
        elif O <= self.x <= B:
            self.contact_barre(((M - C) / (B - C)), maxi, 90 - mini)

    def colisions(self):
        '''Verifie les colisions avec les bords'''
        if self.x + self.rayon >= self.screen_l:
            self.rebond_droite()
            self.Sons.son_collbords()

        if self.x - self.rayon <= 0:
            self.rebond_gauche()
            self.Sons.son_collbords()

        if self.y - self.rayon <= 0:
            self.rebond_haut()
            self.Sons.son_collbords()

        if self.y + self.rayon >= self.screen_h:
            self.mort = True
            self.Sons.son_perdu()

        if self.y_barre + self.vy + 1 > self.y + self.rayon > self.y_barre and not self.lock: self.rebond_barre()

    def colibrique(self):
        '''
        vérifie les colisions avec les différentes faces des briques
    enlève une vie aux briques touchées
    ajoute la texture de fissure sur la brique touchée
        '''
        for ligne in self.Bricks.bricks:
            side = [0, 0, 0]  # droite gauche haut bas nb
            touche = set()
            for brique in ligne:
                if brique.en_vie:
                    # if brique.x_min < self.x < brique.x_max and brique.y_min < self.y < brique.y_max:
                    lmin, lmax = brique.x_min - int(self.rayon), brique.x_max + int(self.rayon)
                    hmin, hmax = brique.y_min - int(self.rayon), brique.y_max + int(self.rayon)
                    # print(lmin,self.x,lmax)
                    # self.h(brique)
                    # self.h1(brique)
                    # self.l(brique)

                    if lmin <= self.x <= lmax:
                        if brique.y_max - self.vy - 1 <= self.y - self.rayon <= brique.y_max:
                            # self.rebond_haut()
                            self.Bricks.briques_restantes = brique.hp_add(-1)
                            touche.add(brique)
                            side[1] -= 1

                        elif brique.y_min + self.vy + 1 >= self.y + self.rayon >= brique.y_min:
                            # self.rebond_bas()
                            self.Bricks.briques_restantes = brique.hp_add(-1)
                            touche.add(brique)
                            side[1] += 1

                    if hmin <= self.y <= hmax:
                        if brique.x_max - abs(self.vx) - 1 <= self.x - self.rayon <= brique.x_max:
                            # self.rebond_gauche()
                            self.Bricks.briques_restantes = brique.hp_add(-1)
                            touche.add(brique)
                            side[0] += 1

                        elif brique.x_min + abs(self.vx) + 1 >= self.x + self.rayon >= brique.x_min:
                            # self.rebond_droite()
                            self.Bricks.briques_restantes = brique.hp_add(-1)
                            touche.add(brique)
                            side[0] -= 1
            if side[0]==-2:
                self.rebond_droite()
            elif side[0] == 2:
                self.rebond_gauche()
            if side[1] == 2:
                self.rebond_bas()
            elif side[1] == -2:
                self.rebond_haut()
            else:
                if side[0] == -1:
                    self.rebond_droite()
                if side[0] == 1:
                    self.rebond_gauche()
                if side[1] == 1:
                    self.rebond_bas()
                if side[1] == -1:
                    self.rebond_haut()
            for brique in touche :
                brique.cassure(self.Bricks.fissures)
                self.Sons.son_briques1()


    def actualiser_ybarre(self):
        '''actualise la taille et la position de la barre en y'''
        self.y_barre = self.Barre.y - self.Barre.taille_y

    def contact_barre(self, gamma, max0, max1):
        '''modifie la taille de la barre à chaque colisions ( change_barre_x )'''
        self.calc_coef_barre(gamma, max0, max1)
        self.Barre.augmente_taile_x(self.change_barre_x)
        self.rebond_bas()
        self.Sons.son_balle_barre()

    def calc_coef_barre(self, gamma, max0, max1):
        '''calcul l'angle de rebond de la balle sur la barre suivant son lieu de rebond sur la barre'''
        self.lock, self.x_dir, self.angle = True, 1, gamma * max0 + max1 * (1 - gamma)
        self.calc_direction()
