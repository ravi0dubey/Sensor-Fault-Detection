# Setup file is created where we write statement so that sensor folder will behave as libraries

from setuptools import find_packages,setup
from typing import List

#def get_requirements() -> List[str]:
def get_requirements() :
    """
    This function will read requirements.txt file and will  append into the list
    """
    requirement_list:List[str] = []
    return requirement_list

setup(
    name ="sensor",
    version="0.0.1",
    author="ineuron",
    author_email="Ravi0dubey@gmail.com",
    packages=find_packages(),
    install_requires= [],
)