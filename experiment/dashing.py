import pygame as pg
from pygame.math import Vector2


PLAYER_IMAGE = pg.Surface((30, 50))
PLAYER_IMAGE.fill(pg.Color('dodgerblue1'))


# Classes for the three states (dash, idle, and move).

class DashState:

    def __init__(self, velocity_x, next_state):
        self.dash_timer = .5  # The dash will last .5 seconds.
        self.velocity_x = velocity_x
        self.next_state = next_state

    def handle_event(self, player, event):
        # Can queue the Move- or IdleState as the
        # next state after the dashing.
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                self.next_state = MoveState(-4)
            elif event.key == pg.K_d:
                self.next_state = MoveState(4)
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a:
                self.next_state = IdleState()
            elif event.key == pg.K_d:
                self.next_state = IdleState()

    def update(self, player, dt):
        # Decrement the timer each frame.
        self.dash_timer -= dt
        # Update the position of the player.
        player.pos.x += self.velocity_x
        player.rect.center = player.pos

        if self.dash_timer <= 0:  # Once the timer is done...
            # switch to the queued state.
            player.state = self.next_state


class MoveState:

    def __init__(self, velocity_x):
        self.velocity_x = velocity_x

    def handle_event(self, player, event):
        # Can switch to Dash or Idle or change the direction.
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                return DashState(-8, player.state)
            elif event.key == pg.K_e:
                return DashState(8, player.state)
            elif event.key == pg.K_a:
                self.velocity_x = -4
            elif event.key == pg.K_d:
                self.velocity_x = 4
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a and self.velocity_x < 0:
                return IdleState()
            elif event.key == pg.K_d and self.velocity_x > 0:
                return IdleState()

    def update(self, player, dt):
        player.pos.x += self.velocity_x
        player.rect.center = player.pos


class IdleState:

    def handle_event(self, player, event):
        # Can switch to Move or Dash.
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                return MoveState(-4)
            elif event.key == pg.K_d:
                return MoveState(4)
            elif event.key == pg.K_q:
                return DashState(-8, player.state)
            elif event.key == pg.K_e:
                return DashState(8, player.state)

    def update(self, player, dt):
        pass


class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect(center=pos)
        self.vel = Vector2(0, 0)
        self.pos = Vector2(pos)
        # Start in the IdleState.
        self.state = IdleState()

    def handle_event(self, event):
        new_state = self.state.handle_event(self, event)
        # Check if the state's handle_event method returned a new
        # state object, if yes, assign it to self.state.
        self.state = new_state if new_state is not None else self.state

    def update(self, dt):
        # Update the current state.
        self.state.update(self, dt)


def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    player = Player((600, 300), all_sprites)
    dt = 0
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            player.handle_event(event)

        all_sprites.update(dt)

        screen.fill((30, 30, 30))
        all_sprites.draw(screen)

        pg.display.flip()
        dt = clock.tick(30) / 1000  # delta time in milliseconds.


if __name__ == '__main__':
    main()
    pg.quit()