# -*- encoding: UTF-8 -*-

# Standard imports
from abc         import ABC, abstractmethod
from typing      import List
from dataclasses import dataclass

# Third party imports

# Application imports

class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def resolve(self, emails: List):
        pass

@dataclass
class AbstractHandler(ABC):
    next: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self.next = handler

        return handler

    @abstractmethod
    async def resolve(self, emails: List):
        if self.next:
            return await self.next.resolve(emails)

        return None

    async def clean(self):
        pass
