"""# causurum.environments.grid_world.squares.PortalExit

Define portal exit square properties and functions.
"""

__all__ = ["PortalExit"]

from environments.grid_world.squares.__base__   import Square

class PortalExit(Square):
    """# Grid World Portal Exit Square.

    Representation of Grid World portal exit square.
    """
    
    def __init__(self,
        coordinate: tuple[int],
        **kwargs
    ):
        """# Instantiate Grid World Portal Exit Square.

        ## Args:
            * coordinate    (tuple[int]):       Row, column coordinate at which portal exit is 
                                                located within grid.
        """
        # Instantiate square.
        super(PortalExit, self).__init__(
            coordinate =    coordinate,
            symbol =        "[",
            terminal =      False,
            value =         0.0
        )