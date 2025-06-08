"""# cuasurum.args

Causurum application argument definitions and parsing.
"""

__all__ = ["parse_ludorum_arguments"]

from argparse   import ArgumentParser, _ArgumentGroup, Namespace, _SubParsersAction


def parse_ludorum_arguments() -> Namespace:
    """# Parse Causurum Arguments.
    
    This function should be called at the entry point of the Causurum application. The name space of 
    argument keys and values that it provides will be passed/provided to subsequent module entry 
    points.
    
    ## Returns:
        * NameSpace:    Name space of parsed arguments and their values.
    """
    # Initialize primary parser
    _parser_:       ArgumentParser =    ArgumentParser(
        prog =          "causurum",
        description =   """A modular framework for Neuro-Symbolic Reinforcement Learning with a 
                        focus on causal reasoning, systematic generalization, and interpretable 
                        agents."""
    )

    # Initialize sub-parser
    _subparser_:    _SubParsersAction = _parser_.add_subparsers(
        dest =          "command",
        help =          "Causurum commands."
    )

    # +============================================================================================+
    # | BEGIN ARGUMENTS                                                                            |
    # +============================================================================================+

    # LOGGING ======================================================================================
    _logging_:      _ArgumentGroup =    _parser_.add_argument_group(
        title =         "Logging",
        description =   "Logging configuration."    
    )

    _logging_.add_argument(
        "--logging-level",
        type =          str,
        choices =       ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "NOTSET"],
        default =       "INFO",
        help =          """Minimum logging level (DEBUG < INFO < WARNING < ERROR < CRITICAL). 
                        Defaults to "INFO"."""
    )

    _logging_.add_argument(
        "--logging-path",
        type =          str,
        default =       "logs",
        help =          """Path at which logs will be written. Defaults to "./logs/"."""
    )

    # +============================================================================================+
    # | END ARGUMENTS                                                                              |
    # +============================================================================================+

    # Parse arguments
    return _parser_.parse_args()