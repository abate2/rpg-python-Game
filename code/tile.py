import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
  def __init__(self,pos,groups):# self it is a key word  that  we are going to use to express the attributes e.g: self.image , it could be anothe word like sexy e.g sexy.image
    super().__init__(groups) #Is a good idea that the groups enter as a parameters in our parent class in that way are going to be processed by the parent class (pygame.sprite.Sprite), this is often necessary to properly initialize the inherited properties and behaviors.
    self.image = pygame.image.load('/home/Orlando517/Documentos/lumetrio/python/rpg-game/graphics/test/rock.png').convert_alpha() #we load the image then we convert it in alpha
    self.rect = self.image.get_rect(topleft = pos) # self.image.get_rect() this method allows us to use properties like .x and get .y to get the coordinates easier and other useful methods
    self.hitbox = self.rect.inflate(0, -10)#hit box is the size of a sprite(image)to collision,  in this case we need to oerlap a little the player image over the obstacules then we need to created and smaller hixbox area, We can do it by .inflate#inflate (x, y) takes a rectangule and changes the size

