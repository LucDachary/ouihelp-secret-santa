import logging
from typing import List, Tuple, Dict, Set

from secret_santa.model import Participant

logger = logging.getLogger(__name__)


def parse_data(names: Set[str], exclusions: List[Tuple[str, str]]) -> Dict[str, Participant]:
    """Parse and build the set of Participant.

    exclusions represent pairs of names that must not be options for one another.
    Each Participant has its list of valid recipient options.
    Return a mapping of names and Participant.
    """
    # Each Participant is initialised with zero option.
    participants = dict([(name, Participant(name)) for name in names])

    # Add all options by default.
    all_participants = participants.values()
    for name, par in participants.items():
        par.options = set(all_participants) - set([par])

    # Remove options according to exclusions.
    for mate1, mate2 in exclusions:
        participants[mate1].options.remove(participants[mate2])
        participants[mate2].options.remove(participants[mate1])

    return participants


def secure_one_option_participants(participants: Dict[str, Participant]) -> Dict[str, Participant]:
    """Browse and modify the list of participants to secure the single options.

    If a participant only has one recipient option, this function will try to remove it from others'
    recipient options, to "secure" it.

    Return the refined mapping.
    """
    logging.debug(f"Got participants to secure: {participants!r}")

    to_secure = list(filter(lambda p: len(p.options) == 1, participants.values()))
    logging.debug(f"Initial list of participant to secure: {to_secure!r}")

    while to_secure:
        vip = to_secure.pop()

        for par in participants.values():
            if vip != par:
                # That would make an interesting search: https://stackoverflow.com/a/60233
                try:
                    par.options.remove(min(vip.options))

                    match len(par.options):
                        # We might have created another "single recipient option" participant,
                        # so queue up!
                        case 1:
                            logging.debug(f"{par.name} is down to one option. To be secured…")
                            to_secure.append(par)
                        case 0:
                            raise RuntimeError("Cannot secure this set of Participant.")
                except KeyError:
                    # this option was not available for par; nothing to do.
                    pass

    return participants


def work_a_distribution(participants: Dict[str, Participant], path: List[Participant]) -> bool:
    """Browse the list of participants using a backtrack algorithm.

    In case a valid distribution is found, path will represent the chain of sender-recipient.
    Return false in case no valid distribution can be worked out.

    This is a recursive function.
    """
    if len(path) == len(participants) and path[0] in path[-1].options:
        logging.debug(f"Found a path! {path=!r}")
        return True

    for name, par in participants.items():
        if par not in path:
            path.append(par)  # Trying…
            if work_a_distribution(participants, path):
                return True
            else:
                path.pop()  # … backtracking.

    logging.debug(f"Failed to find path. {path=!r}")

    return False
