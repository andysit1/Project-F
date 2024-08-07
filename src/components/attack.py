import pygame as pg
from settings import Settings
from modules.clock import Timer



from modules.sprite_base import Moving_Sprite

class SweepAttackSprite(Moving_Sprite):
    def __init__(self, focus, *groups) -> None:
        super().__init__(focus, *groups)
        self.attack_width = 17
        self.attack_height = 45
        self.horizontal_surface = pg.Surface([self.attack_width, self.attack_height])
        self.vertical_surface = pg.Surface([self.attack_height, self.attack_width])
        self.attack_sequence = 0  # Track the current attack sequence stage
        self.attack_sprite = AttackSprite(focus, *groups)
        self.attack_timeout_timer = Timer(threshold=5) # amount of seconds before times out

    def handle_attack_input(self, groups : pg.sprite.Group):
        if self.attack_sequence == 0:
            self.perform_attack(groups)
            self.attack_sequence = 1
            self.attack_timeout_timer.reset()
            print("Performed first attack.")

        elif self.attack_sequence == 1:
            self.perform_attack(groups)
            self.attack_sequence = 2
            self.attack_timeout_timer.reset()
            print("Performed second attack.")

        elif self.attack_sequence == 2:
            self.attack_sprite.perform_smash_attack(groups)
            self.reset_sequence()


    def perform_attack(self, groups : pg.sprite.Group):
        # Check for collision with enemies
        hit_list = pg.sprite.spritecollide(self, group=groups, dokill=False)
        for enemy in hit_list:
            enemy.hurt_enemy(5)  # Apply damage

    def check_attack_timeout(self):
        if self.attack_timeout_timer.is_triggered():
            self.reset_sequence()

    def reset_sequence(self):
        self.attack_sequence = 0
        self.attack_timeout_timer.stop()
        print("Attack sequence reset.")

    def update(self, dt):
        self.attack_timeout_timer.update(dt)
        self.check_attack_timeout()
        return super().update(dt)

class AttackSprite(Moving_Sprite):
    def __init__(self, focus, *groups) -> None:
        super().__init__(focus, *groups)
        self.attack_width = 25
        self.attack_height = 7
        self.horizontal_surface = pg.Surface([self.attack_width, self.attack_height])
        self.vertical_surface = pg.Surface([self.attack_height, self.attack_width])

    def reinit_hitbox(self, width, height):
        self.horizontal_surface = pg.Surface((width, height))
        self.vertical_surface = pg.Surface((height, width))


    def perform_tongue(self, groups : pg.sprite.Group):
        # Check for collision with enemies
        hit_list = pg.sprite.spritecollide(self, group=groups, dokill=False)
        for enemy in hit_list:
            if enemy.swallowable:
                enemy.kill()

            else:
                try:
                    enemy.hurt_enemy(3)  # Apply damage
                except:
                    #um im too lazy to work around the healthbar in enemy group
                    #this just stops errors from collisions of healthbars
                    pass

    def perform_smash_attack(self, groups : pg.sprite.Group):
        hit_list = pg.sprite.spritecollide(self, group=groups, dokill=False)
        for enemy in hit_list:
            enemy.hurt_enemy(13)

    def update(self, dt):
        return super().update(dt)


class AttackHandler:
    def __init__(self, game_state):
        self.game_state = game_state
        self.attack_width = 20
        self.attack_height = 10
        self.attack_length = 40
        self.attack_rect = pg.Rect(0, 0, 0, 0)
        self.attack_sprite = AttackSprite(self, pg.sprite.Group())

    def perform_attack(self):
        player = self.game_state.player
        flies = self.game_state.flies
        wasps = self.game_state.wasps
        engine_surface = self.game_state.engine.surface

        # Define the attack hitbox based on the player's direction

        if player.direction == "up":
            self.attack_rect = pg.Rect(
                player.rect.centerx - self.attack_width // 2,
                player.rect.top - self.game_state.player.rect.height,
                self.attack_width,
                self.attack_length
            )
        elif player.direction == "down":
            self.attack_rect = pg.Rect(
                player.rect.centerx - self.attack_width // 2,
                player.rect.bottom,
                self.attack_width,
                self.attack_length
            )
        elif player.direction == "left":
            self.attack_rect = pg.Rect(
                player.rect.left - self.game_state.player.rect.width,
                player.rect.centery - self.attack_height // 2,
                self.attack_length,
                self.attack_height
            )
        elif player.direction == "right":
            self.attack_rect = pg.Rect(
                player.rect.right,
                player.rect.centery - self.attack_height // 2,
                self.attack_length,
                self.attack_height)

        self.game_state.last_attack_rect = self.attack_rect  # Save the rectangle for drawing
        self.attack_sprite.update(self.attack_rect)

        # Check for collision with enemies
        for enemy in flies + wasps:
            if self.attack_rect.colliderect(enemy.rect):
                if enemy.swallowable:
                    enemy.kill()
                else:
                    enemy.hurt_enemy(5)  # Apply damage

    def clear_attack(self):
        self.attack_rect = pg.Rect(0, 0, 0, 0)  # Reset the attack_rect to an empty rectangle
        self.attack_sprite.clear_attack_visual()
