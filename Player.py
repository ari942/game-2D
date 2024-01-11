import pygame


class Player (pygame.sprite.Sprite): #sprite = element graphique du jeux qui peut intéragire avec d'autres sprite et qui est quelque chose de non statique

    #definir un sprite
    def __init__(self, x, y):
        super().__init__()#initialiser le sprite
        self.sprite_sheet = pygame.image.load('Player.png')#recuperer le spritsheet
        self.image = self.get_image(0, 0)#on ce sert de l'image qui a été découper
        self.image.set_colorkey(pygame.Color([0, 0, 0]))# retire la couleur de l'arriere plan du joueur
        self.rect = self.image.get_rect()#definit le rectangle qui est sa position
        self.position = [x, y]
        self.images_joueur = {
            "down" : self.get_image(0, 0),#les coordonnée en x est toujours a 0 car comme c'est la premiere image, elles sont aligné sur le meme axe donc c'est toujours 0 en x
            "left" : self.get_image(0, 32),
            "right": self.get_image(0, 64),
            "up" : self.get_image(0, 96)
        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12 )#Bloquer les extremité pour travarese les ponts etc / 12 = hauteur
        self.old_position = self.position.copy() #copy = dupliquer les informations et va eviter de  faire une relation entre les elements comme ça si le joueur ce deplace, ça ne va pas modifier le old_position. Il va etre modifié que a la postion avant de ce deplacer

        #self.speed = 3 pour ne pas coder en dur

    def save_location(self):
        self.old_position = self.position.copy() #copy duplique les informations et va eviter de faire une relation entre les elemnts comme ça si le joueur ce deplace ça neva pas modifié le old_position

    def change_animation (self, name):
        self.image = self.images_joueur[name]#va passer en parametre ce que nous voulons nommé avec images_joueur
        self.image.set_colorkey((0, 0, 0)) #‼️probleme : sa ne marche pas ‼️

    def move_right (self) :
        self.position[0] += 3 #permet de modifier la positioon en x et ajouté une vitesse (3)

    def move_left(self):
        self.position[0] -= 3 #ou self.speed qui est en commentaire

    def move_up(self) :
        self.position[1] -= 3

    def move_down (self) :
        self.position[1] += 3

    def update(self):
        self.rect.topleft = self.position #mettre a jour la position du joueur
        self.feet.midbottom = self.rect.midbottom #recupere le bas de ces pieds et faire attention an epas depasser les bords

    def move_back(self): #peremttera de ce replacer a la position avant qu'il y'a eu une collision
        self.position = self.old_position  # va prendre la valeur de son ancienne position pour qu'il ce replace en arriere
        self.rect.topleft = self.position  # mettre a jour la position du joueur
        self.feet.midbottom = self.rect.midbottom


    def get_image(self, x, y):#donner les coordonnées du personnage en x et en y
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))#absorbe notre sprite_sheet / () = extraoy un morceau = distance par défault
        return image #retourner l'image qui a été découper

