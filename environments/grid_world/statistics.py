"""# causurum.environments.grid_world.Statistics

Define statistics management functions and utilities.
"""

__all__ = ["Statistics"]

class Statistics():
    """# Grid World Game Statistics.
    
    Record book for tracking game play statistics relevant to Grid World environment.
    """
    
    def __init__(self,
        grid_shape: tuple[int, int]
    ):
        """# Instantiate Game Statistics.

        ## Args:
            * grid_shape    (tuple[int, int]):  Shape of grid.
        """
        # Initialize data map.
        self._data_:    dict =  {
                                    "coins":        {
                                                        "collected":    0,
                                                        "remaining":    0,
                                                        "ratio":        0.0,
                                                        "reward":       0.0
                                                    },
                                    "collisions":   {
                                                        "boundary":     0,
                                                        "wall":         0,
                                                        "penalty":      0.0,
                                                    },
                                    "portals":      {
                                                        "activated":    0
                                                    },
                                    "squares":      {
                                                        "visited":      0,
                                                        "not_visited":  grid_shape[0] * grid_shape[1],
                                                        "ratio":        0.0
                                                    },
                                    "status":       "INCOMPLETE",
                                    "steps":        {
                                                        "taken":        0,
                                                        "squence":      []
                                                    }
        }