"""# causurum.environments.grid_world.squares.Goal

Define goal square properties and functions.
"""

__all__ = ["Goal"]

from environments.grid_world.squares.__base__   import Square

class Goal(Square):
    """# Grid World Goal Square.

    Representation of Grid World goal square.
    """
    
    def __init__(self,
        coordinate: tuple[int],
        value:      float =     1.0,
        **kwargs
    ):
        """# Instantiate Grid World Goal Square.

        ## Args:
            * coordinate    (tuple[int]):       Row, column coordinate at which goal is located in 
                                                grid.
            * value         (float, optional):  Reward yielded upon reaching goal square. Defaults 
                                                to 1.0.
        """
        # Instantiate square.
        super(Goal, self).__init__(
            coordinate =    coordinate,
            symbol =        "W",
            terminal =      True,
            value =         value
        )