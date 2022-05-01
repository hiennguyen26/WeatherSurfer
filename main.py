# WeatherJumper
# Art from Kenney.nl
# Frozen Jam by https://opengameart.org/content/frozen-jam-seamless-loop
# Yippee by http://opengameart.org/users/snabisch

from datetime import datetime
import pygame as pg
import random
from settings import *
from sprites import *
from os import path
import pandas as pd


#loading in weather AI generated data
df = pd.DataFrame()
df_targets = pd.read_csv("./df_to_use_in_game.csv")
df['predicted'] = df_targets['predicted']
df['date'] = pd.date_range(datetime.today(), periods=len(
    df_targets['predicted'])).tolist()
df.to_csv('./test_data')


# HUD
def draw_player_health(surface, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        color = GREEN
    elif pct > 0.3:
        color = YELLOW
    else:
        color = RED
    pg.draw.rect(surface, color, fill_rect)
    pg.draw.rect(surface, WHITE, outline_rect, 2)


# main game
class Game:
    def __init__(self, df):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        self.df = df

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # load spritesheet image
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        # load clouds 
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(
                path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        self.item_images = {}
        for item in POWERUP_IMAGES:
            self.item_images[item] = pg.image.load(
                path.join(img_dir, POWERUP_IMAGES[item])).convert_alpha()

        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump33.wav'))
        self.boost_sound = pg.mixer.Sound(
            path.join(self.snd_dir, 'Boost16.wav'))
        self.health_sound = pg.mixer.Sound(
            path.join(self.snd_dir, 'health_pack.wav'))

    def new(self):
        # start a new game
        self.score = 0
        self.date = ""
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.icemobs = pg.sprite.Group()
        self.firemobs = pg.sprite.Group()
        self.windmobs = pg.sprite.Group()
        self.rainmobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        
        for plat in PLATFORM_LIST:
            Platform(self, *plat)

        # loads music
        pg.mixer.music.load(path.join(self.snd_dir, 'Frozen Jam.ogg'))
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        #set frequency of mob spawning
        counter = MOB_FREQ
        idx = 0

        self.playing = True
        while self.playing:
            eta = self.clock.tick(FPS)
            self.events()
            self.update()

            #spawning mob every set frequency
            self.draw()
            counter -= eta
            if counter < 0:
                if self.df['predicted'][idx] == 1:
                    self.date = self.df['date'][idx]
                    Mob(self)
                elif self.df['predicted'][idx] == 2:
                    self.date = self.df['date'][idx]
                    RainMob(self)
                elif self.df['predicted'][idx] == 3:
                    self.date = self.df['date'][idx]    
                    WindMob(self)
                elif self.df['predicted'][idx] == 4:
                    self.date = self.df['date'][idx]
                    IceMob(self)
                elif self.df['predicted'][idx] == 5:
                    self.date = self.df['date'][idx]   
                    FireMob(self)
                counter += MOB_FREQ
                idx += 1
        pg.mixer.music.fadeout(500) 

    def update(self):

        # Game Loop - Update
        self.all_sprites.update()

        # hit regular mob?
        mob_hits = pg.sprite.spritecollide(
            self.player, self.mobs, False, pg.sprite.collide_mask)
        for hit in mob_hits:
            self.player.health -= RG_MOB_DMG
            # end game if player health depleted
            if self.player.health <= 0:
                self.playing = False
        if mob_hits:
            self.player.pos += vec(MOB_KNOCKBACK,
                                   0).rotate(mob_hits[0].rotation)

        # hit ice mob?
        icemob_hits = pg.sprite.spritecollide(
            self.player, self.icemobs, False, pg.sprite.collide_mask)
        for hit in icemob_hits:
            self.player.health -= RG_MOB_DMG
            self.player.friction = self.player.friction * 1.5
            # end game if player health depleted
            if self.player.health <= 0:
                self.playing = False
        if icemob_hits:
            self.player.pos += vec(MOB_KNOCKBACK,
                                   0).rotate(icemob_hits[0].rotation)

        # hit fire mob?
        firemob_hits = pg.sprite.spritecollide(
            self.player, self.firemobs, False, pg.sprite.collide_mask)
        for hit in firemob_hits:
            self.player.health -= FIRE_MOB_DMG
            # end game if player health depleted
            if self.player.health <= 0:
                self.playing = False
        if firemob_hits:
            self.player.pos += vec(MOB_KNOCKBACK,
                                   0).rotate(firemob_hits[0].rotation)

        # hit wind mob?
        windmob_hits = pg.sprite.spritecollide(
            self.player, self.windmobs, False, pg.sprite.collide_mask)
        for hit in windmob_hits:
            self.player.health -= RG_MOB_DMG
            self.player.pos.x = choice([0, WIDTH])
            # end game if player health depleted
            if self.player.health <= 0:
                self.playing = False
        if windmob_hits:
            self.player.pos += vec(MOB_KNOCKBACK,
                                   0).rotate(windmob_hits[0].rotation)

        # hit rain mob?
        rainmob_hits = pg.sprite.spritecollide(
            self.player, self.rainmobs, False, pg.sprite.collide_mask)
        for hit in rainmob_hits:
            self.player.health -= RG_MOB_DMG
            self.player.friction = self.player.friction / 2
            # end game if player health depleted
            if self.player.health <= 0:
                self.playing = False
        if rainmob_hits:
            self.player.pos += vec(MOB_KNOCKBACK,
                                   0).rotate(rainmob_hits[0].rotation)

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and \
                   self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # if player reaches top 1/4 of screen, scroll layers
        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(100) < 15:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)

            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)

            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)

            for icemob in self.icemobs:
                icemob.rect.y += max(abs(self.player.vel.y), 2)

            for firemob in self.firemobs:
                firemob.rect.y += max(abs(self.player.vel.y), 2)

            for windmob in self.windmobs:
                windmob.rect.y += max(abs(self.player.vel.y), 2)

            for rainmob in self.rainmobs:
                rainmob.rect.y += max(abs(self.player.vel.y), 2)

            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    # increase score
                    self.score += 10

        # if player hits powerup
        powerup_hits = pg.sprite.spritecollide(
            self.player, self.powerups, False)
        for powerup in powerup_hits:
            # boosts players up vertically
            if powerup.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
            # increases health and resets friction of player
            if powerup.type == 'health' and self.player.health < PLAYER_HEALTH:
                self.health_sound.play()
                powerup.kill()
                self.player.add_health(HEALTH_AMOUNT)
                self.player.friction = -0.12

        # Ending game conditions
    
        # hitting bottom of screen
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep same average number
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                     random.randrange(-75, -30))

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)

        # date
        self.draw_text(str(self.date), 22, WHITE, WIDTH, 15)

        # HUD
        draw_player_health(self.screen, 10, 10,self.player.health / PLAYER_HEALTH)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump",
                       22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22,
                       WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore),
                       22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22,
                       WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22,
                       WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE,
                           WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore),
                           22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    # starts or ends game dependent on key press
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game(df=df)
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
