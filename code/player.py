import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
  def __init__(self,pos,groups,obstacle_sprites,create_attack):#between brackets we have the necessary parameters to initiated the class child Player#When a Player instance is created in level.py, it is added to the visible_sprites group but also given a reference to the obstacle_sprites group for collision detection purposes.
    super().__init__(groups) #Is a good idea that the groups enter as a parameters in our parent class in that way are going to be processed by the parent class (pygame.sprite.Sprite), this is often necessary to properly initialize the inherited properties and behaviors, and  also adding the objects to the groups without need to added them with the method .add When you have a class that inherits from pygame.sprite.Sprite and you want instances of that class to belong to certain sprite groups, you can pass the groups argument to super().__init__(groups). This is a common and effective way to automatically add instances of the class to those groups upon creation.
    self.image = pygame.image.load('/home/Orlando517/Documentos/lumetrio/python/rpg-game/graphics/test/player.png').convert_alpha()
    self.rect = self.image.get_rect(topleft = pos) # self.image.get_rect() is method  that  allows us to use properties like .x and get .y to get the coordinates easier and  other useful methods, topleft= pos helps us  to draw the image in the right left corner of his size, the coordenates given for that be given in the pos argument
    self.hitbox = self.rect.inflate(0, -26)##hit box is the size of a sprite(image)to collision,  in this case we need to oerlap a little the player image over the obstacules then we need to created and smaller hixbox area, We can do it by .inflate#inflate (x, y) takes a rectangule and changes the size

    # graphics setup
    self.import_player_assets()
    self.status = 'down'
    self.frame_index = 0
    self.animation_speed = 0.15

    # movement
    self.direction = pygame.math.Vector2()# self.direction = pygame.math.Vector2() creates a Vector2 object representing a 2D direction, often used in games for movement, aiming, orientation, and other vector-related tasks.When you call pygame.math.Vector2(), it creates a new Vector2 object with its components initialized to 0.0. So, self.direction is now a vector with both x and y components set to 0.0.
    self.speed = 5
    self.attacking = False
    self.attack_cooldown = 400
    self.attack_time = None
    self.obstacle_sprites = obstacle_sprites

    # weapon
    self.create_attack = create_attack #this  will be  the function that our class will receive when the level file is running
    self.weapon_index = 0 #later on we are going to use this number to select weapons
    self.weapon = list(weapon_data.keys())[self.weapon_index] # we are going to call only the keys in the weapon_data dictionary, to be able to use the index we convert the keys in a list
    

  def import_player_assets(self): #with this function we are going to import all the images concerning to player's attacks 
    character_path = '/home/Orlando517/Documentos/lumetrio/python/rpg-game/graphics/player/'
    self.animations = {'up': [], 'down': [],'left': [], 'right': [],
      'right_idle':[], 'left_idle':[], 'up_idle':[],'down_idle':[],
      'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}
    
    for animation in self.animations.keys():# for every item in the dictionary animations 
      full_path = character_path + animation
      self.animations[animation] = import_folder(full_path) #here we are adding the value to thekeyword in the dictionary animations also the value that we are goint to add it the importing function to make the folder's path from settings

  def input(self):
    if not self.attacking:
      keys = pygame.key.get_pressed()#pygame.key.get_pressed() returns a list-like object where each index corresponds to a key on the keyboard.Each index holds a value of 1 (True) if the key is pressed and 0 (False) if the key is not pressed.

      # movement input
      if keys[pygame.K_UP]: #If keys[pygame.K_UP] is True (which means the "up arrow" key is pressed), the following block of code will execute.
        self.direction.y = -1
        self.status = 'up'  #every time that we press the key K_UP or the corresponding will be changed the self.status
      elif keys[pygame.K_DOWN]:
        self.direction.y = 1
        self.status = 'down'
      else:
        self.direction.y = 0

      if keys[pygame.K_RIGHT]: #If keys[pygame.K_UP] is True (which means the "up arrow" key is pressed), the following block of code will execute.
        self.direction.x = 1
        self.status = 'right'
      elif keys[pygame.K_LEFT]:
        self.direction.x = -1
        self.status = 'left'
      else:
        self.direction.x = 0

      # attack input
      if keys[pygame.K_SPACE]:#and not self.attacking not self.attacking: This part checks if self.attacking is False. The not keyword negates the value of self.attacking. So, if self.attacking is False, not self.attacking is True. but  as we already madethat check at the beginning of the function then we can remove that partof the line
        self.attacking = True
        self.attack_time = pygame.time.get_ticks() # with this line we get the time when the action is taking place, this line will be running only once 
        self.create_attack()

      #magic input
      if keys[pygame.K_LCTRL]:
        self.attacking = True
        self.attack_time = pygame.time.get_ticks() # with this line we get the time when the action is taking place, this line will be running only once 
        print('magic')

  def get_status(self):

    # idle status
    if self.direction.x == 0 and self.direction.y == 0: 
      if not 'idle' in self.status and not 'attack' in self.status: # we are checking if the status already has the word idle in it, if not we are going to add it 
        self.status = self.status + '_idle'# if the condition is true then we will add _iddle to the current status
    
    if self.attacking:
      self.direction.x = 0
      self.direction.y = 0
      if not 'attack' in self.status: # we are checking if the status already has the word idle in it, if not we are going to add it 
        if 'idle' in self.status:#if idle is in self.status then we're going to overwrite it
          self.status = self.status.replace('_idle','_attack')#in this line we replace the word _idle in status for _attack
        else:
          self.status = self.status + '_attack'# if the condition is true then we will add _iddle to the current status     
    else:
      if 'attack' in self.status:#when is false we sure that the attack status doesn't continue by changining with an empty string ''
        self.status = self.status.replace( '_attack','')

  def move(self,speed):#we don't use self.speed becausewe  are going to make subsequentently another class in which the player and enemies can inherit methods  an attributes 
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

  def cooldowns(self):
    current_time = pygame.time.get_ticks() #this line is used to calculate the time and also help us to count the time of the actions that we make,this line will be running infinitely

    if self.attacking:
      if current_time -self.attack_time >= self.attack_cooldown:
        self.attacking = False # with this  we control the time of our attack
  
  def animate(self):
    animation = self.animations[self.status]# we are going to call the whole group of images that  are in the dictionary that match with the status

    #loop over the frame index
    self.frame_index += self.animation_speed # we want that our frame_index increases his value to call another image
    if self.frame_index >= len(animation): # with this contition we sure than when the loop reach out the last value, restart to 0 again
      self.frame_index = 0

    #set the image 
    self.image = animation[int(self.frame_index)] # we convert the index in an integer cause the self.animation_speed is 0.15 # if self.frame_index is 0.15 and you do int(self.frame_index), it will become 0, int(1.5) will result in 1,an so on
    self.rect = self.image.get_rect(center = self.hitbox.center)

  def update(self):#The update method in the Player class serves as a central hub for updating the player's state based on user input.By separating input handling into its own method and calling it within update, the code remains organized, modular, and follows standard game development practices.
    self.cooldowns()
    self.get_status()
    self.input()
    self.animate()
    self.move(self.speed)






