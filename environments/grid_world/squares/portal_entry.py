"""# causurum.environments.grid_world.squares.PortalEntry

Define portal entry square properties and functions.
"""

__all__ = ["PortalEntry"]

from typing                                     import override

from environments.grid_world.squares.__base__   import Square

class PortalEntry(Square):
    """# Grid World Portal Entry Square.

    Representation of Grid World portal entry square.
    """
    
    def __init__(self,
        coordinate: tuple[int],
        exit:       tuple[int],
        **kwargs
    ):
        """# Instantiate Grid World Portal Entry Square.

        ## Args:
            * coordinate    (tuple[int]):       Row, column coordinate at which portal entry is 
                                                located within grid.
        """
        # Instantiate square.
        super(PortalEntry, self).__init__(
            coordinate =    coordinate,
            symbol =        "]",
            terminal =      False,
            value =         0.0
        )
        
        # Initialize activation count.
        self._activations_: int =           0
        
        # Define corresponding portal exit.
        self._exit_:        tuple[int] =    exit
        
    @property
    def activations(self) -> int:
        """# Get Activation Count.
        
        Provide the count of portal activations for this entrace.

        ## Returns:
            * int:  Portal entrance activation count.
        """
        return self._activations_
        
    @property
    def exit(self) -> tuple[int]:
        """# Get Exit Coordinate.
        
        Provide coordinate of portal's cooresponding exit.

        ## Returns:
            * tuple[int]:   Exit coordinate.
        """
        return self._exit_
    
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
        self._activations_ += 1
        
        # Provide step data.
        return  (
                    self._exit_,
                    self.value,
                    self.terminal,
                    {
                        "activations":  self._activations_
                    }
                )