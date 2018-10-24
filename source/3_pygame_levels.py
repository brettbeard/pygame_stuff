"""
 Pygame player

"""

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self):

        # Initialize base class
        super(Player, self).__init__()

        width = 40
        height = 60

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

        self.level = None

    def update(self):
        self.calculate_gravity()

        self.rect.x += self.change_x

        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for item in hit_list:
            if self.change_x > 0:
                self.rect.right = item.rect.left
            elif self.change_x < 0:
                self.rect.left = item.rect.right

        self.rect.y += self.change_y

        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for item in hit_list:
            if self.change_y > 0:
                self.rect.bottom = item.rect.top
            elif self.change_y < 0:
                self.rect.top = item.rect.bottom

            self.change_y = 0

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0

    def jump(self):
        self.change_y = -10

    def calculate_gravity(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        # On the ground?
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        # Initialize base class
        super(Platform, self).__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Level(object):
    def __init__(self):
        self.platform_list = pygame.sprite.Group()

    def update(self):
        self.platform_list.update()

    def draw(self, screen):
        screen.fill(BLUE)
        self.platform_list.draw(screen)


class Level01(Level):
    def __init__(self):

        Level.__init__(self)

        levels = [[210, 70, 500, 500],
                  [210, 70, 200, 400],
                  [210, 70, 600, 300]]

        for level in levels:
            platform = Platform(level[0], level[1])
            platform.rect.x = level[2]
            platform.rect.y = level[3]
            self.platform_list.add(platform)


def main():
    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

    # Create the player
    player = Player()

    level = Level01()

    player.level = level

    # Create the sprite group
    active_sprite_list = pygame.sprite.Group()

    player.rect.x = 100
    player.rect.y = 100

    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                elif event.key == pygame.K_RIGHT:
                    player.go_right()
                elif event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.stop()
                elif event.key == pygame.K_RIGHT:
                    player.stop()

        # --- Game logic should go here
        active_sprite_list.update()

        # Update the level
        level.update()

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        #screen.fill(WHITE)

        # --- Drawing code should go here
        level.draw(screen)
        active_sprite_list.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()


if __name__ == "__main__":
    main()

