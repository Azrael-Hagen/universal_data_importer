from typing import List, Dict, Optional


class Pipeline:
    """
    Represents a Meltano pipeline configuration.
    """

    def __init__(
        self,
        source: str,
        target: str,
        transforms: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ):
        self.source = source
        self.target = target
        self.transforms = transforms or []
        self.metadata = metadata or {}

    # -----------------------------------------
    # Pipeline representation
    # -----------------------------------------

    def to_command(self) -> List[str]:
        """
        Convert pipeline into Meltano CLI command.
        """

        command = [
            "meltano",
            "run",
            self.source
        ]

        command.extend(self.transforms)

        command.append(self.target)

        return command

    # -----------------------------------------
    # Serialization
    # -----------------------------------------

    def to_dict(self) -> Dict:

        return {
            "source": self.source,
            "target": self.target,
            "transforms": self.transforms,
            "metadata": self.metadata,
        }

    # -----------------------------------------
    # Utility
    # -----------------------------------------

    def describe(self) -> str:
        """
        Human readable pipeline description.
        """

        transforms = ", ".join(self.transforms) if self.transforms else "none"

        return (
            f"Pipeline:\n"
            f"  Source: {self.source}\n"
            f"  Transforms: {transforms}\n"
            f"  Target: {self.target}"
        )

    def __repr__(self):

        return f"<Pipeline {self.source} -> {self.target}>"