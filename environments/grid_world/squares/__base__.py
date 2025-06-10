"""# causurum.environments.grid_world.squares.Square

Define basic square properties and functions.
"""

__all__ = ["Square"]

class Square():
    """# Grid World Square.
    
    Basic representation of Grid World component.
    """
    
    def __init__(self,
        coordinate: tuple[int],
        symbol:     str =       " ",
        terminal:   bool =      False,
        value:      float =     0.0,
        **kwargs
    ):
        """# Instantiate Grid World Square.

        ## Args:
            * coordinate    (tuple[int]):       Row, column coordinate at which square is located 
                                                in grid.
            * symbol        (str, optional):    Symbol representing square in string formatting. 
                                                Defaults to blank square.
            * terminal      (bool, optional):   Indicate if square is a terminal state in the grid. 
                                                Defaults to False.
            * value         (float, optional):  Value yielded from entering square. This value is 
                                                continuous, i.e., it may be positive or negative, 
                                                with no limits. Defaults to 0.0.
        """
        # Define coordinate.
        self._coordinate_:  tuple[int] =    coordinate
        
        # Define square's symbol.
        self._symbol_:      str =           symbol
        
        # Define terminal status.
        self._terminal_:    bool =          terminal
        
        # Define value.
        self._value_:       float =         value
        
        # Initialize visit count.
        self._visited_:     int =           0
        
    def __repr__(self) -> str:
        """# Get String.
        
        Provide string representation of square.

        ## Returns:
            * str:  String symbol of square.
        """
        return self._symbol_
    
    @property
    def column(self) -> int:
        """# Get Column.
        
        Provide the column number in which the square is located.

        ## Returns:
            * int:  Square's column location.
        """
        return self.coordinate[1]
        
    @property
    def coordinate(self) -> tuple[int]:
        """# Get Coordinate.
        
        Provide coordinate of square within grid.

        ## Returns:
            * tuple[int]:   Square's row, column coordinate.
        """
        return self._coordinate_
    
    def reset(self) -> None:
        """# Reset Square.

        Reset count of visits for square.
        """
        self._visited_: int =   0
    
    @property
    def row(self) -> int:
        """# Get Row.
        
        Provide the row number in which the square is located.

        ## Returns:
            * int:  Square's row location.
        """
        return self.coordinate[0]
    
    @property
    def terminal(self) -> bool:
        """# Is Square Terminal.
        
        Indicate if square is a terminal state within grid. This will only be true for goal & loss 
        squares.

        ## Returns:
            * bool:
                * True:     Square is a terminal state.
                * False:    Square is not a terminal state.
        """
        return self._terminal_
    
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
        self._visited_ += 1
        
        # Provide step data.
        return  (
                    self.coordinate,
                    self.value,
                    self.terminal,
                    {
                        "visited":  self.visited
                    }
                )
    
    @property
    def value(self) -> float:
        """# Get Value.
        
        Provide the reward yielded/penalty incurred by entering square.

        ## Returns:
            * float:    Square's reward/penalty.
        """
        return self._value_
    
    @property
    def visited(self) -> int:
        """# Get Visit Count.
        
        Provide the number of times the square has been visited.

        ## Returns:
            * int:  Number of visits to square.
        """
        return self._visited_