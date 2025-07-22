import pygame
pygame.init()

#initialises sprites
def make_sprite(name, sprites, block_size):
  sprit = pygame.sprite.Sprite()
  info = sprites[name]
  img = pygame.image.load(info[0])
  img = pygame.transform.scale(img, info[1])
  sprit.image = img
  sprit.rect = sprit.image.get_rect()
  sprit.rect.x, sprit.rect.y = info[2]
  sprit.type = info[3]
  sprit.name = name
  sprit.larger_rect = sprit.rect.inflate(block_size*1.6, block_size*1.6)
  if sprit.type == 'person':
    sprit.found = False
  return sprit