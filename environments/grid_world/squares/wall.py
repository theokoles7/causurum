"""# causurum.environments.grid_world.squares.Wall

Define wall square properties and functions.
"""

__all__ = ["Wall"]

from typing                                     import override

from environments.grid_world.squares.__base__   import Square

class Wall(Square):
    """# Grid World Wall Square.
    
    Representation of Grid World wall square.
    """
    
    def __init__(self,
        coordinate: tuple[int],
        value:      float =     -0.1,
        **kwargs
    ):
        """# Instantiate Grid World Wall Square.

        ## Args:
            * coordinate    (tuple[int]):       Row, column coordinate at which wall is located in 
                                                grid.
            * value         (float, optional):  Penalty incurred from colliding with wall. Defaults 
                                                to -0.1.
        """
        # Instantiate square.
        super(Wall, self).__init__(
            coordinate =    coordinate,
            symbol =        "X",
            terminal =      False,
            value =         value
        )
        
        # Initialize collision count.
        self._collisions_:  int =   0
        
    @property
    def collisions(self) -> int:
        """# Get Collision Count.
        
        Provide the number of times the wall has been collided with by agent.

        ## Returns:
            * int:  Collision count.
        """
        return self._collisions_
    
    @override
    def reset(self) -> None:
        """# Reset Square.

        Reset count of collisions for square.
        """
        self._collisions_:  int =   0
    
    @override
    def trigger(self,
        agent_origin:   tuple[int]
    ) -> tuple[tuple[int], float, bool, dict]:
        """# Trigger Square.

        ## Args:
            * agent_origin  (tuple[int]):   Position from which agent is entering square.

        ## Returns:
            * tuple[tuple[int], float, bool, dict]:
                * Agent's new position.
                * Reward yielded/penalty incurred.
                * True if square is terminal, False otherwise.
                * Metadata related to transition.
        """
        # Increment visit count.
        self._collisions_ += 1
        
        # Provide step data.
        return  (
                    agent_origin,
                    self.value,
                    self.terminal,
                    {
                        "collisions":  self._collisions_ 
                    }
                )