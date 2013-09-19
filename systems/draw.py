__author__ = 'Taylan Sengul'
import pygame
import os
from graphics.text import Text


class Draw:
    @staticmethod
    def dungeon(player, screen):
        for tile in player.tiles_in_visibility_radius:
            if tile.is_explored:
                Draw.entity(tile, screen)
                if 'container' in tile.properties:
                    for each in tile.container:
                        Draw.entity(each, screen)
        screen.render_to_main()


    @staticmethod
    def entity(entity, screen):
        if entity.image:
            image_location = os.path.join('images', entity.image)
            image = pygame.image.load(image_location).convert_alpha()
            screen.surface.blit(image, entity.tile.screen_position)
        else:
            t = Text(screen=screen,
                     font='map object',
                     context=entity.icon,
                     coordinates=entity.tile.screen_position,
                     color=entity.color,
                     horizontal_align='center',
                     vertical_align='center')
            t.render()