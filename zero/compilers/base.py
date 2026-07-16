from abc import ABC, abstractmethod
from pathlib import Path


class BaseCompiler(ABC):
    """
    Base class for Compilers utilizing pathlib.Path objects.
    """

    def __init__(self) -> None:
        super().__init__()


    @abstractmethod
    def get_dependencies(self, filepath: Path) -> list[Path]:
        pass


    @abstractmethod
    def build_file(self, filepath: Path, outfile: Path) -> None:  
        pass
    

    @abstractmethod
    def link(self, objects: list[Path], outfile: Path) -> None:  
        pass