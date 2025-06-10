"""# causurum.environments.grid_world.squares.Loss

Define loss square properties and functions.
"""

__all__ = ["Loss"]

from environments.grid_world.squares.__base__   import Square

class Loss(Square):
    """# Grid World Loss Square.

    Representation of Grid World loss square.
    """
    
    def __init__(self,
        coordinate: tuple[int],
        value:      float =     -0.5,
        **kwargs
    ):
        """# Instantiate Grid World Loss Square.

        ## Args:
            * coordinate    (tuple[int]):       Row, column coordinate at which loss is located in 
                                                grid.
            * value         (float, optional):  Reward yielded upon reaching loss square. Defaults 
                                                to -0.5.
        """
        # Instantiate square.
        super(Loss, self).__init__(
            coordinate =    coordinate,
            symbol =        "L",
            terminal =      True,
            value =         value
        )