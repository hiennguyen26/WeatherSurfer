# game options/settings
TITLE = "Weather Jumper"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# Player properties
PLAYER_ACC = 0.5
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20
PLAYER_HEALTH = 100
PLAYER_ROT_SPEED = 200
PLAYER_LAYER = 2

# Mob properties   
RG_MOB_DMG = 20
FIRE_MOB_DMG = 50
MOB_KNOCKBACK = 25
ICE_FREEZE = -1
MOB_FREQ = 1500
MOB_LAYER = 2


# Game properties
BOOST_POWER = 60
PLATFORM_LAYER = 1
CLOUD_LAYER = 0

#Power ups
POWERUP_IMAGES = {'boost': 'boost.png', 'health': 'health.png'}
HEALTH_AMOUNT = 20
POWERUP_SPAWN_PCT = 7
POWERUP_LAYER = 2

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SKYBLUE = (68, 85, 90)
BGCOLOR = SKYBLUE
