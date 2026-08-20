from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol


# slots=true means replace the __dict__ hash table that maps attributes to values
# with a fixed array, meaning that you get less memory and speed here
@dataclass(slots=True)
class Document:
    """
    This is what chunking, db, retieval, citations, etc. will rely on
    To swtich out the corpus, you only need to write a new parser that spits
    out documents, everything else can stay the same
    """

    source_id: str  # Stabe (consistent between runs) )UID
    title: str  # Use in citations
    text: str  # This is what gets chunked
    url: str  # Where verify claims when checking

    # Breadcrumb trail, outermost first: ["Reference", "SQL", "CREATE INDEX"]
    # field(default_factory=list) to create one list for each instance
    section_path: list[str] = field(default_factory=list)

    published_at: datetime | None = None

    # Extra corpus-specific stuff (GitHub labels, author, etc.) stored as JSONB
    # For new parsers to carry their own metadata
    extra: dict = field(default=dict)


# Anything with a parse() method is a Parser
class Parser(Protocol):
    def parse(self) -> Iterator[Document]: ...
