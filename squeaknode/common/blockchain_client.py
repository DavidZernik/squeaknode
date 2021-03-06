from abc import ABC, abstractmethod
from typing import Optional


class BlockchainClient(ABC):
    """Used to get info from the blockchain."""

    @abstractmethod
    def get_latest_block_height(self) -> int:
        pass

    @abstractmethod
    def get_block_hash(self, block_height: int) -> Optional[bytes]:
        pass
