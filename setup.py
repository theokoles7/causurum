"""# causurum.setup

Setup utility for building Causurum.
"""

from setuptools import find_packages, setup

setup(
    name =              "causurum",
    version =           "0.0.1",
    author =            "Gabriel C. Trahan",
    author_email =      "gabriel.trahan1@louisiana.edu",
    description =       """A modular framework for Neuro-Symbolic Reinforcement Learning with a 
                        focus on causal reasoning, systematic generalization, and interpretable 
                        agents.""",
    license =           "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007",
    license_files =     ("LICENSE"),
    url =               "https://github.com/theokoles7/causurum",
    packages =          find_packages(),
    python_requires =   ">=3.10",
    install_requires =  [
        
                        ]
)