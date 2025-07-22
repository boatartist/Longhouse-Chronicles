import pygame
pygame.init()

#image files for chicken to loop through
frames = ['chicken/up.png', 'chicken/down.png', 'chicken/up2.png', 'chicken/down2.png']

#function to manage chicken's position and appearance every frame
def chicken_dance(frame, chicken, block_size, movement):
  left_border = block_size
  right_border = block_size*4
  chicken.rect.x += movement
  if not left_border < chicken.rect.x < right_border:
    movement *= -1
  pic_n = frame//4%2
  if movement < 0:
    pic_n += 2
  pic = pygame.image.load(frames[pic_n])
  chicken.image = pygame.transform.scale(pic, (block_size*0.9, block_size*0.9))
  return chicken, movement