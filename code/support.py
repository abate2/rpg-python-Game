from csv import reader #this is going to allow us read the csv file esential to place all our tiles
from os import walk 
import pygame

def import_csv_layout(path):
  terrain_map = []
  with open(path) as level_map:#Inside the function, the with statement is used to open the CSV file located at the given path. The open() function is used to open the file in a way that ensures it is properly closed after the block of code inside the with statement is executed.
    layout = reader(level_map, delimiter = ',') # the reader needs two arguments the first one is the file that we are going to need , and de second one is a delimitator this one will separate the data, in this case we use the comma(,)
    for row in layout:#then we are going to use this for to get the data fromthe cvs file 
      terrain_map.append(list(row))
    return terrain_map

def import_folder(path):
  surface_list = []

  for _,__,img_files in walk(path):#walk is a build-in function os#when we are using we need to give the path to the directory then it will return a 3-tuple containing: 1)The directory path (root): The current directory being traversed. 2)A list of the names of the subdirectories in the current directory (directories).3)A list of the names of the non-directory files in the current directory (files).
    for image in img_files:
      full_path = path + '/' + image # we are creating the path for every image inside the directory with the info that we got from walk
      image_surf = pygame.image.load(full_path).convert_alpha()
      surface_list.append(image_surf)
 
  return surface_list


#in the map made in tile the obstacules are represented as '395' the '-1' will be empty space
#we don't have to initialize pygame with pygame.init() here cause it has already been initiated in the main file