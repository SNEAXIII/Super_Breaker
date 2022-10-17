import pygame
pygame.init()
pygame.mixer.init()

class son_jeu:
    '''lancement de l'instance pygame playlist pour jouer les sons'''
    def __init__(self):
        self.playlist = set()


    def joue(self):
        '''défini l'utilisation du son dans la fenêtre pygame'''
        if self.playlist != set():
            for i in self.playlist:
                pygame.mixer.music.load(i)
            pygame.mixer.music.play(0)
            self.playlist.clear()


    def son_perdu(self):
        '''joue un son quand le joueur perd la partie'''
        self.playlist.add(r"sounds\player_lose.mp3")


    def son_collbords(self):
        '''joue un son quand la balle touche les bords de la fenêtre'''
        self.playlist.add(r"sounds\wall_collision.mp3")


    def son_briques1(self):
        '''joue un son quand la balle touche une brique'''
        self.playlist.add(r"sounds\brick_collision.mp3")



    def son_briques2(self):
        '''joue un son quand la balle touche une brique'''
        self.playlist.add(r"sounds\brick_breaker.mp3")


    def son_balle_barre(self):
        '''joue un son quand la balle tape dans la barre'''
        self.playlist.add(r"sounds\stick_collision.mp3")