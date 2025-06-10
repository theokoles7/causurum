"""# causurum.environments.grid_world.GridWorld

Define symbolic Grid World environment.
"""

__all__ = ["GridWorld"]

from typing                             import override

from environments.__base__              import Environment
from environments.grid_world.actions    import actions
from environments.grid_world.grid       import Grid

class GridWorld(Environment):
    """# Grid World.
    
    Discrete, deterministic grid environment game.
    """
    
    def __init__(self,
        # Dimensions.
        columns:            int =                           4,
        rows:               int =                           4,
        
        # Features.
        coins:              set[tuple[int]] =               set(),
        goal:               tuple[int] =                    None,
        loss:               set[tuple[int]] =               set(),
        portals:            list[dict[str, tuple[int]]] =   [],
        start:              tuple[int] =                    (0, 0),
        walls:              set[tuple[int]] =               set(),
        wrap_map:           bool =                          False,
        
        # Rewards.
        coin_reward:        float =                         0.5,
        goal_reward:        float =                         1.0,
        
        # Penalties.
        collision_penalty:  float =                         -0.1,
        loss_penalty:       float =                         -0.5,
        step_penalty:       float =                         -0.01,
        **kwargs
    ):
        """# Instantiate Grid World Environment.
        
        ## Dimensions:
            * rows              (int):                          Number of rows with which grid will 
                                                                be initialized. Must be within range 
                                                                1-10. Defaults to 4.
            * columns           (int):                          Number of columns with which grid 
                                                                will be initialized. Must be within 
                                                                range 1-10. Defaults to 4.
        
        ## Features:
            * coins             (set[tuple[int]]):              Set of row, column coordinates at 
                                                                which coins can be picked. Coins are 
                                                                ephimeral, such that they no longer 
                                                                exist once an agent has acquired 
                                                                them. This feature can be useful in 
                                                                evaluating an agent's temporal 
                                                                credit assignment capabilities. 
                                                                Collecting coins will yirld the 
                                                                reward defined by `coin_reward`.
            * goal              (tuple[int]):                   Row, column coordinate at which the 
                                                                goal square will be located. Only 
                                                                one goal exists for any grid world 
                                                                environment. This location will 
                                                                default to the top right square of 
                                                                the grid. Entering this square will 
                                                                terminate the episode and yield the 
                                                                reward defined by `goal_reward`.
            * loss              (list[tuple[int]]):             Set of row, column coordinates at 
                                                                which loss squares will be located. 
                                                                These squares serve as terminal 
                                                                states of the environment. Entering 
                                                                this square will terminate the 
                                                                episode and incur the penalty 
                                                                defined by `loss_penalty`.
            * portals           (list[dict[str, tuple[int]]]):  List of portal maps specifying 
                                                                "entry" and "exit" coordinates.
            * start             (tuple[int]):                   Row, column coordinate at which the 
                                                                agent will begin interacting with 
                                                                the environment at the beginning of 
                                                                each episode. This location will 
                                                                default to the bottom left square of 
                                                                the grid, (0, 0).
            * walls             (set[tuple[int]]):              Set of row, column coordinates at 
                                                                which wall squares will be located. 
                                                                Colliding with these squares incurs 
                                                                the penalty defined by 
                                                                `collision_penalty`.
            * wrap_map          (bool):                         If True, the agent will not incur 
                                                                collision penalties when attempting 
                                                                to move outside the boundaries of 
                                                                the grid. Instead, it will appear at 
                                                                the opposite side of the grid from 
                                                                whence it violated the boundary.
        
        ## Rewards:
            * coin_reward       (float):                        Reward yielded if the agent collects 
                                                                a coin (enters a coin square defined 
                                                                by `coins`). Defaults to 0.5.
            * goal_reward       (float):                        Reward yielded if the agent enters 
                                                                the goal square, terminating the 
                                                                episode. Defaults to 1.0.
        
        ## Penalties:
            * collision_penalty (float):                        Penalty incured if the agent 
                                                                collides with a wall square (enters 
                                                                a square defined by `walls`) or a 
                                                                grid boundary (only applies if 
                                                                `wrap_map` is False). Defaults to 
                                                                -0.1.
            * loss_penalty      (float):                        Penalty incured if the agent enters 
                                                                a loss square, terminating the 
                                                                episode. Defaults to -0.5.
            * step_penalty      (float):                        Penalty incured upon every step that 
                                                                the agent submits if the resulting 
                                                                state does not apply to other 
                                                                rewards/penalties defined. Defaults 
                                                                to -0.01.
        """
        # Instantiate environment.
        super(GridWorld, self).__init__()
        
        # Initialize grid.
        self._grid_:                Grid =          Grid(**{k: v for k, v in locals().items() if k != "self"})
        
        # Define features.
        self._start_:               tuple[int] =    start
        self._wrap_map_:            bool =          wrap_map
        
        # Define penalties.
        self._collision_penalty_:   float =         collision_penalty
        
        # Set environment to initial state.
        self.reset()
        
    def __repr__(self) -> str:
        """# Get String.
        
        Provide string representation of Grid World grid.

        ## Returns:
            * str: String representation of grid.
        """
        # Initialize with top border.
        grid_str:           str =   "   ┌" + ("───┬" * (self.grid.columns - 1)) + "───┐"
        
        # For each row in grid...
        for r, row in reversed(list(enumerate(self.grid))):
            
            # Append left border with row index.
            grid_str +=             f"\n {r} │"
            
            # For each square in row...
            for s, square in enumerate(row):
                
                # Format agent if it's at this position.
                if self._agent_position_ == (r, s): grid_str += f" A │"
                
                # Otherise, append square symbol.
                else: grid_str +=         f" {square} │"
                
            # Append dividing line if not at end of grid.
            if r != 0: grid_str +=  "\n   ├" + ("───┼" * (self.grid.columns - 1)) + "───┤"
            
        # Initialize column index.
        col_idx:            str =   "\n   "
            
        # Populate column index.
        for col in range(self.grid.columns): col_idx += f"  {col} "
            
        # Provide grid string.
        return grid_str + "\n   └" + ("───┴" * (self.grid.columns - 1)) + "───┘" + col_idx
        
    @property
    def grid(self) -> Grid:
        """# Get Grid.
        
        Provide Grid World grid.

        ## Returns:
            * Grid: Current Grid World grid.
        """
        return self._grid_
    
    @override
    def reset(self) -> None:
        """# Reset Environment.
        
        Reset Grid World grid, statistics, etc.
        """
        # Reset agent position to start coordinate.
        self._agent_position_:      tuple[int] =    self._start_
        
        # Define game statistics.
        self._game_status_:         str =           "INCOMPLETE"
        self._cumulative_reward_:   float =         0.0
        self._coins_remaining_:     list[tuple] =   self.grid.coins.copy()
        self._coins_collected_:     int =           0
        self._portal_activations_:  int =           0
        # self._wall_collisions_:
        
        # Reset grid.
        self._grid_.reset()
        
    @property
    def shape(self) -> tuple:
        """# Get Shape.
        
        Provide two-dimensional shape of grid component.

        ## Returns:
            * tuple:    Two dimensional grid shape.
        """
        return (self.rows, self.columns)
        
    @override
    def step(self,
        action: int
    ) -> tuple[tuple[int], float, bool, dict]:
        """# Submit Action.
        
        Submit action to environment. Possible Grid World actions:
        * 0: UP
        * 1: DOWN
        * 2: LEFT
        * 3: RIGHT

        ## Args:
            * action    (int):  Action being submitted.

        ## Returns:
            * tuple[tuple[int], float, bool, dict]:
                * Agent's position after action was taken.
                * Reward yielded/penalty incurred by action taken.
                * Flag indicating if new position is a terminal state (episode concludes).
                * Metadata related to action taken and the new state of the environment.
        """
        # Calculate agent's new position.
        next_position:  tuple[int] =    (
                                            self._agent_position_ + actions[action]["delta"][0],
                                            self._agent_position_ + actions[action]["delta"][1]
                                        )
        
        # If position is out of bounds...
        if not self.grid.contains(coordinate = next_position):
            
            # If map is not wrapped...
            if not self._wrap_map_:
                
                # Return penalty with no effect.
                return  (
                            self._agent_position_,
                            self._collision_penalty_,
                            False,
                            {
                                "event":    "Action leads out of bounds"
                            }
                        )
                
            # Otherwise, modulate position.
            next_position:  tuple[int] =    (
                                                next_position[0] % self.grid.rows,
                                                next_position[1] % self.grid.columns
                                            )
            