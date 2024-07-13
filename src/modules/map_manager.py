"""
How it works

let us plot each map state location onto the scene.

Base ont he location of the portal in game state we can then determine which way the player is moving relative to the
world map

for example lets say we are at base. at the center the map, we can plot the green map below it and it will know that
any portal downwards from the center is going to the center. (also must get the closet node)

You can probably do the same with a graph object but I think this is easier to see and represent
and can be turn into a world map aswell later when we want to draw ontop of these nodes


1.) pass a reference to map object in param and map_machine.current so we current position at all times

2.) if world_map.txt does not exist return an error
        worldmap.txt contain vectors of the location off states set origin center for now...()
        origin -> starting place of player in game

3.) in game state. on_collides with a portal get two things..
    1.) relative location in map state -> creates the direction vector from center and player
    2.) give direction vector to map manager and returns the cloest map state to current map_state..

4.) ta da now we can have an easy way to travel through the map linking these paths with respect to the origin
    -> add pretty designs
    -> add world map button ? or we can keep private
"""
import pygame as pg
import re



class WorldMapManager:
    def __init__(self, engine) -> None:
        self.engine = engine

        #this needs to update base on map_state..
        self.center : pg.Vector2 = pg.Vector2(self.engine.screen_width // 2, self.engine.screen_height // 2)
        self.map_loc : dict[str, pg.Vector2] = []
        self.range_length : int = 60
        self.max_teleport_threshold : int = 5 # max distance to teleport
        self.rect_collision_box : pg.rect.Rect = pg.Rect(0, 0, 60, 60)

    #create regex command to parse the data below
    # (name : str filename: str, x : int, y : int)

    #regex command here...
    # first line is origin, rest does not matter (0, 0)
    # for location in locs:
    #     pass

    def get_direction_vector(self):
        return (self.engine.player.pos - self.center).normalize()

    def get_potential_maps(self):
        distance_from_center = {}
        for map_name in self.map_loc:
            distance_from_center[map_name] = self.map_loc[map_name].distance_to(self.center)

        best_choices = dict(sorted(distance_from_center.items(), key=lambda item: item[1]))
        return best_choices
            # self.map_loc[name].distance_to(self.center)

    """
    idea
    for choices in best choices:
        if said map is in range where range is a collection of rect:
            then we can return our next mapstate -> this becomes next_state in our machine in game state
    """
    def get_next_map(self):
        direction = self.get_direction_vector()
        lerp_point = direction * self.range_length
        player_pos : pg.Vector2 = self.engine.player.pos

        potential_maps = self.get_potential_maps()

        #increment the point where the rect is located
        for i in range(self.range_length, 5):
            step_point = player_pos.lerp(lerp_point, i / self.range_length)
            self.rect_collision_box.move(step_point.x, step_point.y)

            for map_name in self.map_loc:
                map_location_vector = self.map_loc[map_name]

                #should always hit the closes map
                if self.rect_collision_box.collidepoint(map_location_vector):
                    if potential_maps[map_name] < self.max_teleport_threshold:
                        return True


    def load_locations(self):
        pass
        # with open('', 'r+') as f:
        #     locs = f.readlines
    def save_map(self):
        pass

    #if so some reason you add a scene mid game run
    def update_map_after_adding_scene_to_txt_file(self):
        return



if __name__ == "__main__":

    import unittest
    from unittest.mock import MagicMock

    class TestMapManager(unittest.TestCase):
        def setUp(self):
            self.mock_engine = MagicMock()
            self.manager = WorldMapManager(self.mock_engine)

        def test_get_direction_vector(self):
            # Mock player position and center
            self.mock_engine.player.pos = pg.Vector2(-10, -10)  # Example position
            self.manager.center = pg.Vector2(5, 5)  # Example center position
            # Call the method and assert
            direction_vector = self.manager.get_direction_vector()
            print(direction_vector)
            self.assertAlmostEqual(direction_vector.x, -0.707, delta=0.001)  # Example assertion

        def test_get_potential_maps(self):

            self.manager.center = pg.Vector2(5, 5)  # Example center position

            # Mock data for map locations
            self.manager.map_loc = {
                'map1': pg.Vector2(1, 1),
                'map2': pg.Vector2(3, 3),
                'map3': pg.Vector2(2, 2)
            }

            # Call the method and assert
            self.manager.get_potential_maps()
            # Add assertions based on expected behavior

        def test_load_locations(self):
            pass # Implement this test if load_locations method is implemented

        def test_save_map(self):
            pass# Implement this test if save_map method is implemented

        def test_update_map_after_adding_scene_to_txt_file(self):
            pass


    if __name__ == "__main__":
        unittest.main()

