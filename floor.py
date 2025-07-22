import pygame
import random
pygame.init()

def make_floors(block_size, width, height, longhouse_x, longhouse_y, longhouse_width, longhouse_height):
  #make floor image                                       
  #ocean
  floor = pygame.Surface((width, height))
  for x in range(0, width, block_size):
    img = pygame.image.load(f'floor/ocean1.png')
    img = pygame.transform.scale(img, (block_size, block_size))
    floor.blit(img, (x, 0))
    
   #sand 
  for x in range(0, width, block_size):
    num = random.randint(1, 2)
    img = pygame.image.load(f'floor/sand{num}.png')
    img = pygame.transform.scale(img, (block_size, block_size))
    floor.blit(img, (x, block_size))
  
  #grass
  for x in range(0, width, block_size):
    for y in range(block_size*2, height, block_size):
      img = pygame.image.load(random.choice(['floor/floor1.png', 'floor/floor2.png', 'floor/floor3.png', 'floor/floor4.png']))
      img = pygame.transform.scale(img, (block_size, block_size))
      floor.blit(img, (x, y))
  
  #bottom of wharf which can be walked over
  img = pygame.image.load('wharf/plank_lower.png')
  img = pygame.transform.scale(img, (block_size, block_size))
  floor.blit(img, (width-block_size*3, block_size*2))
  
  #fence
  for x in range(0, width, block_size):
    img = pygame.image.load('floor/fence.png')
    img = pygame.transform.scale(img, (block_size, block_size))
    floor.blit(img, (x, height-block_size))
  
  #surface to block out outside while inside
  black_out = pygame.image.load('floor/black_out.png')
  black_out = pygame.transform.scale(black_out, (width, height))
  
  #door img inside
  door_img = pygame.image.load('floor/door.png')
  door_img = pygame.transform.scale(door_img, (block_size, block_size*2))
  black_out.blit(door_img, (longhouse_x+longhouse_width, longhouse_y + block_size))
  
  #inside floor
  for x in range(longhouse_x, longhouse_x+longhouse_width, block_size):
    for y in range(longhouse_y, longhouse_y+longhouse_height, block_size):
      img = pygame.image.load(random.choice(['floor/straw1.png', 'floor/straw2.png']))
      img = pygame.transform.scale(img, (block_size, block_size))
      floor.blit(img, (x, y))
      black_out.blit(img, (x, y))
  
  #roof surface
  roof = pygame.image.load('floor/roof.png')
  roof = pygame.transform.scale(roof, (longhouse_width, longhouse_height))
  roof_rect = roof.get_rect()
  roof_rect.x = longhouse_x
  roof_rect.y = longhouse_y
  
  #door rect
  door = pygame.Rect(width-block_size*3.5, block_size*6, block_size, block_size*2)
  
  #inside floor rect
  floor_rect = pygame.Rect((longhouse_x, longhouse_y, longhouse_width, longhouse_height))

  #empty farm
  img = pygame.image.load('floor/farm_cleared.png')
  img = pygame.transform.scale(img, (block_size*3, block_size*2))
  floor.blit(img, (longhouse_x, height-block_size*3))

  return floor, black_out, roof, door, floor_rect, roof_rect