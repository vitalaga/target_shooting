import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from archer import Archer
from bullet import Bullet
from target import Target

pygame.mixer.pre_init(44100, -16, 1, 512)


class TargetShooting:
    """Class for managing resources and game behavior"""

    def __init__(self):
        """Initializes the game and creates game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.bg_surf = pygame.image.load("images/cobblestone-1374862_1280.jpg")
        self.bg_surf = pygame.transform.scale(self.bg_surf, self.screen.get_size())
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Target Shooting")
        # pygame.display.set_icon(pygame.image.load(""))

        self.stats = GameStats(self)

        self.archer = Archer(self)
        self.bullets = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()

        self._create_target()

        pygame.mixer.music.load("sounds/music/braveheart_02. A Gift Of A Thistle.mp3")
        pygame.mixer.music.play(-1)
        self.fire = pygame.mixer.Sound("sounds/fire.wav")
        self.hit = pygame.mixer.Sound("sounds/hit.wav")
        self.miss = pygame.mixer.Sound("sounds/miss.wav")

        # Creating a Play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Running the main game loop"""
        while True:
            self._check_event()

            if self.stats.game_active:
                self.archer.update()
                self._update_bullets()
                self._update_target()

            self._update_screen()

    def _check_event(self):
        # Tracking keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Starts a new game when the Play button is pressed"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.start_game()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_UP:
            self.archer.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.archer.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.archer.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.archer.moving_down = False

    def start_game(self):
        # Reset game statistics
        self.stats.reset_stats()
        self.stats.game_active = True

        # Target and arrow cleaning
        self.bullets.empty()
        self.targets.empty()
        self.settings.reset_target_speed()

        # Creating new targets and placing the archer in the center
        self._create_target()
        self.archer.center_archer()

        # The mouse pointer is hidden
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Creating a new bullet and including it in a bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.fire.play()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Updates positions bullets and removes old bullets"""
        # Updating bullets positions
        self.bullets.update()

        # Removing old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.bullets.remove(bullet)

        self._check_bullet_target_collisions()

    def _check_bullet_target_collisions(self):
        """Handling projectile collisions with target"""
        # Removing projectiles and zucchini involved in collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.targets, True, True)

        # Destruction of existing formations and creation of new hordes
        if not self.targets:
            self.hit.play()
            self.bullets.empty()
            self._create_target()
            self.settings.reset_target_speed()
            self.stats.reset_stats()
            self._change_direction()

    def _update_target(self):
        self._check_edges()
        self.targets.update()

        if pygame.sprite.spritecollideany(self.archer, self.targets):
            self._hero_lost()

        self._check_bullet_left()

    def _create_target(self):
        """Creating a zucchini and placing it in a row"""
        target = Target(self)
        self.targets.add(target)

    def _check_edges(self):
        for target in self.targets.sprites():
            if target.check_edges():
                self._change_direction()

    def _change_direction(self):
        self.settings.target_direction *= -1

    def _hero_lost(self):
        """Handles the collision of the zucchini with the hero"""
        if self.stats.hero_left > 0:
            # Decrease hero_left
            self.stats.hero_left -= 1
            self.miss.play()
            # Cleaning up shell and zucchini lists

            self.bullets.empty()

            # Creating a new fleet and placing the hero in the center
            # self._create_fleet()
            self.archer.center_archer()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_bullet_left(self):
        """Checks if the squash has reached the left side of the screen"""
        screen_rect = self.screen.get_rect()
        for bullet in self.bullets.sprites():
            if bullet.rect.right >= screen_rect.right:
                self._hero_lost()
                break

    def _update_screen(self):
        # The screen is redrawn every time the loop passes
        self.screen.blit(self.bg_surf, (0, 0))
        self.archer.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.targets.draw(self.screen)

        # The Play button is displayed if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Displaying the last drawn screen
        pygame.display.flip()


if __name__ == '__main__':
    # Instantiate and run the game
    ai = TargetShooting()
    ai.run_game()
