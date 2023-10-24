from unittest import TestCase, skip

from secret_santa import lib
from secret_santa.model import Participant


class LibTestCase(TestCase):
    @skip("TODO")
    def test_parse_data_empty(self):
        """Try to parse an empty data set."""
        pass

    def test_parse_data_ouihelp(self):
        people = set(["Florent", "Jessica", "Coline", "Emilien", "Ambroise", "Bastien"])
        exclusions = [("Florent", "Jessica"), ("Coline", "Emilien")]

        participants = lib.parse_data(people, exclusions)

        self.assertEqual(len(participants), len(people))

        self.assertIn("Coline", participants["Florent"].options_str,
                      "Coline should be an option for Florent.")
        self.assertNotIn("Jessica", participants["Florent"].options_str,
                         "Jessica should not be an option for Florent.")

        # Exhaustive assertions
        self.assertEqual(participants["Florent"].options_str, "Ambroise, Bastien, Coline, Emilien")
        self.assertEqual(participants["Jessica"].options_str, "Ambroise, Bastien, Coline, Emilien")
        self.assertEqual(participants["Coline"].options_str, "Ambroise, Bastien, Florent, Jessica")
        self.assertEqual(participants["Emilien"].options_str, "Ambroise, Bastien, Florent, Jessica")
        self.assertEqual(participants["Ambroise"].options_str,
                         "Bastien, Coline, Emilien, Florent, Jessica")
        self.assertEqual(participants["Bastien"].options_str,
                         "Ambroise, Coline, Emilien, Florent, Jessica")

    def test_secure(self):
        # A, B, C, D
        albert = Participant("Albert")
        bertrand = Participant("Bertrand")
        caroline = Participant("Caroline")
        david = Participant("David")

        # A → B, A→ C
        albert.options.add(bertrand)
        albert.options.add(caroline)

        # B → A, B → C, B → D
        bertrand.options.add(albert)
        bertrand.options.add(caroline)
        bertrand.options.add(david)

        # C→ A, C → D
        caroline.options.add(albert)
        caroline.options.add(david)

        # D → A
        david.options.add(albert)

        mapping = {
            "Albert": albert,
            "Bertrand": bertrand,
            "Caroline": caroline,
            "David": david,
        }

        secured_mapping = lib.secure_one_option_participants(mapping)
        self.assertIsInstance(secured_mapping, dict)
        self.assertEqual(len(mapping), len(secured_mapping))

        #
        # Domino effect

        # Chronologically:
        # 1. Albert is the sole recipient option of David, it is secured;
        #    →  Bertrand and Caroline no longer have Albert as recipient option.
        # 2. Caroline is down to one recipient option, David is being secured;
        #    →  Bertrand no longer has David as recipient option.
        # 3. Bertrand is down to one recipient option, Caroline is being secured;
        #    →  Albert no longer has Caroline as recipient option.
        # 4. Albert is down to one recipient option, Bertrand is being secured.

        self.assertEqual(albert.options, set([bertrand]))
        self.assertEqual(bertrand.options, set([caroline]))
        self.assertEqual(caroline.options, set([david]))
        self.assertEqual(david.options, set([albert]))

    def test_work(self):
        # A, B, C, D
        albert = Participant("Albert")
        bertrand = Participant("Bertrand")
        caroline = Participant("Caroline")
        david = Participant("David")

        participants = {
            "Albert": albert,
            "Bertrand": bertrand,
            "Caroline": caroline,
            "David": david,
        }

        albert.options.add(bertrand)
        bertrand.options.add(caroline)
        caroline.options.add(david)
        david.options.add(albert)

        #
        # Case 1: there is a path.
        path = []
        is_path = lib.work_a_distribution(participants, path)
        self.assertTrue(is_path)
        # A → B → C → D
        self.assertEqual(path, [albert, bertrand, caroline, david])

        #
        # Case 2: there is no path.
        participants["David"].options = set([bertrand, caroline])
        is_path = lib.work_a_distribution(participants, path)
        self.assertFalse(is_path)
