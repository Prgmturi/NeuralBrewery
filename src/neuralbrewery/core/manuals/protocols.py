from typing import Protocol, runtime_checkable

from neuralbrewery.core.manuals.schemas import ManualPassage


@runtime_checkable
class ManualSearch(Protocol):
    """A search over the manuals of the components: the agent reads, and no more.

    It holds text only: nothing here reads the plant or the queue.
    """

    def tags(self) -> frozenset[str]:
        """The tags that have at least one manual."""
        ...

    def search(self, query: str, tag: str = "", limit: int = 3) -> list[ManualPassage]:
        """The passages that match the query best, the best first, at most limit.

        tag, if given, keeps the manuals of that component only, in any
        case. Empty when no passage matches: never an error.
        """
        ...
