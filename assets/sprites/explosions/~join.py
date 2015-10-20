# -*- coding: utf-8 -*-
import pygame

pygame.init()
pygame.display.set_mode((1, 1))

final = pygame.Surface((96 * 24, 96)).convert_alpha()
final.fill((0, 0, 0, 0))

for a in range(24):
	if a < 10:
		image = pygame.image.load("./expl_11_000" + str(a) + ".png").convert_alpha()
	else:
		image = pygame.image.load("./expl_11_00" + str(a) + ".png").convert_alpha()
	final.blit(image, (a * 96, 0))
	pygame.image.save(final, "expl_11.png")