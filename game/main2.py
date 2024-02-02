import time
import pygame
import math
from blast_game.game.fire import make_List

# Initialize pygame
pygame.init()


class Player:

    def __init__(self, x, y, screen):
        self.images = {
            'default': pygame.transform.scale(pygame.image.load('../assets/space-invaders.png'), (120, 100)),
            'left': pygame.transform.scale(pygame.image.load('../assets/space-invaders-left.png'), (120, 100)),
            'right': pygame.transform.scale(pygame.image.load('../assets/space-invaders-right.png'), (120, 100)),
            'down': pygame.transform.scale(pygame.image.load('../assets/space-invaders-down.png'), (120, 100))
        }
        self.b_images = {
            'default': pygame.transform.scale(pygame.image.load('../assets/bullet.png'), (50, 40)),
            'left': pygame.transform.scale(pygame.image.load('../assets/bullet.left.png'), (50, 40)),
            'right': pygame.transform.scale(pygame.image.load('../assets/bullet_right.png'), (50, 40)),
            'down': pygame.transform.scale(pygame.image.load('../assets/bullet_down.png'), (50, 40)),
        }
        self.screen = screen
        self.moving = False
        self.bullet_image = self.b_images['default']
        self.b_direct = None
        self.current_direct = None
        self.current_image = self.images['default']
        self.player_rect = self.current_image.get_rect()
        self.bullet_rect = self.bullet_image.get_rect()
        self.x = x
        self.y = y
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.down_pressed = False
        self.up_pressed = False
        self.speed = 0.5
        self.bullet_speed = 0.7
        self.bullets = []
        self.bullet_count = 0
        self.health = 10
        self.die = False
        self.player_explosion = pygame.transform.scale(pygame.image.load('../assets/player_explosion.png'),
                                                       (150, 150)).convert_alpha()
        self.coins_collected = 1

    def Display(self):
        if self.up_pressed:
            self.current_image = self.images['default']
            self.current_direct = 'up'
        if self.left_pressed:
            self.current_image = self.images['left']
            self.current_direct = 'left'
        if self.right_pressed:
            self.current_image = self.images['right']
            self.current_direct = 'right'
        if self.down_pressed:
            self.current_image = self.images['down']
            self.current_direct = 'down'
        self.player_rect = self.current_image.get_rect(topleft=(self.x, self.y))
        self.player_rect.inflate_ip(-20, -20)
        self.screen.blit(self.current_image, (self.x, self.y))
        if screen1.controls_for_boost_is_pressed:
            screen1.fire_boost.Update(self.x, self.y, self.current_direct, self.player_rect)

    def fire_bullets(self):
        if self.current_direct == 'up':
            self.b_direct = self.current_direct
            self.bullet_image = self.b_images['default']
        if self.current_direct == 'down':
            self.b_direct = self.current_direct
            self.bullet_image = self.b_images['down']
        if self.current_direct == 'left':
            self.b_direct = self.current_direct
            self.bullet_image = self.b_images['left']
        if self.current_direct == 'right':
            self.b_direct = self.current_direct
            self.bullet_image = self.b_images['right']
        self.bullet_rect = self.bullet_image.get_rect(topleft=(self.x, self.y))
        self.bullet_rect.inflate_ip(-20, -20)
        bullet = {
            'x': self.x,
            'y': self.y,
            'image': self.bullet_image,
            'direct': self.b_direct,
            'rect': self.bullet_rect
        }
        self.bullets.append(bullet)

    def update_bullets(self):
        for bullet in self.bullets[:]:
            if bullet['direct'] == 'up':
                bullet['y'] -= self.bullet_speed
            if bullet['direct'] == 'down':
                bullet['y'] += self.bullet_speed
            if bullet['direct'] == 'left':
                bullet['x'] -= self.bullet_speed
            if bullet['direct'] == 'right':
                bullet['x'] += self.bullet_speed
            bullet['rect'].topleft = (bullet['x'], bullet['y'])
            self.screen.blit(bullet['image'], (bullet['x'], bullet['y']))
            if (bullet['x'] < 0 or bullet['x'] > 750 or bullet['y'] < 0 or bullet['y'] > 550):
                self.bullets.remove(bullet)
                screen1.exp.Put_explosions(bullet['x'], bullet['y'], 'bullet')
            if bullet['rect'].colliderect(screen1.enemy1.enemy_rect):
                screen1.exp.Put_explosions(bullet['x'], bullet['y'], 'bullet')
                screen1.rect.count -= 1
                screen1.enemy1.health -= 1
                screen1.rect.Update("Decreasing", 30)
                if screen1.rect.count == 0:
                    screen1.enemy1.Die()
                self.bullets.remove(bullet)
                self.bullet_count += 1

    def Move(self):
        self.velX = 0
        self.velY = 0
        if screen1.controls_for_boost_is_pressed:
            self.speed = 2
        else:
            self.speed = 0.5
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
        self.x += self.velX
        self.y += self.velY

    def Die(self):
        text, rect = screen1.text("YOU LOST", 75, 'center', '#008000', 'game', (400, 300))
        transparency = 255
        self.die = True
        start_ticks = pygame.time.get_ticks()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            transparency -= 5
            self.player_explosion.set_alpha(transparency)
            if transparency > 100:
                screen1.player1.Display()
            if screen1.enemy1.x > 690:
                screen1.enemy1.xix = False
            if screen1.enemy1.x < 0:
                screen1.enemy1.xix = True
            if screen1.enemy1.y < 0:
                screen1.enemy1.yix = True
            if screen1.enemy1.y > 490:
                screen1.enemy1.yix = False

            seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            if seconds < 3:
                time.sleep(0.02)
            self.screen.blit(screen1.reseized, (0, 0))
            screen1.enemy1.Move()
            screen1.enemy1.Display()
            if seconds > 3:
                screen1.screen.blit(text, rect)
            if seconds > 5:
                screen1.Waiting()
            self.screen.blit(self.player_explosion, (self.x, self.y))
            pygame.display.update()


class Enemy(Player):
    def __init__(self, x, y, screen, list):
        super().__init__(
            x, y , screen
        )
        self.list = list
        self.image = pygame.transform.scale(pygame.image.load("../assets/ufo.png"), (120, 100))
        self.image2 = pygame.transform.scale(pygame.image.load("../assets/enemy2.png"), (120, 100))
        self.speedY = 0.5
        self.speedX = 0.3
        self.xix = True
        self.yix = True
        self.enemy_rect = self.image.get_rect()
        self.health = 10
        self.wings = {
            'right': pygame.transform.scale(pygame.image.load('../assets/lines_right.png'), (50, 50)),
            'left': pygame.transform.scale(pygame.image.load('../assets/lines_left.png'), (50, 50)),
        }
        self.wing_x = 0
        self.wing_y = 0
        self.current_wing = self.wings['right']
        self.current_wing_rect = self.current_wing.get_rect(topleft=(self.wing_x, self.wing_y))
        self.open_wings = False
        self.default_movement = True
        self.circle_start = False
        self.circling = False
        self.bullet_image1 = pygame.transform.scale(pygame.image.load('../assets/bomb.png'), (65, 65))
        self._array_bullets = []
        self.direct = None
        self.bullet_rect = None
        self.bullet_speed = 1
        self.target_x = 320
        self.target_y = 240
        self.get_defensive = False
        self.mas_bullet_fire = 2


    def Move(self):
        self.velX = 0
        self.velY = 0
        if self.health == 3 and not self.get_defensive:
            self.default_movement = False
            self.get_defensive = True
            screen1.movements.circle_r = 60
        if self.health ==5:
            self.default_movement = True
            self.circling = False
            self.speedX = 0.5
            self.speed = 0.7
        if self.default_movement:
            self.velX, self.velY = screen1.movements.Regular_Movement(self.speedX, self.speedY, self.velX, self.velY,self.xix, self.yix)
        if (self.health == 8 or self.get_defensive) and not self.circle_start and not self.circling:
            self.default_movement = False
            self.circle_start = True
        if self.circle_start:
            self.velX,self.velY = screen1.movements.Circle_start(last_pos=(self.x,self.y),velX=self.velX,velY=self.velY,speedX=self.speedX,speedY=self.speedY)
            if self.velX is None and self.velY is None:
                self.circle_start = False
                self.circling = True
        if self.circling:
            self.velX, self.velY = screen1.movements.Circling()
            self.velX,self.velY = self.velX - self.x,self.velY - self.y
        self.x += self.velX
        self.y += self.velY
        self.enemy_rect = self.image.get_rect(topleft=(self.x, self.y))
        self.enemy_rect.inflate_ip(-20, -20)

    def Display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def Get_wings(self):
        if self.open_wings:
            if self.xix and self.yix:
                self.current_wing = self.wings['left']
                self.wing_x, self.wing_y = self.enemy_rect.topleft
                self.wing_x -= 50
                self.wing_y -= 50
            elif not self.xix and self.yix:
                self.current_wing = self.wings['right']
                self.wing_x, self.wing_y = self.enemy_rect.topright
                self.wing_x -= 24
                self.wing_y -= 50
            elif not self.xix and not self.yix:
                self.current_wing = self.wings['left']
                self.wing_x, self.wing_y = self.enemy_rect.bottomright
            elif self.xix and not self.yix:
                self.current_wing = self.wings['right']
                self.wing_x, self.wing_y = self.enemy_rect.bottomleft
                self.wing_x += 20
                self.wing_y += 20
            self.current_wing_rect = self.current_wing.get_rect(topleft=(self.wing_x, self.wing_y))
            self.screen.blit(self.current_wing, self.current_wing_rect)

    def Die(self):
        self.die = True
        text, rect = screen1.text("YOU WIN", 75, 'center', '#FFA500', 'game', (400, 300))
        transparency = 255
        start_ticks = pygame.time.get_ticks()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if screen1.player1.x > 690:
                screen1.player1.x = 690
            if screen1.player1.x < 0:
                screen1.player1.x = 0
            if screen1.player1.y < 0:
                screen1.player1.y = 0
            if screen1.player1.y > 490:
                screen1.player1.y = 490
            transparency -= 5
            self.player_explosion.set_alpha(transparency)
            seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            if seconds < 3:
                time.sleep(0.02)
            self.screen.blit(screen1.reseized, (0, 0))
            if seconds > 3:
                screen1.screen.blit(text, rect)
            if seconds > 5:
                screen1.Waiting()
            screen1.player1.Display()
            screen1.player1.Move()
            screen1.screen.blit(self.player_explosion, (self.x, self.y))
            pygame.display.update()

    def bullet_fire(self, x=0,y=0):
        if self.get_defensive:
            for x,y in self.list:
                self.target_x = x
                self.target_y = y
                dir_x = self.target_x - self.x
                dir_y = self.target_y - self.y
                magnitude = math.sqrt(dir_x ** 2 + dir_y ** 2)
                if magnitude != 0:
                    dir_x /= magnitude
                    dir_y /= magnitude
                self.direct = (dir_x, dir_y)
                self.bullet_rect = self.bullet_image1.get_rect(topleft=(self.x, self.y))
                bullet = {
                    "x": self.x,
                    "y": self.y,
                    "image": self.bullet_image1,
                    "rect": self.bullet_rect,
                    "direct": self.direct
                }
                self._array_bullets.append(bullet)
            if self.mas_bullet_fire == 2:
                self.get_defensive = False
                screen1.movements.circle_r = 250
            self.mas_bullet_fire +=1
        else:
            self.target_x = x
            self.target_y = y
            dir_x = self.target_x - self.x
            dir_y = self.target_y - self.y
            magnitude = math.sqrt(dir_x ** 2 + dir_y ** 2)
            if magnitude != 0:
                dir_x /= magnitude
                dir_y /= magnitude
            self.direct = (dir_x, dir_y)
            self.bullet_rect = self.bullet_image1.get_rect(topleft=(self.x, self.y))
            bullet = {
                "x": self.x,
                "y": self.y,
                "image": self.bullet_image1,
                "rect": self.bullet_rect,
                "direct": self.direct
            }
            self._array_bullets.append(bullet)


    def bullet_update(self):
        for bullet in self._array_bullets[:]:
            bullet['x'] += self.bullet_speed * bullet['direct'][0]
            bullet['y'] += self.bullet_speed * bullet['direct'][1]
            bullet['rect'].topleft = (bullet['x'], bullet['y'])
            if bullet['rect'].colliderect(screen1.player1.player_rect):
                self._array_bullets.remove(bullet)
                screen1.exp.Put_explosions(bullet['x'], bullet['y'], 'bullet')
                screen1.rect2.count -=1
                screen1.rect2.Update("Decreasing", 30)
                if screen1.rect2.count == 0:
                    screen1.player1.Die()
            if (bullet['x'] < 0 or bullet['x'] > 750 or bullet['y'] < 0 or bullet['y'] > 550):
                self._array_bullets.remove(bullet)
                screen1.exp.Put_explosions(bullet['x'], bullet['y'], 'bullet')
            screen1.screen.blit(bullet['image'], (bullet['x'], bullet['y']))


class moving_patterns:
    def __init__(self, screen):
        self.circle_r = 250   # 250
        self.center = (320, 240)
        self.speed = 0.005
        self.velX = 0
        self.velY = 0
        self.angle = 0
        self.screen = screen
    def Regular_Movement(self, speedX, speedY, velX, velY, xix, yix):
        if xix and yix:
            velX = speedX
            velY = speedY
        elif not xix and yix:
            velX = -speedX
            velY = speedY
        elif not xix and not yix:
            velX = -speedX
            velY = -speedY
        elif xix and not yix:
            velX = speedX
            velY = -speedY
        return (velX, velY)
    def Circle_start(self,last_pos, velX, velY, speedX, speedY):
        target_pos_x = self.center[0] + self.circle_r * math.cos(self.angle)
        target_pos_y = self.center[1] + self.circle_r * math.sin(self.angle)
        x = last_pos[0]
        y = last_pos[1]
        if target_pos_x > x:
            velX = speedX
        if target_pos_x < x:
            velX = -speedX
        if target_pos_y > y:
            velY = speedY
        if target_pos_y < y:
            velY = -speedY
        if math.floor(target_pos_y) == math.floor(y) and math.floor(target_pos_x) == math.floor(x):
            return (None,None)
        else:
            return (velX, velY)
    def Circling(self):
        self.angle += self.speed
        self.velX = self.center[0] + int(self.circle_r * math.cos(self.angle))
        self.velY =self.center[1] + int(self.circle_r * math.sin(self.angle))
        return (self.velX,self.velY)



class health_rectangle:
    def __init__(self, color, x, y, width, height, object_text, text_color, rect_state, text_size,screen, rotation=None):
        self.color = color
        self.object_text = object_text
        self.x = x
        self.y = y
        self.text_size = text_size
        self.rotation = rotation
        self.rect_state = rect_state
        self.width = width
        self.height = height
        self.is_full = False
        self.screen = screen
        if rect_state == "Increasing":
            self.outline_width = width
            self.outline_height = height
            if rotation:
                self.height = 0
            else:
                self.width = 0
        else:
            self.width = width
            self.height = height
            self.outline_width = self.width
            self.outline_height = self.height
        self.count = 10
        self.font = pygame.font.SysFont(None, self.text_size)
        self.text_color = text_color
        self.text = self.font.render(f"{self.object_text}", True, self.text_color)
        if rotation:
            self.text = pygame.transform.rotate(self.text, 90)
            self.text_rect = self.text.get_rect(center=(self.x + self.width / 2, self.y + self.outline_height / 2))
        else:
            self.text_rect = self.text.get_rect(center=(self.x + self.outline_width / 2, self.y + self.height / 2))
        self.outline_tickness = 3

    def Display(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (
            self.x - self.outline_tickness, self.y - self.outline_tickness,
            self.outline_width + 2 * self.outline_tickness,
            self.outline_height + 2 * self.outline_tickness))
        pygame.draw.rect(screen1.screen, self.color, (self.x, self.y, self.width, self.height))
        self.screen.blit(self.text, self.text_rect)

    def Update(self, direct, speed):
        if direct == "Decreasing":
            self.width -= speed
        else:
            if self.rotation:
                self.height += speed
            else:
                self.width += speed


class Explosion:
    def __init__(self, screen):
        self.image = pygame.transform.scale(pygame.image.load("../assets/explosion.png"), (50, 50))
        self.second_image = pygame.transform.scale(pygame.image.load("../assets/explosion2.png"), (80, 80))
        self.explosions = []
        self.screen = screen

    def Put_explosions(self, x, y, type):
        explosion = {
            'x': x,
            'y': y,
            'duration': 200,
            'type': type
        }
        self.explosions.append(explosion)

    def Display_player(self):
        for explosion in self.explosions[:]:
            if explosion['type'] == "player":
                screen1.screen.blit(self.second_image, (explosion['x'], explosion['y']))
            else:
                self.screen.blit(self.image, (explosion['x'], explosion['y']))
            explosion['duration'] -= 1
            if explosion['duration'] == 0:
                self.explosions.remove(explosion)


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color,screen, rect1=None):
        self.rect1 = rect1
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.flag = False
        self.screen = screen
        if self.image is None:
            self.image = self.text
            self.flag = True
            self.rect = self.image.get_rect(center=(self.x, self.y))
        else:
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.text_rect = self.text.get_rect(center=(self.x, self.y))
        if self.flag:
            self.rect = self.rect.inflate(10, 10)
            self.text_rect = self.rect

    def update(self, screen):
        if self.image is not None:
            self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Player_Fire:
    def __init__(self,screen):
        self.x = 0
        self.y = 0
        self.images = {
            'up': pygame.transform.scale(pygame.image.load("../assets/player_exhasut/rocket_exhasut.png"), (90, 90)).convert_alpha(),
            'right': pygame.transform.scale(pygame.image.load(
                "../assets/player_exhasut/rocket_exhasut_right.png"), (90, 90)).convert_alpha(),
            'left': pygame.transform.scale(pygame.image.load(
                "../assets/player_exhasut/rocket_exhasut_left.png"), (90, 90)).convert_alpha(),
            'down': pygame.transform.scale(pygame.image.load(
                "../assets/player_exhasut/rocket_exhasut_down.png"), (90, 90)).convert_alpha(),
            'up_flipped': pygame.transform.scale(pygame.image.load(
                "../assets/player_exhasut/rocket_exhasut_flipped.png"), (90, 90)).convert_alpha(),
            'right_flipped': pygame.transform.scale(
                pygame.image.load("../assets/player_exhasut/rocket_exhasut_flipped_right.png"), (90, 90)).convert_alpha(),
            'left_flipped': pygame.transform.scale(
                pygame.image.load("../assets/player_exhasut/rocket_exhasut_flipped_left.png"), (90, 90)).convert_alpha(),
            'down_flipped': pygame.transform.scale(
                pygame.image.load("../assets/player_exhasut/rocket_exhasut_flipped_down.png"), (90, 90)).convert_alpha(),
        }
        self.current_image = self.images['up']
        self.current_image_flipped = self.images['up_flipped']
        self.flip = False
        self.transparency_default = 255
        self.transparency_flippped = 0
        self.screen = screen

    def Display(self):
        self.screen.blit(self.current_image, (self.x, self.y))
        self.screen.blit(self.current_image_flipped, (self.x,self.y))

    def Update(self, x, y, direct, rect):
        if direct == "up":
            self.current_image = self.images['down']
            self.current_image_flipped = self.images['down_flipped']
            self.x = rect.centerx - 50
            self.y = rect.bottom + 9
        if direct == "right":
            self.current_image = self.images['left']
            self.current_image_flipped  = self.images['left_flipped']
            self.y = rect.centery - 50
            self.x = rect.left - 100
        if direct == "left":
            self.current_image = self.images['right']
            self.current_image_flipped  = self.images['right_flipped']
            self.y = rect.centery - 45
            self.x = rect.right + 12
        if direct == "down":
            self.current_image = self.images['up']
            self.current_image_flipped  = self.images['up_flipped']
            self.x = rect.centerx - 40
            self.y = rect.top - 105
        self.current_image_flipped.set_alpha(self.transparency_flippped)
        self.current_image.set_alpha(self.transparency_default)
        if not self.flip:
            self.transparency_flippped += 0.6
            self.transparency_default -= 0.6
        if self.transparency_default <=0 or self.transparency_default >255:
            self.flip = not self.flip
        if self.flip:
            self.transparency_flippped -= 0.6
            self.transparency_default += 0.6



class Coins_Collect:
    def __init__(self, x, y,type, image,screen):
        self.x = x
        self.y = y
        self.type = type
        self.coins = []
        self.image = image
        self.speed = 0.5
        self.go = False
        self.screen = screen

    def Display(self):
        for coin in self.coins[:]:
            self.Move(coin)
            self.screen.blit(self.image, (coin['x'], coin['y']))
            if self.Remove_Coins(coin):
                self.coins.remove(coin)

    def Add_coins(self, quantity, to_x):
        for i in range(quantity):
            coin = {
                'y': self.y,
                'x': self.x +to_x,
                'rect': pygame.Rect(self.x + to_x, self.y, 50, 50)
            }
            self.coins.append(coin)
            to_x += 150

    def Remove_Coins(self, coin):
        if self.type != "health":
            if screen1.player1.player_rect.colliderect(coin['rect']):
                screen1.player1.coins_collected += 1
                if screen1.player1.coins_collected % 40 == 0:
                    screen1.enemy1.speedX += 0.2
                    screen1.enemy1.speedY += 0.2
                    screen1.enemy1.open_wings = True
                if screen1.coin_count.width <= 138:
                    screen1.coin_count.Update("Increasing", 1.5)
                return True
            if coin['x'] < 0:
                return True
            else:
                return False
        else:
            if screen1.player1.player_rect.colliderect(coin['rect']):
                if screen1.rect2.width != 300:
                    screen1.rect2.count += 1
                    screen1.rect2.Update("Increasing", 30)
                return True
            if coin['x'] < 0:
                return True
            else:
                return False


    def Move(self, coin):
        coin['x'] -= self.speed
        coin['rect'].topleft = (coin['x'], coin['y'])

# class Coin_Patterns:

class Screens:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # Stages
        self.rect = health_rectangle((255, 0, 0), 0, 5, 300, 20,
                                     'ENEMY', (255, 255, 255), rect_state="Decreasing", text_size=20,screen=self.screen)
        self.rect2 = health_rectangle((0, 255, 0), 499, 5, 300, 20,
                                      'YOU', (255, 255, 255), rect_state="Decreasing", text_size=20,screen=self.screen)
        self.boost = health_rectangle((0, 0, 255), 630, 40, 170, 20, "BOOST",
                                      (255, 255, 255), rect_state="Increasing", text_size=20,screen=self.screen)
        self.coin_count = health_rectangle((255, 255, 0), 330, 5, 140, 50, "COINS",
                                           (255, 255, 255), rect_state="Increasing", text_size=20,screen=self.screen)
        # Explosions
        self.exp = Explosion(screen=self.screen)
        # create the screen
        self.icon = pygame.image.load('../assets/ufo.png')
        # Player
        self.player1 = Player(370, 480,screen=self.screen)
        # Enemy
        self.enemy1 = Enemy(370, 5,screen=self.screen,list=make_List())
        self.icon = pygame.image.load('../assets/ufo.png')
        # Background
        self.background = pygame.image.load("../assets/42827.jpg")
        self.reseized = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.BG = pygame.image.load('../assets/Background.png')
        self.main = True
        self.overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        # Player Fire boost
        self.fire_boost = Player_Fire(screen=self.screen)
        self.controls_for_boost_is_pressed = False
        self.up_down = "Increasing"
        self.speed_for_boost = 17
        # Coins
        self.coin_image = pygame.transform.scale(pygame.image.load('../assets/coins.png'), (50, 50))
        self.coins_first_row = Coins_Collect(800, 100, "coin", image=self.coin_image,screen=self.screen)
        self.coins_second_row = Coins_Collect(800, 300,"coin", image=self.coin_image, screen=self.screen)
        self.coins_third_row = Coins_Collect(800, 500,"coin", image=self.coin_image, screen=self.screen)
        # Health
        self.health_image = pygame.transform.scale(pygame.image.load('../assets/health-care.png'), (50, 50))
        self.health_first_row = Coins_Collect(800, 100, "health", image=self.health_image, screen=self.screen)
        self.health_second_row = Coins_Collect(800, 300, "health", image=self.health_image, screen=self.screen)
        self.health_third_row = Coins_Collect(800, 500, "health", image=self.health_image, screen=self.screen)
        # Enemy Movements
        self.movements = moving_patterns(screen=self.screen)

    @staticmethod
    def get_font(size, type, bold=False, italic=False):
        if type == "game":
            return pygame.font.Font("../assets/font.ttf", size)
        else:
            return pygame.font.SysFont(type, size, bold=bold, italic=italic)

    def Play(self):
        pygame.display.set_caption("Space Invaders")
        pygame.display.set_icon(self.icon)
        # Game Loop
        collision_occured = True
        running = True
        start_ticks = pygame.time.get_ticks()
        text, rect = screen1.text("FULL BOOST", 10, 'topright', '#FF0000', 'game', (775, 70))
        controls_for_boost, c_rect = screen1.text("PRESS V", 20, 'topright', '#FFFFFF', 'Sans-serif', (660, 70))
        clock = pygame.time.Clock()
        fps = 300
        while running:
            frame_start_time = pygame.time.get_ticks()
            # RGB - red,green,blue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.Main()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player1.left_pressed = True
                    if event.key == pygame.K_RIGHT:
                        self.player1.right_pressed = True
                    if event.key == pygame.K_DOWN:
                        self.player1.down_pressed = True
                    if event.key == pygame.K_UP:
                        self.player1.up_pressed = True
                    if event.key == pygame.K_SPACE:
                        self.player1.fire_bullets()
                    if event.key == pygame.K_ESCAPE:
                        self.Waiting()
                    if event.key == pygame.K_v and screen1.boost.is_full:
                        self.controls_for_boost_is_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player1.left_pressed = False
                    if event.key == pygame.K_RIGHT:
                        self.player1.right_pressed = False
                    if event.key == pygame.K_DOWN:
                        self.player1.down_pressed = False
                    if event.key == pygame.K_UP:
                        self.player1.up_pressed = False
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds % 2 == 0 and not self.boost.is_full:
                self.boost.Update(self.up_down, self.speed_for_boost)
                self.enemy1.bullet_fire(self.player1.x,self.player1.y)
            if not self.enemy1.get_defensive:
                if seconds % 3 == 0:
                    self.coins_second_row.Add_coins(2,150)
                    self.health_second_row.Add_coins(1,450)
                    self.coins_second_row.Add_coins(2, 600)
                    screen1.enemy1.open_wings = False
                elif seconds % 4 == 0:
                    self.coins_first_row.Add_coins(2,150)
                    self.health_first_row.Add_coins(1,450)
                    self.coins_first_row.Add_coins(2, 600)
                elif seconds % 5 == 0:
                    self.coins_third_row.Add_coins(2,150)
                    self.health_third_row.Add_coins(1, 450)
                    self.coins_third_row.Add_coins(2, 600)
            if self.player1.x > 690:
                self.player1.x = 690
            if self.player1.x < 0:
                self.player1.x = 0
            if self.player1.y < 0:
                self.player1.y = 0
            if self.player1.y > 490:
                self.player1.y = 490
            #     nadolu-nadqsno = x++,y++ ,1,1
            #     nadolu-nalqvo = x--, y++ 0,1
            #     nagore-nalqvo = x--,y-- 0,0
            #     nagoee-nqdqsno = x++,y-- 1,0
            if self.enemy1.x > 690:
                self.enemy1.xix = False
            if self.enemy1.x < 0:
                self.enemy1.xix = True
            if self.enemy1.y < 0:
                self.enemy1.yix = True
            if self.enemy1.y > 490:
                self.enemy1.yix = False
            if self.enemy1.enemy_rect.colliderect(self.player1.player_rect):
                if not collision_occured:
                    self.exp.Put_explosions(self.player1.x, self.player1.y, 'player')
                    self.rect2.count -= 1
                    self.rect2.Update("Decreasing", 30)
                    if self.rect2.count == 0:
                        self.player1.Die()
                    collision_occured = True
            else:
                collision_occured = False
            # if 0<self.player1.x<600 and 0<self.player1.y<450 and self.enemy1.circling:
            self.screen.blit(self.reseized, (0, 0))
            self.player1.Display()
            self.enemy1.Display()
            self.enemy1.Move()
            self.player1.Move()
            self.player1.update_bullets()
            self.rect.Display()
            self.rect2.Display()
            self.boost.Display()
            self.exp.Display_player()
            if not self.enemy1.get_defensive:
                self.coins_second_row.Display()
                self.coins_first_row.Display()
                self.coins_third_row.Display()
                self.health_first_row.Display()
                self.health_second_row.Display()
                self.health_third_row.Display()
                self.coin_count.Display()
            self.enemy1.bullet_update()
            self.enemy1.Get_wings()
            if self.boost.width == self.boost.outline_width and not self.controls_for_boost_is_pressed:
                self.boost.is_full = True
                screen1.screen.blit(text, rect)
                screen1.screen.blit(controls_for_boost, c_rect)
            if self.controls_for_boost_is_pressed:
                self.fire_boost.Display()
                self.boost.is_full = False
                self.up_down = "Decreasing"
                self.speed_for_boost = 34
                if self.boost.width <= 0:
                    self.controls_for_boost_is_pressed = False
                    self.up_down = "Increasing"
                    self.speed_for_boost = 17
            pygame.display.update()
            frame_duration = pygame.time.get_ticks() - frame_start_time
            if frame_duration > 0:
                current_fps = 1000 // frame_duration
                if current_fps < fps - 5:
                    fps = max(30, fps -5)
                elif current_fps > fps + 5:
                    fps +=5
            clock.tick(fps)

    def Main(self):
        pygame.display.set_caption("Menu")
        while True:
            self.screen.blit(self.BG, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = self.get_font(80, 'game').render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

            PLAY_BUTTON = Button(image=pygame.image.load('../assets/Play Rect.png'), pos=(400, 250),
                                 text_input="PLAY", font=self.get_font(50, 'game'), base_color="blue",
                                 hovering_color="White", screen=self.screen)
            OPTIONS_BUTTON = Button(image=pygame.image.load('../assets/Options Rect.png'), pos=(400, 385),
                                    text_input="OPTIONS", font=self.get_font(50, 'game'), base_color="blue",
                                    hovering_color="White", screen=self.screen)
            QUIT_BUTTON = Button(image=pygame.image.load('../assets/Quit Rect.png'), pos=(400, 520),
                                 text_input="QUIT", font=self.get_font(50, 'game'), base_color="blue",
                                 hovering_color="White", screen=self.screen)

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.Play()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
            pygame.display.update()

    def Waiting(self, loser=None):
        pygame.display.set_caption("WAITING FOR RESPONSE")
        whole_surface = pygame.draw.rect(self.overlay, (128, 128, 128, 10), (0, 0, 800, 600))
        insider = pygame.draw.rect(self.overlay, "dark grey", [220, 150, 360, 250], 0, 10)
        num = 60 if self.enemy1.die or self.player1.die else 90
        while True:
            if loser is not None:
                MENU_TEXT = self.get_font(50, 'game').render(loser, True, "#b68f40")
                MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
                self.screen.blit(MENU_TEXT, MENU_RECT)
            self.screen.blit(self.overlay, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            QUIT_BUTTON = Button(image=None, pos=(insider.x + insider.width // 2, insider.y + insider.height // 2),
                                 rect1=insider,
                                 text_input="QUIT", font=self.get_font(20, 'game'), base_color="blue",
                                 hovering_color="White",screen=self.screen)
            RESTART_BUTTON = Button(image=None,
                                    pos=(insider.x + insider.width // 2, (insider.y + insider.height // 2) + 30),
                                    rect1=insider,
                                    text_input="RESTART", font=self.get_font(20, 'game'), base_color="blue",
                                    hovering_color="White",screen=self.screen)
            CONTINUE_BUTTON = Button(image=None,
                                     pos=(insider.x + insider.width // 2, (insider.y + insider.height // 2) + 60),
                                     rect1=insider,
                                     text_input="CONTINUE", font=self.get_font(20, 'game'), base_color="blue",
                                     hovering_color="White",screen=self.screen)
            RETURN_MENU = Button(image=None,
                                 pos=(insider.x + insider.width // 2, (insider.y + insider.height // 2) + num),
                                 rect1=insider,
                                 text_input="RETURN TO MENU", font=self.get_font(20, 'game'), base_color="blue",
                                 hovering_color="White",screen=self.screen)
            list = [QUIT_BUTTON, RESTART_BUTTON, RETURN_MENU, CONTINUE_BUTTON]
            if self.player1.die or self.enemy1.die:
                list.remove(list[3])
            for button in list:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CONTINUE_BUTTON.checkForInput(
                            MENU_MOUSE_POS) and self.player1.die == False and self.enemy1.die == False:
                        self.Play()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                    if RESTART_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.Restart()
                        self.Play()
                    if RETURN_MENU.checkForInput(MENU_MOUSE_POS):
                        self.Restart()
                        self.Main()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.player1.die == False and self.enemy1.die == False:
                        self.Play()
            pygame.display.update()

    def Restart(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # Stages
        self.rect = health_rectangle((255, 0, 0), 0, 5, 300, 20,
                                     'ENEMY', (255, 255, 255), rect_state="Decreasing", text_size=20,
                                     screen=self.screen)
        self.rect2 = health_rectangle((0, 255, 0), 499, 5, 300, 20,
                                      'YOU', (255, 255, 255), rect_state="Decreasing", text_size=20, screen=self.screen)
        self.boost = health_rectangle((0, 0, 255), 630, 40, 170, 20, "BOOST",
                                      (255, 255, 255), rect_state="Increasing", text_size=20, screen=self.screen)
        self.coin_count = health_rectangle((255, 255, 0), 330, 5, 140, 50, "COINS",
                                           (255, 255, 255), rect_state="Increasing", text_size=20, screen=self.screen)
        # Explosions
        self.exp = Explosion(screen=self.screen)
        # create the screen
        self.icon = pygame.image.load('../assets/ufo.png')
        # Player
        self.player1 = Player(370, 480, screen=self.screen)
        # Enemy
        self.enemy1 = Enemy(370, 5, screen=self.screen)
        self.icon = pygame.image.load('../assets/ufo.png')
        # Background
        self.background = pygame.image.load("../assets/42827.jpg")
        self.reseized = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.BG = pygame.image.load('../assets/Background.png')
        self.main = True
        self.overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        # Player Fire boost
        self.fire_boost = Player_Fire(screen=self.screen)
        self.controls_for_boost_is_pressed = False
        self.up_down = "Increasing"
        self.speed_for_boost = 17
        # Coins
        self.coin_image = pygame.transform.scale(pygame.image.load('../assets/coins.png'), (50, 50))
        self.coins_first_row = Coins_Collect(800, 100, "coin", image=self.coin_image, screen=self.screen)
        self.coins_second_row = Coins_Collect(800, 300, "coin", image=self.coin_image, screen=self.screen)
        self.coins_third_row = Coins_Collect(800, 500, "coin", image=self.coin_image, screen=self.screen)
        # Health
        self.health_image = pygame.transform.scale(pygame.image.load('../assets/health-care.png'), (50, 50))
        self.health_first_row = Coins_Collect(800, 100, "health", image=self.health_image, screen=self.screen)
        self.health_second_row = Coins_Collect(800, 300, "health", image=self.health_image, screen=self.screen)
        self.health_third_row = Coins_Collect(800, 500, "health", image=self.health_image, screen=self.screen)
        # Enemy Movements
        self.movements = moving_patterns(screen=self.screen)

    @staticmethod
    def text(text, text_size, pos, color, type, xy):
        x, y = xy[0], xy[1]
        loser_text = screen1.get_font(text_size, type).render(text, True, color)
        if pos == 'center':
            loser_rect = loser_text.get_rect(center=(400, 300))
        elif pos == "topright":
            loser_rect = loser_text.get_rect(topright=(x, y))
        return (loser_text, loser_rect)


screen1 = Screens()
screen1.Main()
