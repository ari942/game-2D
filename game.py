import pygame
import pytmx
import pyscroll
import self as self

from Player import Player

pygame.init()  # initialiser les composants

class Game:

    def __init__(self):

        #creer la fenetre du jeu
        self.screen = pygame.display.set_mode([800, 600]) #display=gerer les affichage set_mode=change les parametre du jeu et la fenetre self.screen = ranger des elements a l'intereieur de l'objet pour pouvoir les modifier
        pygame.display.set_caption("pygamon -Aventure")#change le titre de la fenetre

        #charger la carte (tmx)

        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx') #permet de specifier le fichier en tmx
        map_data = pyscroll.data.TiledMapData(tmx_data)#recupere les données de tmx pour extraire la carte
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size()) #charger les different calque qu'on a creer a l'interieur de cette carte // #contient les map regroupé get_size = recupere sa taille en largeur et en hauteur // # = self.screen.get_size()sur la surface qu'on va dessiner le jeu
        map_layer.zoom = 2 #pour zoomer l'affichage

        #generer un joueur a partir de cette classe
        player_position = tmx_data.get_object_by_name("player")#recuperer les coordonnées de tiled  / ("player") = recupere le nom de l'object qu'on a creer dans tired
        self.player = Player(player_position.x, player_position.y)#.x et .y car c'est les coordonnées du logiciels tired = plus besoin de passer par le code pour placer le joueurs

        #definir une liste qui va stocker les rectangle des collisions

        self.walls = []

        for object in tmx_data.objects:#recupere tous les objets de la carte
            if object.type == "(Collision)":
                self.walls.append(pygame.Rect(object.x, object.y, object.width, object.height))#ajouter dans un liste de mur


        #dessiner le groupe de calques

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4) #default_layer  permet de donner la postion du calque par défaut pour donner la hauteur du joueur a un certain niveau pour ne pas etre sous l'eau ou au dessus des arbres
        self.group.add(self.player)#on rajoute le player

    def handle_input (self):#permet de récupérer quel sont les touches enclanché pour joué
        pressed =pygame.key.get_pressed()#recupere toute les touches enclanché par le joueur

        if pressed[pygame.K_UP]: #il essaye d'appyuer pour aller en  haut
            self.player.move_up()
            self.player.change_animation('up')#voir le commentaire 21 de player.py
        elif pressed[pygame.K_DOWN]: #il essaye d'appyuer pour aller en bas
            self.player.move_down()
            self.player.change_animation("down")
        elif pressed[pygame.K_LEFT]: #il essaye d'appyuer pour aller à gauche
            self.player.move_left()
            self.player.change_animation("left")
        elif pressed[pygame.K_RIGHT]: #il essaye d'appyuer pour aller à droite
            self.player.move_right()
            self.player.change_animation("right")

    def update(self):#va fairevle travail d'actualisation du groupe
        self.group.update()

        #verification de la collision
        for sprite in self.group.sprites():#verifier si self contient un sprite avec la propriété feet qui doit entrer en collision avec un elkement de la liste self.walls
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()



    def run(self):

        clock = pygame.time.Clock() #permet de fixer le nombre de fps a chauqe tour de boucle

        #boucle du jeu

        running = True
        while running:
            self.player.save_location()#memoriser la localisation du joueur
            self.handle_input()
            self.update()#actualisation du groupe
            self.group.center(self.player.rect)#permet de recentrer le camera sur le joueur etq ue sa le suit tout le temps
            self.group.draw(self.screen)#dessiner les calque

            pygame.display.flip()# pour actualiser le jeu en temps réel
            for event in pygame.event.get(): #event = evenement get = nous liste les elements
                if event.type == pygame.QUIT: #si le jeu est de type pygame.QUIT (est activé) le joueur a tenté de tenter de fermé la fenetre sur la petite croix
                    running = False# passer running sur false donc la fermé

            clock.tick(60)#nombre de fps

        pygame.quit()