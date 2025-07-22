import pygame
from display_extras import *
from make_sprite import *
pygame.init()

#deals with collecting food or tools when user interacts with one
def food_tool(inventory_spot, objects, inventory, item, insides, outsides, progress, increment):
  if inventory_spot < 5:
    inventory_spot += 1
    objects.remove(item)
    if item in insides:
      insides.remove(item)
    else:
      outsides.remove(item)
    inventory.add(item)
    progress += increment
    if item.name[0].lower() in 'aeiou':
      text_img = display_text(f'You got an {item.name}')
    else:
      text_img = display_text(f'You got a {item.name}')
  else:
    text_img = display_text('Your inventory is full')
  return objects, inventory, text_img, insides, outsides, progress


equipment = {'tree':'axe', 'chest':'key', 'farm':'scythe'}
second_state = {'tree':'stump', 'chest':'unlocked_chest', 'farm':'empty_farm'}
reward = {'tree':'wood', 'chest':'shield', 'farm':'bread'}
description = {'tree':('You need an axe to chop down this tree', 'You chopped down a tree and got wood'), 
               'chest':('The chest is locked', 'You unlocked the chest and got a shield'),
              'farm':('This wheat is ready to harvest', 'You cleared the wheat and made bread')}

#interacting with challenge items and exchanging items in inventory
def challenge(item, inventory, inventory_spot, insides, outsides, objects, sprites, block_size, sprite_names, progress, increment):
  has_tool = False
  text_img = display_text(description[item.name][0])
  for thing in inventory:
    if thing.name == equipment[item.name]:
      has_tool = True
      tool = thing
      inventory_spot -=1
      break
  if has_tool:
    inventory.remove(tool)
    objects.remove(tool)
    objects.remove(item)
    new = make_sprite(second_state[item.name], sprites, block_size)
    objects.add(new)
    if item in insides:
      insides.remove(item)
      insides.add(new)
    elif item in outsides:
      outsides.remove(item)
      outsides.add(new)
    sprite_names.remove(item.name)
    sprite_names.append(new.name)
    sprite_names.append(reward[item.name])
    prize = make_sprite(reward[item.name], sprites, block_size)
    inventory.add(prize)
    text_img = display_text(description[item.name][1])
    progress += increment
  return inventory, insides, outsides, objects, sprite_names, text_img, progress