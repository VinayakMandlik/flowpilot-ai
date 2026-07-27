from abc import ABC, abstractmethod
from typing import Generator


class BaseProvider(ABC):

    @abstractmethod
    def stream(self, prompt: str) -> Generator[str, None, None]:
        """
        Stream the response from the LLM.
        """
        pass