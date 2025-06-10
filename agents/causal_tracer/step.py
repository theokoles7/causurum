"""# causurum.agents.causal_tracer.Step

Define data structure to hold metadata related to transitions in an environment when actions are 
submitted.
"""

__all__ = ["Step"]

class Step():
    """# Trace Step.
    
    Atomic data structure comprising CausalTraceBuffers, which stores step-by-step data related to 
    transitions in an environment during an episode.
    """
    
    def __init__(self,
        state:      any,
        action:     any,
        reward:     float,
        next_state: any,
        done:       bool,
        metadata:   dict[str, any] =    {},
        symbol:     str =               ""
    ):
        """# Instantiate Trace Step.

        ## Args:
            * state         (any):                      State of environment before action was 
                                                        submitted.
            * action        (any):                      Action submitted upon environment state.
            * reward        (float):                    Reward yielded by action.
            * next_state    (any):                      State of environment after action was 
                                                        submitted.
            * done          (bool):                     True if `next_state` is a terminal state of 
                                                        the environment.
            * metadata      (dict[str, any], optional): Metadata and information related to 
                                                        environment state.
            * symbol        (str, optional):            String representation of action submitted.
        """
        # Define step data.
        self._state_:       any =               state
        self._action_:      any =               action
        self._reward_:      float =             reward
        self._next_state_:  any =               next_state
        self._done_:        bool =              done
        self._metadata_:    dict[str, any] =    metadata
        self._symbol_:      str =               symbol
    
    @property
    def action(self) -> any:
        """# Reference Action.
        
        Provide the action taken during this step.

        ## Returns:
            * any:  Action taken during step.
        """
        return self._action_
    
    @property
    def done(self) -> bool:
        """# Reference Done Status.
        
        Indicate if step resulted in terminal state.

        ## Returns:
            * bool:
                * True:     Environment reached a terminal state after action.
                * False:    Environment did not reach a terminal state after action.
        """
        return self._done_
    
    @property
    def meta_data(self) -> dict:
        """# Reference Metadata.
        
        Provide metadata stored for step.

        ## Returns:
            * dict: Step metadata.
        """
        return self._metadata_
    
    @property
    def next_state(self) -> any:
        """# Reference Next State.
        
        Provide state in which the environment was in after the action taken.

        ## Returns:
            * any:  State in which environment was in after action submitted.
        """
        return self._next_state_
    
    @property
    def reward(self) -> float:
        """# Reference Reward.
        
        Provide the reward yielded by the submitted action during the step.

        ## Returns:
            * float:    Reward yielded from action submitted during step.
        """
        return self._reward_
        
    @property
    def state(self) -> any:
        """# Reference Initial State.
        
        Provide the state in which the environment was in prior to action being taken.

        ## Returns:
            * any:  State in which environment was in prior to action submission.
        """
        return self._state_
    
    @property
    def symbol(self) -> str:
        """# Reference Symbol.
        
        Provide string representation of action taken during step.

        ## Returns:
            * str:  String representation of action.
        """
        return self._symbol_