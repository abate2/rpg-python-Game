import pygame
from settings import *

class Player(pygame.sprite.Sprite):
  def __init__(self,pos,groups,obstacle_sprites):#between brackets we have the necessary parameters to initiated the class child Player#When a Player instance is created in level.py, it is added to the visible_sprites group but also given a reference to the obstacle_sprites group for collision detection purposes.
    super().__init__(groups) #Is a good idea that the groups enter as a parameters in our parent class in that way are going to be processed by the parent class (pygame.sprite.Sprite), this is often necessary to properly initialize the inherited properties and behaviors, and  also adding the objects to the groups without need to added them with the metho .add When you have a class that inherits from pygame.sprite.Sprite and you want instances of that class to belong to certain sprite groups, you can pass the groups argument to super().__init__(groups). This is a common and effective way to automatically add instances of the class to those groups upon creation.
    self.image = pygame.image.load('/home/Orlando517/Documentos/lumetrio/python/rpg-game/graphics/test/player.png').convert_alpha()
    self.rect = self.image.get_rect(topleft = pos) # self.image.get_rect() is method  that  allows us to use properties like .x and get .y to get the coordinates easier and  other useful methods, topleft= pos helps us  to draw the image in the right left corner of his size, the coordenates given for that be given in the pos argument
    self.hitbox = self.rect.inflate(0, -26)##hit box is the size of a sprite(image)to collision,  in this case we need to oerlap a little the player image over the obstacules then we need to created and smaller hixbox area, We can do it by .inflate#inflate (x, y) takes a rectangule and changes the size

    self.direction = pygame.math.Vector2()# self.direction = pygame.math.Vector2() creates a Vector2 object representing a 2D direction, often used in games for movement, aiming, orientation, and other vector-related tasks.When you call pygame.math.Vector2(), it creates a new Vector2 object with its components initialized to 0.0. So, self.direction is now a vector with both x and y components set to 0.0.
    self.speed = 5

    self.obstacle_sprites = obstacle_sprites

  def input(self):
    keys = pygame.key.get_pressed()#pygame.key.get_pressed() returns a list-like object where each index corresponds to a key on the keyboard.Each index holds a value of 1 (True) if the key is pressed and 0 (False) if the key is not pressed.

    if keys[pygame.K_UP]: #If keys[pygame.K_UP] is True (which means the "up arrow" key is pressed), the following block of code will execute.
      self.direction.y = -1
    elif keys[pygame.K_DOWN]:
      self.direction.y = 1
    else:
      self.direction.y = 0

    if keys[pygame.K_RIGHT]: #If keys[pygame.K_UP] is True (which means the "up arrow" key is pressed), the following block of code will execute.
      self.direction.x = 1
    elif keys[pygame.K_LEFT]:
      self.direction.x = -1
    else:
      self.direction.x = 0

  def move(self,speed):#we  don't use self.speed becausewe  are going to make subsequentently another class in which the player and enemies can inherit methods  an attributes 
    if self.direction.magnitude() != 0:
      self.direction = self.direction.normalize()#A unit vector is a vector that has a magnitude (length) of 1 but retains the same direction as the original vector.When you normalize a vector, you are essentially "scaling" it down to a length of 1 while keeping its direction intact.#The self.direction = self.direction.normalize() line normalizes the self.direction vector.#This step ensures that the sprite moves at a consistent speed in any direction, without any bias towards diagonals or cardinals

    self.hitbox.x += self.direction.x * speed
    self.collision('horizontal') # we are activating the collisions whe there is movement,in this way always when there's movement the collisions will be activated
    self.hitbox.y += self.direction.y * speed 
    self.collision('vertical')
    self.rect.center = self.hitbox.center

    #self.rect.center += self.direction * speed #When you use self.rect.center, you are accessing the center point of the sprite's rectangle.

  def collision(self,direction):
    if direction == 'horizontal':
      for sprite in self.obstacle_sprites:
          if sprite.hitbox.colliderect(self.hitbox):# we are checking if the self.hitbox(player) will collide with the sprites in self.obstacle_sprites
            if self.direction.x > 0: #moving right#if  we are moving to the right
              self.hitbox.right = sprite.hitbox.left # in this line we sure that then the player overlaps with an obstacule,  only the left side of our player get in contact with the obstacule #.right: This is one of the properties of a Rect object in Pygame. It represents the x-coordinate of the right side of the rectangle.#self.rect: This refers to the rect attribute of the Player sprite. As mentioned earlier, it represents the rectangular area that defines the position and size of the Player sprite on the screen.#.right: This is one of the properties of a Rect object in Pygame. It represents the x-coordinate of the right side of the rectangle.#sprite.rect: This refers to the rect attribute of the sprite object, which is an obstacle sprite. This rect defines the position and size of the obstacle sprite.#.left: This is another property of a Rect object. It represents the x-coordinate of the left side of the rectangle.
            if self.direction.x < 0: #moving left
              self.hitbox.left = sprite.hitbox.right #here we are converting the coordinates of the right side of the obstacule  that  we received from the level file when it starts the program , then we can use the own attributes or functions of the self.obstacle_sprites = pygame.sprite.Group() defined in the level file   
   
    if direction == 'vertical':
      for sprite in self.obstacle_sprites:
        if sprite.hitbox.colliderect(self.hitbox):
          if self.direction.y > 0: #moving down
            self.hitbox.bottom = sprite.hitbox.top
          if self.direction.y < 0: #moving up
            self.hitbox.top = sprite.hitbox.bottom #


  def update(self):#The update method in the Player class serves as a central hub for updating the player's state based on user input.By separating input handling into its own method and calling it within update, the code remains organized, modular, and follows standard game development practices.
    self.input()
    self.move(self.speed)






