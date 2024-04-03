import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice # we need the choise method from random
from weapon import Weapon

class Level:
  def __init__(self):

    #get the display surface
    self.display_surface = pygame.display.get_surface() #is commonly used when you have a part of your code (like a class or module) that needs to interact with the main display surface, and you want to obtain a reference to that surface.

    #sprite group setup
    self.visible_sprites = YSortCameraGroup() #Sprites can be added to these groups, and the groups can be updated and drawn on the display surface.
    self.obstacle_sprites = pygame.sprite.Group()

    # sprite setup
    self.create_map()

  def create_map(self):
    layouts = {
      'boundary': import_csv_layout('/home/Orlando517/Documentos/lumetrio/python/rpg-game/map/map_FloorBlocks.csv'), # we are converting the cvs file in a dictionary to used as we used the setting world map # the file map_FloorBlocks.csv is one of the layers that we made for the map with the program tile and also is the exporting file of that layer that we made from that map
      'grass': import_csv_layout('/home/Orlando517/Documentos/lumetrio/python/rpg-game/map/map_Grass.csv'), #every one of the items contain in this dictionary are list to help us to position every detail in this case the grass by usingthe function import_csv_layout created in the file support.py
      'object': import_csv_layout('/home/Orlando517/Documentos/lumetrio/python/rpg-game/map/map_Objects.csv'),
    }
    graphics = {
      'grass': import_folder('/home/Orlando517/Documentos/lumetrio/python/rpg-game/graphics/Grass'),# in this case we are using the function that we created in support to get all the paths of the images that we need
      'objects': import_folder('/home/Orlando517/Documentos/lumetrio/python/rpg-game/graphics/Objects')
    }

    for style,layout in layouts.items():#style is going to be boundary right now and layout will be the import_csv_layout 
      for row_index,row in enumerate(layout):#The enumerate() function is a built-in Python function that takes an iterable (such as a list, tuple, or string) as input and returns an iterator that yields pairs of (index, value)##also  you can use the for loop with multiple variables by unpacking tuples or other iterable objects##
        for col_index, col in enumerate(row):
          if col != '-1':
            #Create the base floor and layouts
            x = col_index * TILESIZE
            y = row_index * TILESIZE

            if style == 'boundary':#we establish the file that we want to show by the key word boundary from the dictionary layouts
              Tile((x,y),[self.obstacle_sprites],'invisible')# we removed the self.visible_sprites from this because we dont want to see the tiles draw
            if style == 'grass':
              #create a grass tile
              random_grass_image = choice(graphics['grass'])# choice(graphics['grass']): This accesses a list of grass images from the graphics dictionary. The 'grass' key is used to retrieve this list.#choice(...): This function from the random module selects a random item from a sequence (like a list).#
              Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'grass',random_grass_image)# here we choose the grass images to be the surfaces to be draw

            if style == 'object':
              surf = graphics['objects'][int(col)]#here we are getting the surface in this way cause every image that will work as a surface it is different, with choosing it  from the list inside the dictionary
              Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)# here we choose the grass images to be the surfaces to be draw
    
    self.player = Player((2000,1430),[self.visible_sprites],self.obstacle_sprites,self.create_attack)#functions as self.create_attack never have to be called with the parenthesis included whe are used as a parameters inside other function

  def create_attack(self):
    Weapon(self.player,[self.visible_sprites])#we call the funcion Weapon an we passed the parameters tha can be find out in this class
  
  def destroy_weapon(self):

  def run(self):
    # update and draw the game
    self.visible_sprites.custom_draw(self.player)# we replaced teh draw method with the one we did
    self.visible_sprites.update()
    debug(self.player.status)
    

class YSortCameraGroup(pygame.sprite.Group):#in the YSortCameraGroup what we are doing is to override the pygame.sprite.Group function that comes build-in in python for the self.visible_sprites attribute
  def __init__(self):

    #general setup
    super().__init__()
    self.display_surface = pygame.display.get_surface()
    self.half_width = self.display_surface.get_size()[0] // 2 # get_size helps us to get a tuple with the width and height of our draw surface (width, height)
    self.half_height = self.display_surface.get_size()[1] // 2
    self.offset = pygame.math.Vector2()#we created a vector to sum an offset to the display to achieve the effect of a camera, the coordinates by defect without values will be 0

    #creating the floor
    self.floor_surf = pygame.image.load('/home/Orlando517/Documentos/lumetrio/python/rpg-game/graphics/tilemap/ground.png').convert()#we are adding the backgroup map image behind every other detail drawn in order to not cover , it means it will be the first one to be draw
    self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))# here we set the coordinates for the floor_suf (backgroup map image) 
  
  def custom_draw(self,player):
    
    #getting the offset
    self.offset.x = player.rect.centerx - self.half_width #we are calling the attribute player.rect from the class level  where  we are calling the class Player from the other file player
    self.offset.y = player.rect.centery - self.half_height #Subtracting self.half_height from player.rect.centery moves the "camera" up or down based on where the player is.

    #drawing the floor
    floor_offset_pos = self.floor_rect.topleft - self.offset
    self.display_surface.blit(self.floor_surf,floor_offset_pos)

    #for sprite in self.sprites():
    for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):# sorted take two parameters the first one is the group to organized , the second one  the key is the parameter by we are going to organized the group #When the sprites are sorted by centery, those with lower centery values (higher up on the screen) are drawn first. Then, as the loop progresses, sprites with higher centery values are drawn, ensuring that objects lower on the screen appear on top.
      offset_pos = sprite.rect.topleft - self.offset #topleft gives us the left top coordinates of our rectangule
      self.display_surface.blit(sprite.image, offset_pos)# blit()Draws a source Surface onto this Surface#The draw can be positioned with the dest argument. The dest argument can either be a pair of coordinates representing the position of the upper left corner of the blit or a Rect, where the upper left corner of the rectangle will be used as the position for the blit#blit(source, dest, area=None, special_flags=0)#the offset position will be the point from the entire game will start to be draw having into account that the offset will be subtracted fromt the coordinates of our player's image having  in this way a way to redraw the map froma  position relative to our character's image#sprite: This is a reference to an individual sprite in the YSortCameraGroup group.#.image: This is the attribute of the sprite that holds the surface representing its visual appearance.#The pygame.sprite.Group that we are working with contains all the sprites that we added to it from the Player class and the Tile class.


#self.visible_sprites.draw(self.display_surface)#The draw() method is a built-in method provided by pygame.sprite.Group. #When you call self.visible_sprites.draw(surface), you are telling Pygame to draw all the sprites in self.visible_sprites onto the specified surface
#in the run method ---->debug(self.player.direction)# we are usign the method debug fromt the file debug to see the  changes  in the direction attribute from the class player  
#always the sprites add it to pygame.sprite.Group() will be drawn in order, which means that it's going to draw the latest image added on the top of the others  
    # create an object tile
    #     if col == 'x':
    #       Tile((x,y),[self.visible_sprites,self.obstacle_sprites])#we are calling the class Tile from the file tile.py and we assigned the parameters in brackets
    #     if col == 'p':
    #       self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites)#When you have multiple sprite groups to pass, you need to enclose them in brackets to create a list.For example, if you have another sprite group self.other_sprites, you would pass both self.visible_sprites and self.other_sprites like this:Player((x, y), [self.visible_sprites, self.other_sprites])
