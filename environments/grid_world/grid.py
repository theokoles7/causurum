"""# causurum.environments.grid_world.Grid

Define structure, properties, and functions of Grid World grid.
"""

__all__ = ["Grid"]

from typing                             import Iterator

from environments.grid_world.squares    import *

class Grid():
    """# Grid World Grid.
    
    2D representation of squares that constitue Grid World grid.
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
        # Define dimensions.
        self._columns_:             int =                           columns
        self._rows_:                int =                           rows
        
        # Define features.
        self._coins_:               set[tuple[int]] =               coins
        self._goal_:                tuple[int] =                    goal if goal is not None else (self.rows - 1, self.columns - 1)
        self._loss_:                set[tuple[int]] =               loss
        self._portals_:             list[dict[str, tuple[int]]] =   portals
        self._walls_:               set[tuple[int]] =               walls
        self._wrap_map_:            bool =                          wrap_map
        
        # Define rewards.
        self._coin_reward_:         float =                         coin_reward
        self._goal_reward_:         float =                         goal_reward
        
        # Define penalties.
        self._collision_penalty_:   float =                         collision_penalty
        self._loss_penalty_:        float =                         loss_penalty
        self._step_penalty_:        float =                         step_penalty
        
        # Initialize grid.
        self._grid_:                list[list[Square]] =            self.populate_grid()
        
    def __getitem__(self,
        key:    tuple[int, int]
    ) -> Square:
        """# Get Square.
        
        Get grid element located at given coordinate.

        ## Args:
            * key   (tuple[int, int]):  Coordinate of Square element being fetched.

        ## Returns:
            * Square:   Square element located at given coordinate.
        """
        return self._grid_[key[0]][key[1]]
    
    def __iter__(self) -> Iterator[list[Square]]:
        """# Iterate Over Elements.
        
        Provide iterable of grid rows.

        ## Yields:
            * Iterator[list[Square]]:   Grid row iterable.
        """
        for row in self._grid_: yield row
    
    def __setitem__(self,
        key:    tuple[int, int],
        square: Square
    ) -> None:
        """# Set Square.
        
        Set grid element located at given coordinate.

        ## Args:
            * key       (tuple[int, int]):  Coordinate of Square element being set.
            * square    (Square):           Square object being assigned to coordinate.
        """
        self._grid_[key[0]][key[1]] = square
        
    @property
    def coins(self) -> set[tuple[int]]:
        """# Get Coins.
        
        Provide set of coin coordinates defined at environment initialization.

        ## Returns:
            * set[tuple[int]]:  Original set of coin coordinates.
        """
        return self._coins_.copy()
        
    @property
    def coin_reward(self) -> float:
        """# Get Coin Reward.
        
        Provide reward value for collecting a coin.

        ## Returns:
            * float:    Reward for collecting a coin.
        """
        return self._coin_reward_
    
    @property
    def columns(self) -> int:
        """# Get Columns.

        Provide number of columns in grid.

        ## Returns:
            * int:  Number of columns in grid.
        """
        return self._columns_

    @property
    def collision_penalty(self) -> float:
        """# Get Collision Penalty.
        
        Provide penalty value for colliding with a wall or boundary.

        ## Returns:
            * float:    Penalty for collision.
        """
        return self._collision_penalty_
    
    def contains(self,
        coordinate: tuple[int]
    ) -> bool:
        """# Grid Contains?
        
        Indicate if given coordinate is an element of grid space.

        ## Args:
            * coordinate    (tuple[int]):   Coordinate for which to search within grid space.

        ## Returns:
            * bool:
                * True:     Coordinate ∈ Grid
                * False:    Coordinate ∉ Grid
        """
        return  (
                    # Row coordinate is valid.
                    0 < coordinate[0] < self.rows and
                    
                    # Column coordinate is valid.
                    0 < coordinate[1] < self.columns
                )
    
    def get_portal_exit(self,
        entry:  tuple[int]
    ) -> tuple[int]:
        """# Get Portal Exit.
        
        Get the respective portal exit for the given entry point.

        ## Args:
            * entry (list[int]):    Portal entry that will be used as index to look up respective 
                                    entry.

        ## Returns:
            * tuple[int]:   Respective portal exit coordinate.
        """
        # For each portal defined...
        for portal in self.portals:
            
            # Return the exit coordinate when found.
            if portal["entry"] == entry: return portal["exit"]
    
    @property
    def goal(self) -> tuple[int]:
        """# Get Goal.
        
        Provide goal coordinate.

        ## Returns:
            * tuple[int]:   Grid's goal coordinate.
        """
        return self._goal_

    @property
    def goal_reward(self) -> float:
        """# Get Goal Reward.
        
        Provide reward value for reaching the goal square.

        ## Returns:
            * float:    Reward for reaching the goal square.
        """
        return self._goal_reward_

    @property
    def loss(self) -> set[tuple[int]]:
        """# Get Loss Squares.
        
        Provide loss square coordinates.

        ## Returns:
            * set[tuple[int]]:  Loss square coordinates.
        """
        return self._loss_.copy()

    @property
    def loss_penalty(self) -> float:
        """# Get Loss Penalty.
        
        Provide penalty value for entering a loss square.

        ## Returns:
            * float:    Penalty for entering a loss square.
        """
        return self._loss_penalty_
    
    def populate_grid(self) -> list[list[Square]]:
        """# Populate Grid.
        
        Initialize & populate grid according to parameters specified in class instantiation.

        ## Returns:
            * list[list[Square]]:   2D grid, populated with Squares.
        """
        # Initialize empty grid.
        grid:   list[list[Square]] =    [[None for _ in range(self.columns)] for _ in range(self.rows)]
        
        # For each row in grid...
        for r, row in enumerate(grid):
            
            # For each square in row...
            for s, square in enumerate(row):
                
                # Instantiate squares based on parameters.
                # Coins.
                if (r, s) in self.coins:            grid[r][s] =    Coin(
                                                                        coordinate =    (r, s),
                                                                        value =         self.coin_reward
                                                                    )
                
                # Goal.
                elif (r, s) == self.goal:           grid[r][s] =    Goal(
                                                                        coordinate =    (r, s),
                                                                        value =         self.goal_reward
                                                                    )
                
                # Loss.
                elif (r, s) in self.loss:           grid[r][s] =    Loss(
                                                                        coordinate =    (r, s),
                                                                        value =         self.loss_penalty
                                                                    )
                
                # Portal Entries.
                elif (r, s) in self.portal_entries: grid[r][s] =    PortalEntry(
                                                                        coordinate =    (r, s),
                                                                        exit =          self.get_portal_exit(
                                                                                            entry = (r, s)
                                                                                        )
                                                                    )
                
                # Portal Exits.
                elif (r, s) in self.portal_exits:   grid[r][s] =    PortalExit(
                                                                        coordinate =    (r, s)
                                                                    )
                
                # Walls.
                elif (r, s) in self.walls:          grid[r][s] =    Wall(
                                                                        coordinate =    (r, s),
                                                                        value =         self.collision_penalty
                                                                    )
                
                # Generic Squares.
                else:                               grid[r][s] =    Square(
                                                                        coordinate =    (r, s)
                                                                    )
                
        # Provide initialized grid.
        return grid

    @property
    def portals(self) -> list[dict[str, tuple[int]]]:
        """# Get Portals.
        
        Provide portal mappings.

        ## Returns:
            * list[dict[str, tuple[int]]]:  List of portal mappings.
        """
        return self._portals_.copy()
    
    @property
    def portal_entries(self) -> set[tuple[int]]:
        """# Get Portal Entries.
        
        Provide set of all portal entrance coordinates.

        ## Returns:
            * set[tuple[int]]:  Set of portal entry coordinates.
        """
        return set([portal["entry"] for portal in self.portals])
    
    @property
    def portal_exits(self) -> set[tuple[int]]:
        """# Get Portal Exits.
        
        Provide set of all portal exit coordinates.

        ## Returns:
            * set[tuple[int]]:  Set of portal exit coordinates.
        """
        return set([portal["exit"] for portal in self.portals])
    
    def reset(self) -> None:
        """# Reset Grid.
        
        Reset the grid, its statistics, and all Squares contained within.
        """
        # For each row...
        for row in self._grid_:
            
            # For each square in row...
            for square in row:
                
                # Reset square.
                square.reset()

    @property
    def rows(self) -> int:
        """# Get Rows.
        
        Provide number of rows in grid.

        ## Returns:
            * int:  Number of rows in grid.
        """
        return self._rows_

    @property
    def start(self) -> tuple[int]:
        """# Get Start Position.
        
        Provide starting position of the agent.

        ## Returns:
            * tuple[int]:   Starting position coordinates.
        """
        return self._start_

    @property
    def step_penalty(self) -> float:
        """# Get Step Penalty.
        
        Provide penalty value incurred for each step.

        ## Returns:
            * float:    Penalty for each step.
        """
        return self._step_penalty_
    
    def validate_coordinates(self) -> None:
        """# Validate Coordinates.
        
        Validate coordinates of all grid features to ensure that they do not conflict with each 
        other.

        ## Raises:
            * ValueError:   If coordinate conflict is found.
        """
        from collections    import Counter
        
        # Initialize list to store coordinates.
        coordinates:    list[tuple[int]] =  []
        
        # Flatten all coordinates into list.
        coordinates.extend(self.coins)
        coordinates.extend([self.goal])
        coordinates.extend(self.loss)
        coordinates.extend([portal["entry"], portal["exit"]] for portal in self.portals)
        coordinates.extend(self.start)
        coordinates.extend(self.walls)
        
        # For each coordinate provided...
        for coord in coordinates:
            
            # If it's out of bounds.
            if  any([
                coord[0] <  0,
                coord[0] >= self.rows,
                coord[1] <  0,
                coord[0] >= self.columns
            ]):
                
                # Raise error.
                raise ValueError(f"Coordinate {coord} is out of bounds.")
        
        # Cout how many oocurrences there are of each coordinate.
        conflicts:      list[tuple[int]] =  [
                                                position
                                                for position, count
                                                in Counter(coordinates)
                                                if count > 1
                                            ]
        
        # If there are conflicts...
        if conflicts:
            
            # Raise error to report them.
            raise ValueError(f"Conflicting coordinates defined for features:{"\n".join(str(coord) for coord in coordinates)}")

    @property
    def walls(self) -> set[tuple[int]]:
        """# Get Walls.
        
        Provide wall square coordinates.

        ## Returns:
            * set[tuple[int]]:  Original set of wall square coordinates.
        """
        return self._walls_.copy()

    @property
    def wrap_map(self) -> bool:
        """# Get Wrap Map.
        
        Indicate whether the grid allows wrap-around movement.

        ## Returns:
            * bool: True if wrap-around is enabled, False otherwise.
        """
        return self._wrap_map_