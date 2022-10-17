import pygame
from niveaux import liste_level_0, liste_level_1, liste_level_2, liste_level_3, liste_level_4

b_clear = r"textures\bouton_jouer_clear.png"
b_souris = r"textures\bouton_jouer_souris.png"

class souris:

    '''permet d'obtenir la position de la souris à chaque frame'''
    def __init__(self):
        self.press = False
        self.position()

    def position(self):
        self.pos = pygame.mouse.get_pos()


## Class Menu
''' Création du Menu du jeu qui s'occupera de lancer les différentes configurations de fenêtres pour le jeu, les options, les crédits et les niveaux '''


class Menu:
    '''
    souris = coordonnées de la souris
    jouer/levels/credits/quitter = création des boutons avec la classe Bouton
    font = définition de la police utilisé pour les boutons
    '''
    def __init__(self, surface, font, souris):
        self.souris = souris
        self.surface = surface
        self.jouer = Bouton(surface, 350, 261, 385, 115, b_clear, b_souris,
                            "JOUER", font, self.souris)
        self.levels = Bouton(surface, 350, 413, 385, 115, b_clear, b_souris,
                             "NIVEAUX", font, self.souris)
        self.credits = Bouton(surface, 20, 585, 385, 115, b_clear, b_souris,
                              "CREDITS", font, self.souris)
        self.quitter = Bouton(surface, 675, 585, 385, 115, b_clear, b_souris,
                              "QUITTER", font, self.souris)
        self.font = font
        self.reset()

    def verif_bouton(self):
        '''verifie si la souris se trouve dans le bouton correspondant'''
        self.jouer.verif()
        self.credits.verif()
        self.levels.verif()
        self.quitter.verif()

    def change_texture_bouton(self):
        '''change la texture de bouton lorsque la souris survole le bouton'''
        self.jouer.change_textu()
        self.credits.change_textu()
        self.levels.change_textu()
        self.quitter.change_textu()

    def affiche_bouton(self):
        '''affiche les boutons dans la fenêtre pygame'''
        self.jouer.afficher()
        self.credits.afficher()
        self.levels.afficher()
        self.quitter.afficher()

    def affiche_texte(self):
        '''affiche le texte sur chaque bouton'''
        self.jouer.affiche_texte()
        self.levels.affiche_texte()
        self.credits.affiche_texte()
        self.quitter.affiche_texte()

    def click(self):
        if self.jouer.click():
            # Affiche le jeu avec les paramètres sélectionnés
            self.jeu = True
        elif self.credits.click():
            # Afficher l'image des crédits
            self.credit = True
        elif self.levels.click():
            # Afficher les boutons des niveaux
            self.level = True
        elif self.quitter.click():
            # Quitte la fenêtre Pygame et clos le programme
            self.end = True

    def next_frame(self):
        '''actualise l'affichage'''
        self.souris.position()
        self.verif_bouton()
        self.change_texture_bouton()
        self.affiche_bouton()
        self.affiche_texte()
        self.click()

    def reset(self):
        '''remet à 0 chaque bouton'''
        self.souris.press = False
        self.end = False
        self.jeu = False
        self.level = False
        self.credit = False


## Class Bouton
'''Création des boutons du Menu du jeu'''


class Bouton:

    '''
    image simple = texture de base du bouton
    image souris = texture lorsque la souris survole le bouton
    str = texte à afficher dans le bouton
    text = définition de la la font de la taille et du style de l'écriture
    souris_dedans = True quand la souris est dans le bouton dans la fenêtre
    '''
    def __init__(self, surface, x, y, taille_x, taille_y, image_simple, image_souris, texte, font, souris):
        self.surface = surface
        self.x = x
        self.y = y
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.image_simple = self.image_actuelle = pygame.image.load(image_simple)
        self.image_souris = pygame.image.load(image_souris)
        self.str = texte
        self.text = font.render(texte, True, (0, 0, 0))
        self.souris_dedans = False
        self.souris = souris

    def __str__(self):
        return f"{self.text} -> {self.x} , {self.y}"

    def afficher(self):
        '''affiche la texture du bouton'''
        self.surface.blit(self.image_actuelle, (self.x, self.y))

    def verif(self):
        '''vérifie si le curseur de la souris et dans l'aire du bouton'''
        if self.x <= self.souris.pos[0] <= self.x + self.taille_x and self.y <= self.souris.pos[
            1] <= self.y + self.taille_y:
            self.souris_dedans = True
        else:
            self.souris_dedans = False

    def change_textu(self):
        '''change la texture à afficher en fonction de verif'''
        if self.souris_dedans:
            self.image_actuelle = self.image_souris
        else:
            self.image_actuelle = self.image_simple

    def click(self):
        '''retourne True si la souris clique dans le bouton'''
        if self.souris.press and self.souris_dedans:
            return True

    def affiche_texte(self):
        '''affiche le texte du bouton par dessus le bouton'''
        self.surface.blit(self.text, (self.x + (self.taille_x / 2) - (len(self.str) / 2) * 30 - 15, self.y + self.taille_y / 2 - 30))


## Class Level

class Menu_Level:

    '''
    retour/btnlevel1/level2/level3/level4 = création des boutons avec la classe bouton
    '''
    def __init__(self, surface, font, souris):
        self.souris = souris
        self.surface = surface
        self.retour = Bouton(surface, 347, 538, 385, 115, b_clear, b_souris, "RETOUR",
                             font, souris)
        self.bouton_level_1 = Bouton(surface, 109, 109, 385, 115, b_clear, b_souris,
                                     "Niveau 1", font, souris)
        self.bouton_level_2 = Bouton(surface, 595, 109, 385, 115, b_clear, b_souris,
                                     "Niveau 2", font, souris)
        self.bouton_level_3 = Bouton(surface, 109, 323, 385, 115, b_clear, b_souris,
                                     "Niveau 3", font, souris)
        self.bouton_level_4 = Bouton(surface, 595, 323, 385, 115, b_clear, b_souris,
                                     "Niveau 4", font, souris)
        # self.level_1 = Niveau(liste_level_1, 6, -2, 55, 2, 3)
        # self.level_2 = Niveau(liste_level_2, 7, -5, 25, 3, 2)
        # self.level_3 = Niveau(liste_level_3, 8, -6, 45, 3, 2)
        # self.level_4 = Niveau(liste_level_4, 10, -8, 20, 3, 1)
        self.reset()
        self.font = font

    def verif_bouton(self):
        '''verifie si la souris est dans chaque bouton'''
        self.bouton_level_1.verif()
        self.bouton_level_2.verif()
        self.bouton_level_3.verif()
        self.bouton_level_4.verif()
        self.retour.verif()

    def change_texture_bouton(self):
        '''modifie la textu du bouton si la souris est dedans'''
        self.bouton_level_1.change_textu()
        self.bouton_level_2.change_textu()
        self.bouton_level_3.change_textu()
        self.bouton_level_4.change_textu()
        self.retour.change_textu()

    def affiche_bouton(self):
        '''affiche chaque bouton'''
        self.bouton_level_1.afficher()
        self.bouton_level_2.afficher()
        self.bouton_level_3.afficher()
        self.bouton_level_4.afficher()
        self.retour.afficher()

    def affiche_texte(self):
        '''affiche le texte par dessus chaque bouton'''
        self.bouton_level_1.affiche_texte()
        self.bouton_level_2.affiche_texte()
        self.bouton_level_3.affiche_texte()
        self.bouton_level_4.affiche_texte()
        self.retour.affiche_texte()

    def click(self):
        '''
        intialise chaque paramètres de jeu en fonction du bouton de jeu cliqué
        retourne sur le menu principal si le bouton retour est cliqué
        '''
        if self.bouton_level_1.click():
            # Lance le jeu avec les paramètres choisis
            return Niveau(liste_level_1, 6, -2, 55, 2, 3)

        elif self.bouton_level_2.click():
            # Lance le jeu avec les paramètres choisis
            return Niveau(liste_level_2, 7, -5, 25, 3, 2)

        elif self.bouton_level_3.click():
            # Lance le jeu avec les paramètres choisis
            return Niveau(liste_level_3, 8, -6, 45, 3, 2)

        elif self.bouton_level_4.click():
            # Lance le jeu avec les paramètres choisis
            return Niveau(liste_level_4, 10, -8, 20, 3, 1)

        elif self.retour.click():
            # Retourne sur le menu de base
            self.end = True
            return False

        else:
            return False

    def next_frame(self):
        self.souris.position()
        self.verif_bouton()
        self.change_texture_bouton()
        self.affiche_bouton()
        self.affiche_texte()

    def reset(self):
        self.end = False
        self.souris.press = False


class Niveau:

    '''
    définition de chaque paramètre des niveaux, la forme des briques, la vitesse de la balle,
    la variation de la barre, l'angle de la balle au départ, la vie des briques et le nombre de vie du joueur
    '''
    def __init__(self, pattern, vitesse_ball, change_barre, angle_depart, hp_brique, hp):
        self.pattern = pattern
        self.vitesse = vitesse_ball
        self.taille_barre = change_barre
        self.angle = angle_depart
        self.hp_brique = hp_brique
        self.hp_ball = hp
