import json
from pathlib import Path
import unittest


NOTEBOOK = Path(__file__).parents[1] / "Indoor_Air_Quality_model.ipynb"


class NotebookReproducibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        cls.cells = ["".join(cell.get("source", [])) for cell in cls.notebook["cells"]]

    def test_notebook_file_and_parameter_instructions_are_current(self):
        readme = NOTEBOOK.with_name("README.md").read_text(encoding="utf-8")
        self.assertIn("Indoor_Air_Quality_model.ipynb", readme)
        self.assertNotIn("Wellcome_Trust_WindowAC.ipynb", readme)
        self.assertNotIn("Wellcome_Trust_0505.ipynb", readme)
        self.assertIn("05282025_test.txt", readme)
        self.assertIn("not tracked", readme)

    def test_scenario_calls_supply_required_infiltration_argument(self):
        calls = [cell for cell in self.cells if "solve_static(" in cell and "def solve_static(" not in cell]
        self.assertTrue(calls)
        for cell in calls:
            self.assertIn("ach_inf_base=", cell)

    def test_parameter_loader_has_clear_missing_and_schema_validation(self):
        loader = next(cell for cell in self.cells if "def load_params(" in cell)
        self.assertIn("FileNotFoundError", loader)
        self.assertIn("REQUIRED_PARAMS", loader)
        self.assertIn("missing required keys", loader)
        self.assertIn("Duplicate parameter", loader)


if __name__ == "__main__":
    unittest.main()
