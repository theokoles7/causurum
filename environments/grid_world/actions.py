"""# causurum.environments.grid_world.Actions

Define mapping and related utilities of Grid World actions.
"""

__all__ = ["Action", "Actions"]

from random import choice
from typing import Literal
    
# Define actions.
Action =  Literal[0, 1, 2, 3]

class Actions():
    """# Grid World Actions.
    
    Definitions of actions applicable to Grid World.
    """
    
    def __init__(self):
        """# Instantiate action space."""
        
        # Define action deltas.
        self._deltas_:  dict[Action, tuple[int, int]] = {
                                                            0:  "UP",
                                                            1:  "DOWN",
                                                            2:  "LEFT",
                                                            3:  "RIGHT"
                                                        }
        
        # Define action names.
        self._names_:   dict[Action, str] =             {
                                                            0:  ( 1,  0),
                                                            1:  (-1,  0),
                                                            2:  ( 0, -1),
                                                            3:  ( 0,  1)
                                                        }
        
        # Define action symbols.
        self._symbols_: dict[Action, str] =             {
                                                            0:  "↑",
                                                            1:  "↓",
                                                            2:  "←",
                                                            3:  "→"
                                                        }
        
    def delta(self,
        action: Action
    ) -> tuple[int]:
        """# Get Action Delta.

        ## Args:
            * action    (Action):   Action for which delta will be fetched.

        ## Returns:
            * tuple[int]:   Action delta.
        """
        return self._deltas_[action]
    
    def name(self,
        action: Action
    ) -> str:
        """# Get Action Name.

        ## Args:
            * action    (Action):   Action for which name will be fetched.

        ## Returns:
            * str:  Action name.
        """
        return self._names_[action]
    
    def sample(self) -> Action:
        """# Sample Actions.
        
        Provide random action.

        ## Returns:
            * Action:   Random action.
        """
        return choice(list(self.space))
    
    @property
    def size(self) -> int:
        """# Get Size.
        
        Provide the discrete size of action space.

        ## Returns:
            * int:  Action space size, i.e. number of possible actions.
        """
        return 4
        
    @property
    def space(self) -> range:
        """# Get Action Space.

        ## Returns:
            range:    Discrete action space.
        """
        return range(start = 0, stop = 4, step = 1)
    
    def symbol(self,
        action: Action
    ) -> str:
        """# Get Action Symbol.

        ## Args:
            * action    (Action):   Action for which symbol will be fetched.

        ## Returns:
            * str:  Action symbol.
        """
        return self._symbols_[action]