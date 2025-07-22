import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import random
import time
from make_sprite import *
from person import *
from display_extras import *
from food_tool import *
from floor import *
from main_game import *
from menu import *
from chicken import *

#constants
width = 600
height = 600
block_size = 40
speed = 6
longhouse_x = block_size * 2
longhouse_y = block_size * 5
longhouse_width = block_size * 10
longhouse_height = block_size * 6

#pygame initiating stuff
pygame.init()
pygame.display.set_caption('Viking')
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

#player frames
front_frames = [
    'player/player_front.png', 'player/player_front_step1.png',
    'player/player_front.png', 'player/player_front_step2.png'
]
back_frames = [
    'player/player_back.png', 'player/player_back_step1.png',
    'player/player_back.png', 'player/player_back_step2.png'
]
left_frames = [
    'player/player_left.png', 'player/player_left_step.png',
    'player/player_left.png', 'player/player_left_step.png'
]
right_frames = [
    'player/player_right.png', 'player/player_right_step.png',
    'player/player_right.png', 'player/player_right_step.png'
]

#education
facts = {
    'cow':'Moo *in some longhouses, animals lived inside, especially in winter*',
    'beds':'Most vikings slept on raised wooden platforms, under furs or blankets',
    'cauldron':'Cooking cauldrons were suspended from the ceiling above a fire',
    'forge': 'Viking blacksmithing was very advanced for the time',
    'unlocked_chest': 'The chest is empty'
}

#name: (filename, dimensions, coordinates, type)
sprites = {
    'mid_wharf': ('wharf/plank.png', (block_size, block_size),
                  (width - block_size * 3, block_size), 'wharf'),
    'upper_wharf': ('wharf/plank.png', (block_size, block_size),
                    (width - block_size * 3, 0), 'wharf'),
    'barrel': ('objects/barrel.png', (block_size, block_size),
               (longhouse_x + block_size * 3,
                longhouse_y + longhouse_height - block_size), 'object'),
    'stew': ('objects/stew.png', (block_size * 0.8, block_size * 0.8),
             (block_size * 5, block_size * 7), 'food'),
    'cauldron': ('objects/cauldron.png', (block_size, block_size),
                 (block_size * 5, block_size * 7), 'informative'),
    'shield':
    ('objects/shield1.png', (block_size, block_size),
     (longhouse_x + longhouse_width - block_size, longhouse_y), 'tool'),
    'table': ('objects/table.png', (block_size, block_size * 2),
              (block_size * 10, block_size * 7), 'object'),
    'bread': ('objects/bread.png', (block_size * 0.7, block_size * 0.35),
              (block_size * 10 + block_size * 0.15,
               block_size * 7 + block_size * 1.2), 'food'),
    'fish': ('objects/fish.png', (block_size * 0.75, block_size * 0.375),
             (block_size * 10.1, block_size * 7.2), 'food'),
    'father': ('others/father.png', (block_size * 0.825, block_size * 1.5),
               (width - block_size * 3 + 6, block_size), 'person'),
    'mother': ('others/mother.png', (block_size * 0.6, block_size * 1.5),
               (longhouse_x + block_size * 3.2,
                longhouse_y + block_size * 0.4), 'person'),
    'rod': ('objects/rod.png', (block_size * 0.75, block_size * 0.9),
            (0, block_size * 0.6), 'tool'),
    'axe':
    ('objects/axe.png', (block_size * 0.95, block_size * 0.9),
     (longhouse_x + longhouse_width - block_size * 2, longhouse_y), 'tool'),
    'cow': ('others/cow.png', (block_size * 2, block_size * 1.5),
            (longhouse_x, longhouse_y - block_size * 0.5), 'informative'),
    'loom':
    ('objects/loom.png', (block_size, block_size * 2),
     (longhouse_x + block_size * 6, longhouse_y - block_size * 1.9), 'object'),
    'aunt': ('others/woman.png', (block_size * 0.6, block_size * 1.5),
             (longhouse_x + block_size * 6.2, longhouse_y), 'person'),
    'chest': ('objects/chest.png', (block_size * 2, block_size),
              (longhouse_x, longhouse_y + block_size * 4), 'challenge'),
    'unlocked_chest':
    ('objects/chest.png', (block_size * 2, block_size),
     (longhouse_x, longhouse_y + block_size * 4), 'informative'),
    'inside_fence_up': ('objects/inside_fence.png', (block_size // 4,
                                                     block_size * 1.2),
                        (longhouse_x + block_size * 2.2,
                         longhouse_y - block_size * 0.3), 'object'),
    'inside_fence_side':
    ('objects/inside_fence_side.png', (block_size * 2.4, block_size * 0.6),
     (longhouse_x, longhouse_y + block_size * 0.8), 'object'),
    'beds': ('floor/beds.png', (block_size * 6, block_size * 1.2),
             (longhouse_x + block_size * 4,
              longhouse_y + longhouse_height - block_size * 1.2),
             'informative'),
    'tree': ('objects/tree.png', (block_size * 1.5, block_size * 3),
             (block_size * 0.25, block_size * 8), 'challenge'),
    'stump': ('objects/stump.png', (block_size * 0.15, block_size * 0.52),
              (block_size * 0.9, block_size * 10.4), 'finished_challenge'),
    'wood': ('objects/wood.png', (block_size * 0.85, block_size * 0.95),
             (0, 0), 'tool'),
    'uncle': ('others/uncle.png', (block_size * 0.825, block_size * 1.5),
              (width - block_size * 2, height - block_size * 3.5), 'person'),
    'key': ('objects/key.png', (block_size * 0.5, block_size * 0.2),
            (block_size, block_size), 'tool'),
    'forge': ('objects/forge.png', (block_size * 4, block_size * 0.9),
              (width - block_size * 4.5,
               height - block_size * 2), 'informative'),
    'sword': ('objects/sword.png', (block_size, block_size), (0, 0), 'tool'),
    'helmet': ('objects/helmet.png', (block_size, block_size), (0, 0), 'tool'),
    'farm': ('floor/farm_full.png', (block_size*3, block_size*2), (longhouse_x, height-block_size*3), 'challenge'),
    'empty_farm':('floor/farm_cleared.png', (block_size*3, block_size*2), (width, height), 'finished_challenge'),
    'scythe':('objects/scythe.png', (block_size, block_size), (longhouse_x + longhouse_width-block_size, longhouse_y), 'tool'),
    'chicken':('chicken/up.png', (block_size * 0.9, block_size*0.9), (block_size, block_size*2), 'chicken')}

#things that need to be reset at each new play
def initialise():
  #variables
  running = True
  frame = 0
  inside = False
  progress = 0
  increment = 1
  max_points = 16
  
  #sprite groups
  moving = pygame.sprite.Group()
  objects = pygame.sprite.Group()
  insides = pygame.sprite.Group()
  outsides = pygame.sprite.Group()
  inventory = pygame.sprite.Group()
  
  #player sprite and frames
  player = pygame.sprite.Sprite()
  img = pygame.image.load('player/player_front.png')
  player.image = pygame.transform.scale(img, (block_size * 0.6, block_size))
  player.rect = player.image.get_rect()
  player.rect.x = 140
  player.rect.y = 140
  moving.add(player)
  
  floor, black_out, roof, door, floor_rect, roof_rect = make_floors(
      block_size, width, height, longhouse_x, longhouse_y, longhouse_width,
      longhouse_height)
  
  #make these objects at start (others added later)
  sprite_names = [
      'mid_wharf', 'upper_wharf', 'barrel', 'cauldron', 'table', 'father',
      'mother', 'axe', 'cow', 'aunt', 'loom', 'chest', 'inside_fence_up',
      'inside_fence_side', 'beds', 'tree', 'uncle', 'forge', 'farm', 'chicken'
  ]
  
  for name in sprite_names:
    sprit = make_sprite(name, sprites, block_size)
    if sprit.rect.colliderect(floor_rect):
      insides.add(sprit)
    else:
      outsides.add(sprit)
    objects.add(sprit)
  
  show_text = False
  text_img = None
  
  inventory_spot = 0
  collided_speaker_rect = None
  
  mode = 'menu'
  time_taken = 0
  chicken_frame = 0
  chicken_movement = 2

  transparent_rect = pygame.Surface((block_size*3, block_size))
  transparent_rect.set_alpha(100)
  transparent_rect.fill((200, 200, 200))

  return running, frame, inside, progress, increment, max_points, moving, objects, insides, outsides, inventory, player, floor, black_out, roof, door, floor_rect, roof_rect, show_text, text_img, inventory_spot, collided_speaker_rect, mode, time_taken, chicken_frame, chicken_movement, sprite_names, transparent_rect

running, frame, inside, progress, increment, max_points, moving, objects, insides, outsides, inventory, player, floor, black_out, roof, door, floor_rect, roof_rect, show_text, text_img, inventory_spot, collided_speaker_rect, mode, time_taken, chicken_frame, chicken_movement, sprite_names, transparent_rect = initialise()

while running:
  start_time = None
  if mode == 'play':
    start_time = time.time()
    screen, text_img, frame, player, insides, outsides, inside, objects, inventory_spot, inventory, sprite_names, progress, collided_speaker_rect, mode, chicken_movement = main(
        width, height, screen, floor, text_img, speed, frame, front_frames,
        back_frames, player, block_size, left_frames, right_frames, insides,
        outsides, inside, door, longhouse_x, longhouse_y, longhouse_width,
        longhouse_height, objects, facts, inventory_spot, sprites, inventory,
        sprite_names, progress, increment, roof_rect, floor_rect, moving,
        black_out, roof, collided_speaker_rect, chicken_frame, chicken_movement, time_taken, transparent_rect)
    
  elif mode == 'menu':
    screen, mode, running = menu(screen, width, height)

  elif mode == 'about':
    screen, mode, running = about(screen, width, height)

  elif mode == 'end':
    screen, mode, running, frame = end(screen, width, height, frame, floor, roof, roof_rect, outsides, block_size, inventory, sprites, sprite_names)

  elif mode == 'done':
    screen, running, mode = done(screen, width, height, time_taken)
    if mode == 'menu':
      print('run again')
      running, frame, inside, progress, increment, max_points, moving, objects, insides, outsides, inventory, player, floor, black_out, roof, door, floor_rect, roof_rect, show_text, text_img, inventory_spot, collided_speaker_rect, mode, time_taken, chicken_frame, chicken_movement, sprite_names, transparent_rect = initialise()
    
  if progress >= max_points:
    mode = 'end'
    frame = 0
    progress = 0
    
  pygame.display.update()
  clock.tick(20)
  chicken_frame += 1
  if chicken_frame > 200:
    chicken_frame = 0
  if mode == 'play' and start_time:
    end_time = time.time()
    time_taken += end_time-start_time

pygame.quit()