import pygame
from make_sprite import *
from display_extras import *
pygame.init()

#person: (desired_item, before_speech, during_speech, (optional bonus item), after_speech)
desired_items = {'father':(['stew'], ('No son, you haven\'t proved yourself worthy', 'That stew was amazing, thank you', 'helmet', 'I\'d let you come, but you don\'t have enough gear')), 
                 'mother':(['bread', 'scythe'], ('I need to bake some bread to go with dinner', 'Thank you so much for that bread, here\'s some stew for your dad', 'stew', 'Not now son, I\'m busy cooking')), 
                 'aunt':(['rod'], ('Hello nephew, I seem to be missing my fishing rod, have you seen it?', 'Thank you so much for finding my fishing rod, here\'s a fish I caught earlier', 'fish', 'I hope I finish this weaving before the raid')),
                'uncle':(['wood'], ('Hey mate, don\'t suppose you could find some wood for me could you?', 'Thanks, now I can finish my sword, take this as thanks', 'key', 'You\'re trying to get your dad\'s approval, right? Use the key'))}

to_exclude = ['father', 'uncle']
def person(item, sprite_names, objects, inventory, inventory_size, sprites, insides, outsides, floor_rect, block_size, progress, increment):
  text_img = None
  desired_item = desired_items[item.name][0]
  if not item.found:
    if desired_item[-1] not in sprite_names and item.name not in to_exclude:
      progress += increment
      sprite_names.append(desired_item[-1])
      sprit = make_sprite(desired_item[-1], sprites, block_size)
      objects.add(sprit)
      if sprit.rect.colliderect(floor_rect):
        insides.add(sprit)
      else:
        outsides.add(sprit)
    for thing in inventory:
      if thing.name == desired_item[0]:
        inventory_size -= 1
        item.found = True
        inventory.remove(thing)
        progress += increment
  if item.found:
    bonus = desired_items[item.name][1][2]
    if not bonus in sprite_names:
      sprite_names.append(bonus)
      sprit = make_sprite(bonus, sprites, block_size)
      inventory_size += 1
      inventory.add(sprit)
      progress += increment
      text_img = display_text(desired_items[item.name][1][1])
    else:
      text_img = display_text(desired_items[item.name][1][3])
  else:
    text_img = display_text(desired_items[item.name][1][0])
  return sprite_names, text_img, objects, inventory, inventory_size, insides, outsides, progress