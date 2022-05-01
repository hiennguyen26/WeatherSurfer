import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0, 255, 0)
YELLOW = (255,255,0)
BACKGROUND_COLOR = (0,0,0)

player_size = 50
player_health = 100
movement_speed = 10
player_pos = [WIDTH/2, HEIGHT-2*player_size]


#TODO: make two classes of enemies: snow vs rain vs actual blockade
enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

def set_level(score, SPEED):
	if score < 20:
		SPEED = 5
	elif score < 40:
		SPEED = 8
	elif score < 60:
		SPEED = 12
	else:
		SPEED = 15
	return SPEED
	# SPEED = score/5 + 1


def drop_enemies(enemy_list):
    #TODO: AI stuff goes here
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0,WIDTH-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])

#TODO: draw more enemies classes
def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
    #TODO: If 
		pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += SPEED
		else:
			enemy_list.pop(idx)
			score += 1
	return score

def collision_check(enemy_list, player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return True
	return False


def detect_collision(player_pos, enemy_pos):
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
			return True
	return False

#TODO: wrap in main function
while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	

	keys = pygame.key.get_pressed() #checking if key is pressed

	x = player_pos[0]
	y = player_pos[1]

	if keys[pygame.K_LEFT]: 
		x -= movement_speed
	elif keys[pygame.K_RIGHT]:
		x += movement_speed

	player_pos = [x,y]

	
		
	screen.fill(BACKGROUND_COLOR)

	drop_enemies(enemy_list)
	score = update_enemy_positions(enemy_list, score)
	SPEED = set_level(score, SPEED)

	text = "Score:" + str(score)
	label = myFont.render(text, 1, YELLOW)
	screen.blit(label, (WIDTH-200, HEIGHT-40))

	if collision_check(enemy_list, player_pos):
		player_health -= 5
		if player_health <= 0:
			game_over = True
			break

	draw_enemies(enemy_list)
	print(enemy_list)
	#player
	pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

	#healthbar
	pygame.draw.rect(screen, RED, (player_pos[0] - player_size / 2, player_pos[1] - 15, 100, 7))
	pygame.draw.rect(screen, GREEN, (player_pos[0] - player_size / 2, player_pos[1] - 15, player_health, 7))


	clock.tick(30)

	pygame.display.update()
