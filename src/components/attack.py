import pygame as pg
from settings import Settings

class AttackHandler:
    def __init__(self, game_state):
        self.game_state = game_state
        self.attack_width = 20
        self.attack_height = 10
        self.attack_length = 40
        self.attack_sprite = AttackSprite(self, pg.sprite.Group())


    def perform_attack(self):
        player = self.game_state.player
        flies = self.game_state.flies
        wasps = self.game_state.wasps
        engine_surface = self.game_state.engine.surface

        # Define the attack hitbox based on the player's direction


        if player.direction == "up":
            attack_rect = pg.Rect(player.rect.centerx - self.attack_width // 2,
                                player.rect.top - self.attack_length,
                                self.attack_width, self.attack_length)
        elif player.direction == "down":
            attack_rect = pg.Rect(player.rect.centerx - self.attack_width // 2,
                                player.rect.bottom,
                                self.attack_width, self.attack_length)
        elif player.direction == "left":
            attack_rect = pg.Rect(player.rect.left - self.attack_length,
                                player.rect.centery - self.attack_height // 2,
                                self.attack_length, self.attack_height)
        elif player.direction == "right":
            attack_rect = pg.Rect(player.rect.right,
                                player.rect.centery - self.attack_height // 2,
                                self.attack_length, self.attack_height)

        self.attack_sprite.update(attack_rect)

        # Check for collision with enemies
        for enemy in flies + wasps:
            if attack_rect.colliderect(enemy.rect):
                enemy.hurt_enemy(5)  # Apply damage
    def clear_attack_visual(self):
        """Clear the attack rectangle after the attack is complete."""
        self.attack_sprite.update()

class AttackSprite(pg.sprite.Sprite):
    def __init__(self, focus: AttackHandler, *groups):
        super().__init__(*groups)
        self.focus = focus
        self.attack_width = self.focus.attack_width  # From AttackHandler now
        self.attack_height = self.focus.attack_height
        self.visible = False
        self.image = pg.Surface([self.attack_width, self.attack_height])
        self.image.fill("red")
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()

    def update(self, attack_rect=None):
        if attack_rect:
            self.image = pg.Surface((attack_rect.width, attack_rect.height))
            self.image.fill(pg.Color('red'))  # Fill the surface with red
            self.rect = attack_rect
            self.visible = True
            self.image.set_alpha(255)
        else:
            self.visible = False  # Hide the sprite when not attacking
            self.image.set_alpha(0)
    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)
            