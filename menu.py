import pygame
from display_extras import *
from make_sprite import *
pygame.init()

buttons = ['play', 'about']
button_rects = {}
font = pygame.font.Font('others/VT323-Regular.ttf', 40)

#menu buttons
def make_button(screen, width, height, text, i):
  words = font.render(text, True, (0, 0, 0))
  img = pygame.image.load('others/speech.png')
  img = pygame.transform.scale(img, (words.get_width(), words.get_height()+6))
  img.blit(words, (0, 2))
  img_x = (width-img.get_width())//2
  img_y = height//3*(i+1)
  screen.blit(img, (img_x, img_y))

  left = pygame.image.load('others/left_bubble.png')
  left = pygame.transform.scale(left, (0.3125*img.get_height(), img.get_height()))
  screen.blit(left, (img_x-left.get_width(), img_y))
  right = pygame.image.load('others/right_bubble.png')
  right = pygame.transform.scale(right, (0.3125*img.get_height(), img.get_height()))
  screen.blit(right, (img_x+img.get_width(), img_y))

  img_rect = img.get_rect()
  img_rect.x = img_x
  img_rect.y = img_y
  img_rect.inflate_ip(img_rect.width*0.625, 0)
  return screen, img_rect

#menu page mode
def menu(screen, width, height):
  mode = 'menu'
  running = True
  bg = pygame.image.load('others/cover_image.png')
  bg = pygame.transform.scale(bg, (width, height))
  screen.blit(bg, (0, 0))

  for i in range(len(buttons)):
    button = buttons[i]
    screen, img_rect = make_button(screen, width, height, button, i)
    button_rects[button] = img_rect

  #checks for input to change mode or quit game
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      x, y = pygame.mouse.get_pos()
      for name, rect in button_rects.items():
        if rect.collidepoint(x, y):
          mode = name
    if event.type == pygame.QUIT:
      running = False
      
  return screen, mode, running

#about mode
def about(screen, width, height):
  mode = 'about'
  running = True
  bg = pygame.image.load('others/cover_image.png')
  bg = pygame.transform.scale(bg, (width, height))
  screen.blit(bg, (0, 0))

  instructions = pygame.image.load('others/instructions.png')
  instructions = pygame.transform.scale(instructions, (480, 480))
  screen.blit(instructions, (60, 60))

  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        mode = 'menu'
    if event.type == pygame.QUIT:
      running = False
  return screen, mode, running

frames = ['Well son, I guess I was wrong, you\'ve proved your worth', 'It\'s just a shame that you don\'t have the right gear to come on the raid', 'Maybe next year...', 'Hang on, you do have the right gear!', 'Alright, pack your bags, we\'re going to England']

#end cutscene mode
def end(screen, width, height, frame, floor, roof, roof_rect, outsides, block_size, inventory, sprites, sprite_names):
  if not 'sword' in sprite_names:
    sword = make_sprite('sword', sprites, block_size)
    inventory.add(sword)
    sprite_names.append('sword')
  people = ['father', 'mother', 'uncle', 'woman']
  dimensions = {'father':(block_size*0.825, block_size*1.5),
              'mother':(block_size*0.6, block_size*1.5),
              'uncle':(block_size*0.825, block_size*1.5),
              'woman':(block_size*0.6, block_size*1.5)}
  mode = 'end'
  running = True
  screen.blit(floor, (0, 0))
  screen.blit(roof, roof_rect)
  for item in outsides:
    if item.type != 'person':
      screen.blit(item.image, item.rect)
  for i in range(len(people)):
    file = f'others/{people[i]}.png'
    img = pygame.image.load(file)
    img = pygame.transform.scale(img, dimensions[people[i]])
    screen.blit(img, (width-block_size*(3+i)+6, block_size))
  player = pygame.image.load('player/player_back.png')
  player = pygame.transform.scale(player, (block_size*0.6, block_size))
  screen.blit(player, (width-block_size*2.8, block_size*3))

  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        frame += 1

  if frame >= len(frames):
    mode = 'done'
  else:
    text = display_text(frames[frame])
    screen = make_text_img(text, screen)
    screen = draw_inventory(screen, block_size, inventory, width, height)
    screen = show_progress(screen, block_size, width, height, 15)
  return screen, mode, running, frame

#final image
def done(screen, width, height, time_taken):
  mode = 'done'
  img = pygame.image.load('others/end_image.png')
  img = pygame.transform.scale(img, (width, height))
  screen.blit(img, (0, 0))
  small_font = pygame.font.Font('others/VT323-Regular.ttf', 20)
  time = small_font.render(f'Time: {time_taken:.02f} seconds', True, (255, 255, 255))
  screen.blit(time, (0, 0))
  running = True
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        mode = 'menu'
  return screen, running, mode