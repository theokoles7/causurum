"""# causurum.environments.grid_world.squares.Coin

Define coin square properties and functions.
"""

__all__ = ["Coin"]

from typing                                     import override

from environments.grid_world.squares.__base__   import Square

class Coin(Square):
    """# Grid World Coin Square.

    Representation of Grid World coin square.
    """
    
    def __init__(self,
        coordinate: tuple[int],
        value:      float =     0.5,
        **kwargs
    ):
        """# Instantiate Grid World Coin Square.

        ## Args:
            * coordinate    (tuple[int]):       Row, column coordinate at which coin is located in 
                                                grid.
            * value         (float, optional):  Value yielded from entering square (collecting 
                                                coin). Defaults to 0.0.
        """
        # Instantiate square.
        super(Coin, self).__init__(
            coordinate =    coordinate,
            symbol =        "$",
            terminal =      False,
            value =         value
        )
        
        # Define coin status.
        self._collected_:   bool =  False
        
    @override
    def __repr__(self) -> str:
        """# Get String.

        ## Returns:
            * str:  String symbol of coin square.
        """
        return " " if self.collected else self._symbol_
        
    @property
    def collected(self) -> bool:
        """# Get Collected Status.
        
        Indicate if coin has been collected already.

        ## Returns:
            * bool:
                * True:     Coin has already been collected.
                * False:    Coin has not been collected yet. 
        """
        return self._collected_
       
    @collected.setter 
    def collected(self,
        collected:  bool
    ) -> None:
        """# Set Collected Status.
        
        Set coin's `collected` status.
        
        ## Args:
        * collected (bool): Coin's new collected status.
        """
        self._collected_:   bool =  collected
        
    @override
    def reset(self) -> None:
        """# Reset Coin Square.
        
        Reset count of visits for square and set collected status back to False.
        """
        # Reset visit count.
        super(Coin, self).reset()
        
        # Set collected status back to False.
        self.collected =    False
    
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
        self._visited_ +=           1
        
        # Record value prior to calling self.collected to prevent invalid state response.
        value:              float = self.value
        
        # Set collected status.
        self.collected(True)
        
        # Provide step data.
        return  (
                    self.coordinate,
                    value,
                    self.terminal,
                    {
                        "visited":  self.visited
                    }
                )
        
    @override
    @property
    def value(self) -> float:
        """# Get Value.
        
        Provide the reward yielded/penalty incurred by entering square.

        ## Returns:
            * float:    Square's reward/penalty.
        """
        return 0.0 if self.collected else self._value_