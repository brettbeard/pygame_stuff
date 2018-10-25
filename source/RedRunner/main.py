"""
    Red Runner main
"""

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SKY_BLUE = (135, 206, 235)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(WHITE)

        # Return the image
        return image


class Player(pygame.sprite.Sprite):
    def __init__(self):
        
        super(Player, self).__init__()

        self.change_x = 0
        self.change_y = 0

        self.idle_frames_r = []
        self.idle_frames_l = []
        self.running_frames_r = []
        self.running_frames_r = []
        self.jumping_frames_r = []
        self.jumping_frames_r = []

        sprite_sheet = SpriteSheet("player_idle.png")
        for loopCount in range(12):
            frame = sprite_sheet.get_image((loopCount * 81) + 24, 24, 81, 81)
            self.idle_frames_r.append(frame)
            flipped = pygame.transform.flip(frame, True, False)
            self.idle_frames_l.append(flipped)

        sprite_sheet = SpriteSheet("player_run.png")
        frame = sprite_sheet.get_image(52, 34, 81, 81)
        self.running_frames_r.append(frame)

        sprite_sheet = SpriteSheet("player_jump.png")
        frame = sprite_sheet.get_image(28, 20, 90, 90)
        self.jumping_frames_r.append(frame)
        frame = sprite_sheet.get_image(148, 20, 90, 90)
        self.jumping_frames_r.append(frame)

        self.image = self.idle_frames_r[0]

        self.rect = self.image.get_rect()

        self.counter = 0
        self.frame_number = 0

    def update(self):
        self.counter += 1
        if (self.counter % 5) == 0:
            self.frame_number += 1
            if self.frame_number >= 10:
                self.frame_number = 0

        self.calculate_gravity()

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.change_x == 0 and self.change_y == 0:
            self.image = self.idle_frames_r[self.frame_number]
        elif self.change_y < 0:
            self.image = self.jumping_frames_r[0]
        elif self.change_y > 0:
            self.image = self.jumping_frames_r[1]
        else:
            self.image = self.running_frames_r[0]

    def go_right(self):
        self.change_x = 6

    def go_left(self):
        self.change_x = -6

    def stop(self):
        self.change_x = 0

    def calculate_gravity(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        # On the ground?
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.change_y = -10


class Level(object):
    def __init__(self):
        super(Level, self).__init__()

        self.platform_list = pygame.sprite.Group()

    def update(self):
        self.platform_list.update()

    def draw(self, screen):

        screen.fill(SKY_BLUE)
        screen.blit(self.background, (0, 0))
        self.platform_list.draw(screen)


class Level_01(Level):
    def __init__(self):

        # Initialize base class
        Level.__init__(self)

        self.background = pygame.image.load("background.png").convert()


def main():
    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Red Runner")

    level = Level_01()

    player = Player()

    active_sprite_list = pygame.sprite.Group()

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
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
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                elif event.key == pygame.K_LEFT:
                    player.go_left()
                elif event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.stop()


        # --- Game logic should go here
        active_sprite_list.update()
        level.update()

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        #screen.fill(SKY_BLUE)

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

