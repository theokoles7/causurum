"""# causurum.agents.causal_tracer.CausalTraceBuffer

Define a buffer capable of storing/managing transition traces.
"""

__all__ = ["Buffer"]

from dataclasses                import asdict
from random                     import randint

from agents.causal_tracer.step  import Step

class Buffer():
    """# Causal Trace Buffer.
    
    Buffer that stores a complete trajectory (trace) for a single episode of agent/environment 
    interaction. Designed to enable counterfactual interventions at arbitrary points.
    """
    
    def __init__(self):
        """# Instantiate Causal Trace Buffer.
        
        Initialize buffer's empty tree.
        """
        self._trace_:   list[Step] =    []
        
    def __len__(self) -> int:
        """# Reference Buffer Length.
        
        Provide current length of buffer.

        ## Returns:
            * int:  Length of buffer.
        """
        return len(self.trace)
        
    def clear(self) -> None:
        """# Clear Buffer.
        
        Re-initialize trace buffer as empty list.
        """
        self._trace_:   list[Step] =    []
        
    def sample(self,
        method: str =   "random"
    ) -> int:
        """# Sample Trace Buffer.
        
        Sample a time index at which to perform an intervention.

        ## Args:
            * method    (str, optional):    Method by which buffer will be sampled. Defaults to 
                                            "random".

        ## Returns:
            * int:  Trace index at which to intervene.
        """
        # Assert that buffer contains at least 2 steps.
        assert len(self.trace) >= 2, f"At least 2 steps are required for sampling. Buffer length is currently {len(self.trace)}"
        
        # Match sampling strategy.
        match method:
            
            # Random
            case "random":  return randint(a = 0, b = len(self.trace) - 2)
            
            # Invalid method.
            case _:         raise ValueError(f"Invalid sampling method provided: {method}")
        
    def record(self,
        step:   Step
    ) -> None:
        """# Record Step.
        
        Record data related to environment state during transition and the action taken during the 
        transition.

        ## Args:
            * step  (Step): Step transition metadata structure.
        """
        # Append transition to trace.
        self._trace_.append(step)
        
    def to_dict(self) -> list[dict[str, any]]:
        """# Represent as Dictionary.
        
        Serialize trace into a list of dictionaries.

        ## Returns:
            * list[dict[str, any]]: JSON-serializable version of trace.
        """
        return [asdict(step) for step in self.trace]
        
    @property
    def trace(self) -> list[Step]:
        """# Reference Trace.
        
        Provide the trace stored in buffer.

        ## Returns:
            * list[Step]:   Copy of trace buffer.
        """
        return self._trace_.copy()