import pygame

class Weapon(pygame.sprite.Sprite):
  def __init__(self,player,groups):
    super().__init__(groups)
    direction = player.status.split('_')[0]# the split method needs two arguments, the first one is at which character we want to split things, and the second one is how many times the string can be divided in this case we won't use it, if  he doesn't find an underscore then they simply ignore it, as the split is goint to return in some cases a list with two elements we are going to choose the first one  tha is the one with the direction [0]

    # graphic
    full_path = f'/home/Orlando517/Documentos/lumetrio/python/rpg-game/graphics/weapons/{player.weapon}/{direction}.png'
    self.image = pygame.image.load(full_path).convert_alpha() # pygame.Surface((40,40))we created the surface to the  weapons but also can be created only by loading an image
    
    # placement
    if direction == 'right':
      self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))#we are placing the initial coordinates to draw the midleft position of our weapon in the midright position of our player ,  also in order that the weapon looks good we added an offset(pygame.math.Vector2)
    elif direction == 'left':
      self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
    elif direction == 'down':
      self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
    else:
      self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
