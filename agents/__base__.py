"""# causurum.agents.Agent

Define an abstract agent class from which concrete agents will inherit their standard structure.
"""

from abc            import ABC

from environments   import Environment

class Agent(ABC):
    """# Abstract Agent.
    
    Abstract agent class from which concrete agents should inherit a standard structure.
    """
    
    def __init__(self,
        environment:    Environment
    ):
        """# Initialize Agent.

        ## Args:
            * environment   (Environment):  Environment with which agent will interact.
        """