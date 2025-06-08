"""# causurum.environments.Environment

Define an abstract environment class from which concrete environments will inherit their standard 
structure.
"""

from abc    import ABC, abstractmethod

class Environment(ABC):
    """# Abstract Environment.
    
    Abstract agent class from which concrete agents should inherit a standard structure.
    """
    
    @property
    def action_space(self) -> any:
        """# Get Action Space.
        
        Get the action space of the environment.

        ## Returns:
            * any:  Environment's action space.
        """
        # Provide environment's action space.
        return self._action_space_
    
    @property
    def state_space(self) -> any:
        """# Get State Space.
        
        Get the state space of the environment.

        ## Returns:
            * any:  Environment's state space.
        """
        # Provide environment's state space.
        return self._state_space_
    
    @abstractmethod
    def reset(self) -> any:
        """# Reset Environment.
        
        Reset environment to its original state.

        ## Returns:
            * any:  The environments current state, after resetting.
        """
        pass
    
    @abstractmethod
    def step(self,
        action: any
    ) -> tuple[any]:
        """# Update Environment.
        
        Update environment data and state based on action submitted.

        ## Args:
            * action    (any):  Action chosen by agent interacting with environment.

        ## Returns:
            * tuple[any]:   Data indicating state of environment after action is taken.
        """
        pass