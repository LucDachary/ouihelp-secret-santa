from typing import Set, Optional


class Participant:
    """A Secret Santa participant, represented by its name.

    Each participant has its set of valid recipient options.
    """
    __name: str
    __options: Set

    def __init__(self, name, options: Optional[Set] = None):
        assert isinstance(name, str) and name, "Please provide the name as a non-empty string."
        if options is not None:
            assert isinstance(options, set), "Please provide the options as a set of Participant."
            for option in options:
                assert isinstance(option, Participant), "All options must be of type Participant."

        self.__name = name
        self.__options = options or set()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def options(self) -> Set:
        """Provide the valid recipient options as a set."""
        return self.__options

    @options.setter
    def options(self, new_options: Set):
        assert isinstance(new_options, set)
        for new_option in new_options:
            assert isinstance(new_option, Participant), "All options must be of type Participant."

        self.__options = new_options

    @property
    def options_str(self) -> str:
        """Return a string representation of the recipient options.

        Options are sorted alphabetically.
        """
        return ", ".join(sorted(map(str, self.__options)))

    def __str__(self):
        return self.__name

    def __repr__(self):
        return f"{self.__name} [options: {len(self.__options)}]"
