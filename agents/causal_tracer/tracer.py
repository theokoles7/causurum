"""# causurum.agents.causal_tracer.CausalTracer

Implement a utility that records environment-agent interactions and can optionally perform 
counterfactual interventions using stored trajectories.
"""

__all__ = ["TraceRecorder"]

from agents.causal_tracer.buffer    import *
from agents.causal_tracer.contrast  import CounterFactualConstructor
from environments                   import Environment


class TraceRecorder:
    """# Tracer Recorder.

    Collects traces of environment-agent interaction and optionally generates counterfactuals via
    stored trajectory replays.
    """

    def __init__(self,
        transition_function:    callable,
        symbolic_mapper:        callable =  lambda x: ""
    ):
        """# Instantiate Causal Tracer.

        ## Args:
            * transition_function   (Callable):             Function mapping (state, action) → 
                                                            (next_state, reward, done).
            * symbolic_mapper       (Callable, optional):   Optional stringifier for symbolic 
                                                            representation of actions.
        """
        self._buffer_:                      CausalTraceBuffer =         CausalTraceBuffer()
        self._counterfactual_constructor_:  CounterFactualConstructor = CounterFactualConstructor(
                                                                            transition_function =   transition_function,
                                                                            symbolic_mapper =       symbolic_mapper
                                                                        )

    def generate_counterfactual(self,
        index:      int,
        new_action: any
    ) -> list[TraceStep]:
        """# Generate Counterfactual Trace.

        Reconstructs an alternate trajectory from a prior trace using a different action at a given
        time index.

        ## Args:
            * index         (int):  Index at which to intervene.
            * new_action    (any):  Action to substitute at the index.

        ## Returns:
            * list[TraceStep]:  Counterfactual trace.
        """
        return self._counterfactual_constructor.intervene(
            buffer =        self._buffer_,
            index =         index,
            new_action =    new_action
        )

    def sample_counterfactual(self,
        method:                 str =       "random",
        new_action_function:    callable =  lambda step: step.action
    ) -> list[TraceStep]:
        """# Sample Step.

        Choose an index using the buffer's sampling strategy and substitute a new action from a 
        user-defined generator.

        ## Args:
            * method                (str):      Sampling method. Defaults to "random".
            * new_action_function   (callable): Function to generate the new action based on the 
                                                original step.

        ## Returns:
            * list[TraceStep]:  Generated counterfactual trace.
        """
        # Sample step from buffer.
        index:          int =       self._buffer_.sample(method=method)
        
        # Reference original action from that step.
        original_step:  TraceStep = self._buffer_.trace[index]
        
        # Determine new step to take during intervention step.
        new_action:     any =       new_action_function(original_step)

        # Provide counterfactual.
        return  self.generate_counterfactual(
                    index =         index,
                    new_action =    new_action
                )

    def trace_episode(self,
        environment:    Environment,
        policy:         callable,
        max_steps:      int =       1000
    ) -> CausalTraceBuffer:
        """# Trace Episode.

        Executes an episode using a given policy and records the interaction trace.

        ## Args:
            * env        (Any):             Environment with `.reset()` and `.step()` methods.
            * policy     (callable):        Policy mapping states to actions.
            * max_steps  (int, optional):   Maximum steps per episode.

        ## Returns:
            * CausalTraceBuffer: Trace of the executed episode.
        """
        # Clear trace buffer.
        self._buffer_.clear()
        
        # Reset environment.
        state:                              any =       environment.reset()

        # For each possible step...
        for s in range(start = 1, stop = max_steps + 1):
            
            # Determine action.
            action:                         any =       policy(state)
            
            # Submit action, and record the following state, reward, and status of environment.
            next_state, reward, done, *_ =              environment.step(action)

            # Create a trace step and record it
            step:                           TraceStep = TraceStep(
                                                            state =         state,
                                                            action =        action,
                                                            reward =        reward,
                                                            next_state =    next_state,
                                                            done =          done,
                                                            metadata =      {},
                                                            symbol =        self._counterfactual_constructor._symbolic_mapper_(action)
                                                        )
            
            # Record step data in buffer.
            self._buffer_.record(step)

            # Break episode if terminal state is reached.
            if done: break

            # Update current state.
            state:                          any =       next_state

        # Provide step trace.
        return self._buffer_