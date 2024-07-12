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