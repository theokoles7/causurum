"""# causurum.agents.causal_tracer.CounterfactualConstructor

Define utilities to construct and evaluate contrastive counterfactuals based on stored causal 
traces.
"""

__all__ = ["CounterfactualConstructor"]

from agents.causal_tracer.buffer    import *

class CounterfactualConstructor():
    """# Counterfactual Constructor.

    Module for generating counterfactual trajectories from real environment traces by intervening at 
    a chosen step and evaluating alternate outcomes.
    """
    
    def __init__(self,
        transition_function:    callable,
        symbolic_mapper:        callable =  lambda x: ""
    ):
        """# Instantiate Counterfactual Constructor.

        ## Args:
            * transition_function   (callable):             Transition function that takes `(state, 
                                                            action)` and returns `(next_state, 
                                                            reward, done)`.
            * symbolic_mapper       (callable, optional):   Optional callable that maps an action or 
                                                            state to symbolic representation (used 
                                                            for logging).
        """
        # Define transition function.
        self._transition_function_: callable =  transition_function
        
        # Define symbolic mapper.
        self._symbolic_mapper_:     callable =  symbolic_mapper
        
    def intervene(self,
        buffer:     CausalTraceBuffer,
        index:      int,
        new_action: any
    ) -> list[TraceStep]:
        """# Perform Counterfactual Intervention.

        Construct a new counterfactual trace that starts identically up to `index`, but then 
        branches using `new_action` at `index`, replaying the trajectory with updated outcomes.

        ## Args:
            * buffer        (CausalTraceBuffer):    Original trace buffer from environment interaction.
            * index         (int):                  Step index at which intervention should occur.
            * new_action    (any):                  New action to use at intervention point.

        ## Returns:
            * list[TraceStep]:  New trace reflecting counterfactual trajectory.
        """
        # Store all steps prior to intervention index.
        new_trace:                      list[TraceStep] =   buffer.trace[:index]
        
        # Fetch state from trace at intervention point.
        state:                          any =               buffer.trace[index].state
        
        # Submit new action.
        next_state, reward, done =                          self._transition_function_(state, new_action)
        
        # Construct mapping of intervention step.
        step:                           TraceStep =         TraceStep(
                                                                state =         state,
                                                                action =        new_action,
                                                                reward =        reward,
                                                                next_state =    next_state,
                                                                done =          done,
                                                                metadata =      {},
                                                                symbol =        self._symbolic_mapper_(new_action)
                                                            )
        
        # Add step to new trace.
        new_trace.append(step)
        
        # Return new trace if new action yielded terminal state.
        if done: return new_trace
        
        # Otherise, update current state.
        current_state:                  any =               next_state
        
        # For remaining steps in buffer trace...
        for future_step in buffer.trace[index + 1:]:
            
            # Use the same action that was originally taken at this timestep.
            action:                     any =               step.action

            # Apply the original action to the *new current state* (post-intervention), simulating how the environment would evolve.
            next_state, reward, done =                  self._transition_function_(current_state, action)

            # Create a new TraceStep for this imagined transition.
            step:                       TraceStep =         TraceStep(
                                                                state =         current_state,
                                                                action =        action,
                                                                reward =        reward,
                                                                next_state =    next_state,
                                                                done =          done,
                                                                metadata =      {},
                                                                symbol =        self._symbolic_mapper_(action)
                                                            )

            # Append the generated step to the counterfactual trace.
            new_trace.append(step)

            # If the new trajectory reaches a terminal state, stop rolling forward.
            if done: break

            # Otherwise, continue simulating from the new state.
            current_state:              any =               next_state

        # Return the fully reconstructed counterfactual trace.
        return new_trace