import pygame
from display_extras import *
from floor import *
from food_tool import *
from make_sprite import *
from person import *
from chicken import *

pygame.init()

#runs every frame when in playing mode
def main(width, height, screen, floor, text_img, speed, frame, front_frames,
         back_frames, player, block_size, left_frames, right_frames, insides,
         outsides, inside, door, longhouse_x, longhouse_y, longhouse_width,
         longhouse_height, objects, facts, inventory_spot, sprites, inventory,
         sprite_names, progress, increment, roof_rect, floor_rect, moving,
         black_out, roof, collided_speaker_rect, chicken_frame, chicken_movement, time_taken, transparent_rect):
  space = False
  mode = 'play'

  extras = pygame.Surface((width, height)).convert_alpha()
  extras.fill((0, 0, 0, 0))
  x_change = 0
  y_change = 0
  screen.blit(floor, (0, 0))

  for item in objects:
    if item.type == 'chicken':
      objects.remove(item)
      outsides.remove(item)
      item, chicken_movement = chicken_dance(chicken_frame, item, block_size, chicken_movement)
      objects.add(item)
      outsides.add(item)

  #checks for key presses
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        if text_img:
          text_img = None
        else:
          space = True
      if event.key == pygame.K_ESCAPE:
        mode = 'menu'

  keys = pygame.key.get_pressed()

  #checks to see if arrow keys are pressed and changes movement and appearance accordingly
  if keys[pygame.K_UP] or keys[pygame.K_w]:
    y_change -= speed
    frame += 1
    if frame >= len(back_frames):
      frame -= len(back_frames)
    img = pygame.image.load(back_frames[frame])
    player.image = pygame.transform.scale(img, (block_size * 0.6, block_size))

  elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
    y_change += speed
    frame += 1
    if frame >= len(front_frames):
      frame -= len(front_frames)
    img = pygame.image.load(front_frames[frame])
    player.image = pygame.transform.scale(img, (block_size * 0.6, block_size))

  elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
    x_change -= speed
    frame += 1
    if frame >= len(left_frames):
      frame -= len(left_frames)
    img = pygame.image.load(left_frames[frame])
    player.image = pygame.transform.scale(img, (block_size * 0.6, block_size))

  elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    x_change += speed
    frame += 1
    if frame >= len(right_frames):
      frame -= len(right_frames)
    img = pygame.image.load(right_frames[frame])
    player.image = pygame.transform.scale(img, (block_size * 0.6, block_size))

  else:
    img = pygame.image.load('player/player_front.png')
    player.image = pygame.transform.scale(img, (block_size * 0.6, block_size))

  #moves player and checks for collisions with items inside (if inside) or outside (if outside)
  player.rect.x += x_change
  if (inside and pygame.sprite.spritecollideany(player, insides)) or (
      not inside and pygame.sprite.spritecollideany(player, outsides)):
    player.rect.x -= x_change

  player.rect.y += y_change
  if (inside and pygame.sprite.spritecollideany(player, insides)) or (
      not inside and pygame.sprite.spritecollideany(player, outsides)):
    player.rect.y -= y_change

  #stop player leaving screen
  if player.rect.x < 0:
    player.rect.x = 0
  elif player.rect.x + block_size > width:
    player.rect.x = width - block_size
  if player.rect.y < block_size:
    player.rect.y = block_size
  elif player.rect.y > height - block_size * 2:
    player.rect.y = height - block_size * 2

  past_setting = inside
  #set inside or outside
  if player.rect.colliderect(roof_rect):
    inside = True
  else:
    inside = False

  #prevents player from walking through walls
  if past_setting != inside and not player.rect.colliderect(door):
    player.rect.x -= x_change
    player.rect.y -= y_change
    inside = not inside
  if inside and player.rect.y + player.rect.height > longhouse_y + longhouse_height:
    player.rect.y -= y_change
  if inside and (player.rect.x < longhouse_x
                 or player.rect.x + player.rect.width > longhouse_x +
                 longhouse_width) and not player.rect.colliderect(door):
    player.rect.x -= x_change

  bubbles = []
  order = ['person', 'challenge', 'food', 'tool', 'informative', 'chicken']
  for item in objects:
    if item.type in [
        'person', 'food', 'tool', 'informative', 'challenge', 'chicken']:
      if (item.rect.colliderect(floor_rect)
          and inside) or (not item.rect.colliderect(floor_rect)
                          and not inside):
        if item.larger_rect.colliderect(player.rect):
          bubbles.append(item)

  if len(bubbles) > 0:
    bubbles.sort(key=lambda item: order.index(item.type))
    item = bubbles[0]
    bubble = pygame.image.load('others/bubble.png')
    bubble = pygame.transform.scale(bubble,
                                    (block_size * 0.45, block_size * 0.25))
    bubble_x = item.rect.x + (item.rect.width - bubble.get_width()) // 2
    bubble_y = item.rect.y - bubble.get_height() - 2
    extras.blit(bubble, (bubble_x, bubble_y))
    if space:
      if item.type == 'informative':
        text_img = display_text(facts[item.name])
      elif item.type == 'challenge':
        inventory, insides, outsides, objects, sprite_names, text_img, progress = challenge(
            item, inventory, inventory_spot, insides, outsides, objects,
            sprites, block_size, sprite_names, progress, increment)
      elif item.type == 'food' or item.type == 'tool':
        objects, inventory, text_img, insides, outsides, progress = food_tool(
            inventory_spot, objects, inventory, item, insides, outsides,
            progress, increment)
      elif item.type == 'person':
        sprite_names, text_img, objects, inventory, inventory_size, insides, outsides, progress = person(
            item, sprite_names, objects, inventory, inventory_spot, sprites,
            insides, outsides, floor_rect, block_size, progress, increment)
      elif item.type == 'chicken':
        text_img = display_text('Long-legged Chicken: Helping remove bugs since 793')

      collided_speaker_rect = item.larger_rect

  if collided_speaker_rect:
    if not player.rect.colliderect(collided_speaker_rect):
      text_img = None
      collided_speaker_rect = None

  #make inventory
  extras = draw_inventory(extras, block_size, inventory, width, height)

  #display speech
  if text_img:
    extras = make_text_img(text_img, extras)

  #draw sprites if inside
  if inside:
    screen.blit(black_out, (0, 0))
    insides.draw(screen)
  moving.draw(screen)
  #draw sprites if outside
  if not inside:
    outsides.draw(screen)
    screen.blit(roof, roof_rect)

  #draw progress
  extras = show_progress(extras, block_size, width, height, progress)
  screen.blit(extras, (0, 0))

  #display speedrun timer
  small_font = pygame.font.Font('others/VT323-Regular.ttf', 20)
  time = small_font.render(f'Time: {time_taken:.02f}', True, (0, 0, 0))
  screen.blit(transparent_rect, (width-block_size*3, height-block_size))
  screen.blit(time, (width-block_size*2.75, height-block_size*0.75))

  return screen, text_img, frame, player, insides, outsides, inside, objects, inventory_spot, inventory, sprite_names, progress, collided_speaker_rect, mode, chicken_movement