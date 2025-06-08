[causurum](../../README.md) / [documentation](../../documentation/README.md) / [agents](../README.md) / causal-tracer

# Causal Tracer

## Motivations:
Development of the Causal Tracer agent is in pursuit of building an agent that:

* Learns from symbolic, structured traces of its experience
* Can query counterfactuals over those traces
* Uses these counterfactuals to improve policy learning and explanation generation
* Learns/leverages a causal model that links actions to abstract effects

This forms the basis for explainable, systematic generalization via causal reasoning over symbolic RL experience.

## High-Level Framework:

```
FOR each episode:
    Interact with environment
    Record symbolic + low-level transitions (causal trace)
    At the end of the episode:
        Generate counterfactual variants of key transitions
        Evaluate consequences of these hypothetical decisions
        Optionally use outcomes to refine policy/explain choices
```

## Concepts & Mechanisms:

| Component                 | Description                                                                                                   |
|---------------------------|---------------------------------------------------------------------------------------------------------------|
| Causal Trace              | A structured log of (state, action, reward, next_state, info) tuples, with symbolic metadata                  |
| Intervention Point        | A step in the trace chosen for counterfactual modification (e.g., "What if I turned left here instead?")      |
| Counterfactual Rollout    | A re-execution of the environment from the modified point onward, using either a policy or scripted actions   |
| Delta Analysis            | A comparison between the original and counterfactual trajectories (reward, states reached, symbols acquired, etc.)    |
| Learning Signal           | Optionally, use counterfactual deltas to improve the policy via imitation, reward shaping, or self-supervised prediction  |

## Step-by-Step Algorithm:

1. Environment Interact + Trace Logging
    * During each episode, log transitions into a `TraceBuffer`
    * Store symbolic annotations if possible (e.g., "picked up key", "entered trap zone")
2. Trace Analysis (Post-Episode)
    * Choose one or more intervention points: steps where alternate actions may lead to meaningful changes (Can be random, saliency-based, or rule-driven)
3. Counterfactual Generation
    * Modify the action at the intervention point (e.g., "turn right" instead of "turn left")
    * Re-run the rest of the episode with the new trajectory (either using the same policy or fixed rollouts)
    * Compare the results: Changes in reward, outcome, symbolic events
4. Optional Learning/Training Signal
    * Use insights from counterfactual rollouts to:
        * Update value/policy networks
        * Train a counterfactual predictor model
        * Populate causal graphs (state -> outcome dependencies)
        * Generate human-readable explanations

## Outputs/Evaluation Metrics:

| Output                    | Purpose                                                                   |
|---------------------------|---------------------------------------------------------------------------|
| Causal Trace Logs         | Can be used to visualize, debug, and analyze behavior                     |
| Counterfactual Reports    | Differences in trajectory/reward between actual and hypothetical          |
| Causal Graph              | Encodes the learned relationships between state -> action -> outcome      |
| Explainability Reports    | "Had the agent done X, it would have reached goal ffaster/avoided trap"   |
| Policy Improvement        | Better generalization or learning speed                                   |

## Novelty Compared to Prior Work:

| Prior             | Difference                                                                                                        |
|-------------------|-------------------------------------------------------------------------------------------------------------------|
| Madumal et al.    | Focuses on pre-defined SCMs; we build symbolic traces + perform direct trace-based interventions                  |
| Model-based RL    | Focuses on full environment prediction; we work at a symbolic intervention level                                  |
| Causal Curiosity  | Focuses on intrinsic motivation to uncover causal structure; we focus on exploiting it to generate trace-level explanations   |
| Neuro-symbolic RL | Often uses external logic modules or planners; we stay within the agent’s own experience, grounded in RL traces   |