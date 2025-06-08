"""# causurum.agents.causal_tracer.CausalTracer

Implement a utility that records environment-agent interactions and can optionally perform 
counterfactual interventions using stored trajectories.
"""

__all__ = ["CausalTracer"]

from agents.__base__                import Agent
from agents.causal_tracer.buffer    import TraceStep
from agents.causal_tracer.contrast  import CounterFactualConstructor
from agents.causal_tracer.tracer    import TraceRecorder
from environments                   import Environment


class CausalTracer(Agent):
    """# Causal Tracer.

    Collects traces of environment-agent interaction and optionally generates counterfactuals via
    stored trajectory replays.
    """
    
    def __init__(self,
        transition_function:    callable,
        symbolic_mapper:        callable =  lambda x: "",
        intervention_method:    str =       "random"
    ):
        """# Instantiate Causal Tracer Agent.
        
        ## Args:
            * transition_function   (callable): Function taking `(state, action)` and returning 
                                                `(next_state, reward, done)`.
            * symbolic_mapper       (callable): Optional mapper to get symbolic representation of 
                                                actions/states.
            * intervention_method   (str):      Sampling method for intervention point selection in 
                                                trajectory.
        """
        super().__init__()

        # Recorder manages trace collection and counterfactual reasoning.
        self._recorder_:            TraceRecorder = TraceRecorder(
                                                        transition_function =   transition_function,
                                                        symbolic_mapper =       symbolic_mapper
                                                    )

        # Method used to select intervention points in trace.
        self._intervention_method_: str =           intervention_method

        # Most recent action chosen by policy.
        self._latest_action_:       any =           None
        
    # def act(self, state: any) -> any:
    #     """# Select Action.
        
    #     Define policy to choose next action based on current state.

    #     For now, this is a placeholder (e.g., a random or hardcoded policy). In practice, this should
    #     be overridden or extended with a learned or symbolic policy.

    #     ## Args:
    #         * state (Any): Current state of environment.
        
    #     ## Returns:
    #         * Any: Chosen action.
    #     """
    #     # Placeholder: override in subclasses for learning agents.
    #     self._latest_action_ = 0  # Replace with actual policy.
    #     return self._latest_action_
    
    def observe(self,
        state:      any,
        action:     any,
        reward:     float,
        next_state: any,
        done:       bool,
        info:       dict =  {}
    ) -> None:
        """# Observe Environment Transition.
        
        Record environment step into the causal trace.

        ## Args:
            * state         (any):      State before action.
            * action        (any):      Action taken.
            * reward        (float):    Reward received.
            * next_state    (any):      Resulting state.
            * done          (bool):     Whether episode ended.
            * info          (dict):     Optional metadata from env.
        """
        # Record transition.
        self._recorder_.record(
            state =         state,
            action =        action,
            reward =        reward,
            next_state =    next_state,
            done =          done,
            metadata =      info
        )
    
    def reset(self) -> None:
        """# Reset Agent State.
        
        Clear internal trajectory and prepare for new episode.
        """
        self._recorder_.reset()
    
    def train(self) -> None:
        """# Train on Recorded Episode.
        
        Run a contrastive counterfactual reasoning step by intervening at a selected point in the 
        stored trajectory and printing or analyzing the resulting counterfactual trace.
        """
        # If there are not at least 2 steps established, simply return.
        if len(self._recorder_.trace) < 2: return

        # Define naive contrast function (e.g., flip binary action).
        def contrast(
            step: TraceStep
        ) -> any:
            if isinstance(step.action, int) and step.action in (0, 1):
                return 1 - step.action
            return step.action  # No change for non-binary actions

        counterfactual_trace = self._recorder_.sample_counterfactual(
            method = self._intervention_method_,
            new_action_function = contrast
        )

        print(f"[CausalTracerAgent] Generated counterfactual:")
        for i, step in enumerate(counterfactual_trace):
            print(f"  Step {i}: S={step.state}, A={step.symbol}, R={step.reward}, S'={step.next_state}, Done={step.done}")