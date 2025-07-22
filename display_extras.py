import pygame
pygame.init()

#font used
font = pygame.font.Font('others/VT323-Regular.ttf', 20)

#code to make text and background
def display_text(text):
  words = font.render(text, True, (0, 0, 0))
  img = pygame.image.load('others/speech.png')
  img = pygame.transform.scale(img, (words.get_width(), words.get_height()+6))
  img.blit(words, (0, 2))
  return img

#makes sides of bubble and draws entire bubble to screen
def make_text_img(text_img, extras):
  left = pygame.image.load('others/left_bubble.png')
  left = pygame.transform.scale(left, (0.3125*text_img.get_height(), text_img.get_height()))
  extras.blit(left, (0, 0))
  extras.blit(text_img, (left.get_width(), 0))
  right = pygame.image.load('others/right_bubble.png')
  right = pygame.transform.scale(right, (0.3125*text_img.get_height(), text_img.get_height()))
  extras.blit(right, (left.get_width()+text_img.get_width(), 0))
  return extras

#loads the inventory image and draws all images on
def draw_inventory(extras, block_size, inventory, width, height):
  inventory_bg = pygame.image.load('others/inventory.png')
  inventory_bg = pygame.transform.scale(inventory_bg, (block_size*4.8, block_size))
  index = 0
  for item in inventory:
    img = item.image
    i_width = img.get_width()
    i_height = img.get_height()
    inventory_bg.blit(img, (index*block_size + (block_size-i_width)//2, (block_size-i_height)//2))
    index += 1
  extras.blit(inventory_bg, ((width-inventory_bg.get_width())//2, height-block_size))
  return extras

#draws the progress bar and rectangle showing progress
def show_progress(extras, block_size, width, height, progress):
  img = pygame.image.load('others/progress.png')
  img = pygame.transform.scale(img, (block_size*0.6, block_size*3.1))
  extras.blit(img, (width-block_size*0.6, block_size))
  green = (119, 237, 112)
  pygame.draw.rect(extras, green, (width-block_size*0.55, block_size*4.05-progress*block_size//5, block_size*0.5, progress*block_size//5))
  return extras