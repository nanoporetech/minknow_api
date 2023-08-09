import re
import sys
import unittest
from pathlib import Path
from typing import Sequence

from minknow_api.protocol_pb2 import BarcodeUserData

example_root = Path(__file__).parent.parent.parent / "minknow_api" / "examples"
sys.path.insert(0, example_root)

from minknow_api.examples.load_sample_sheet import (  # noqa E402
    ParsedSampleSheetEntry,
    SampleSheetParseError,
    load_sample_sheet_csv,
)


def sample_sheet_csv_path(*args):
    return str(
        Path(__file__).parent.joinpath("sample_sheets", *args).with_suffix(".csv")
    )


class TestLoadSampleSheet(unittest.TestCase):
    def compare_sample_sheet(
        self,
        actual: Sequence[ParsedSampleSheetEntry],
        expected: Sequence[ParsedSampleSheetEntry],
    ):
        self.assertEqual(len(actual), len(expected))

        def sort_entries(el):
            return el.flow_cell_id, el.position_id

        def sort_barcode_info(el):
            return el.barcode_name, el.lamp_barcode_id

        for (actual_entry, expected_entry) in zip(
            sorted(actual, key=sort_entries), sorted(expected, key=sort_entries)
        ):
            self.assertEqual(actual_entry.flow_cell_id, expected_entry.flow_cell_id)
            self.assertEqual(actual_entry.position_id, expected_entry.position_id)
            self.assertEqual(actual_entry.sample_id, expected_entry.sample_id)
            self.assertEqual(actual_entry.experiment_id, expected_entry.experiment_id)

            if expected_entry.barcode_info is None:
                self.assertIsNone(actual_entry.barcode_info)
            else:
                self.assertIsNotNone(actual_entry.barcode_info)
                self.assertEqual(
                    sorted(
                        actual_entry.barcode_info,
                        key=sort_barcode_info,
                    ),
                    sorted(
                        expected_entry.barcode_info,
                        key=sort_barcode_info,
                    ),
                )

    def test_no_barcoding(self):
        sample_sheet = load_sample_sheet_csv(
            sample_sheet_csv_path("good", "no_barcoding")
        )
        self.compare_sample_sheet(
            sample_sheet,
            [
                ParsedSampleSheetEntry(
                    flow_cell_id="FC001",
                    position_id=None,
                    sample_id="my_sample",
                    experiment_id="my_experiment",
                    barcode_info=None,
                ),
            ],
        )

    def test_single_barcoding(self):
        sample_sheet = load_sample_sheet_csv(
            sample_sheet_csv_path("good", "single_barcoding")
        )
        SampleType = BarcodeUserData.SampleType

        self.compare_sample_sheet(
            sample_sheet,
            [
                ParsedSampleSheetEntry(
                    flow_cell_id="FC001",
                    position_id=None,
                    sample_id=None,
                    experiment_id=None,
                    barcode_info=[
                        BarcodeUserData(
                            barcode_name="barcode01",
                            alias="alias01",
                            type=SampleType.test_sample,
                        ),
                        BarcodeUserData(
                            barcode_name="barcode02",
                            alias="alias02",
                            type=SampleType.positive_control,
                        ),
                        BarcodeUserData(
                            barcode_name="barcode03",
                            alias="alias03",
                            type=SampleType.negative_control,
                        ),
                        BarcodeUserData(
                            barcode_name="barcode04",
                            alias="alias04",
                            type=SampleType.no_template_control,
                        ),
                    ],
                ),
            ],
        )

    def test_dual_barcoding(self):
        sample_sheet = load_sample_sheet_csv(
            sample_sheet_csv_path("good", "dual_barcoding")
        )

        self.compare_sample_sheet(
            sample_sheet,
            [
                ParsedSampleSheetEntry(
                    flow_cell_id="FC001",
                    position_id=None,
                    sample_id=None,
                    experiment_id=None,
                    barcode_info=[
                        BarcodeUserData(
                            barcode_name="external01",
                            barcode_name_internal="internal01",
                            alias="alias01",
                        ),
                        BarcodeUserData(
                            barcode_name="external02",
                            barcode_name_internal="internal01",
                            alias="alias02",
                        ),
                    ],
                ),
            ],
        )

    def test_lampore_barcoding(self):
        sample_sheet = load_sample_sheet_csv(
            sample_sheet_csv_path("good", "lampore_barcoding")
        )

        self.compare_sample_sheet(
            sample_sheet,
            [
                ParsedSampleSheetEntry(
                    flow_cell_id="FC001",
                    position_id=None,
                    sample_id=None,
                    experiment_id=None,
                    barcode_info=[
                        BarcodeUserData(
                            barcode_name="barcode01",
                            lamp_barcode_id="FIP01",
                            alias="alias01",
                        ),
                        BarcodeUserData(
                            barcode_name="barcode02",
                            lamp_barcode_id="FIP01",
                            alias="alias02",
                        ),
                    ],
                ),
            ],
        )

    def test_multiple_positions(self):
        sample_sheet = load_sample_sheet_csv(
            sample_sheet_csv_path("good", "multiple_positions")
        )

        self.compare_sample_sheet(
            sample_sheet,
            [
                ParsedSampleSheetEntry(
                    flow_cell_id=None,
                    position_id="A1",
                    sample_id="my_sample_1",
                    experiment_id="my_experiment",
                    barcode_info=[
                        BarcodeUserData(barcode_name="barcode01", alias="alias01"),
                    ],
                ),
                ParsedSampleSheetEntry(
                    flow_cell_id=None,
                    position_id="A2",
                    sample_id="my_sample_2",
                    experiment_id="my_experiment",
                    barcode_info=[
                        BarcodeUserData(barcode_name="barcode01", alias="alias01"),
                    ],
                ),
            ],
        )

    def test_bad_column_names(self):
        expected_messages = {
            "no_columns": "No columns in sample sheet",
            "invalid_columns": "Unrecognised columns in sample sheet: 'a', 'b'",
            "duplicate_columns": "Duplicate columns in sample sheet: 'sample_id'",
            "no_position_information": "Invalid position information in sample sheet. Must have exactly one of 'flow_cell_id' and 'position_id'",
            "both_position_information": "Invalid position information in sample sheet. Must have exactly one of 'flow_cell_id' and 'position_id'",
            "conflicting_barcoding_columns": "Conflicting barcode column names: 'barcode', 'rapid_barcode', 'fip_barcode'",
            "missing_barcoding_column": "Missing barcoding column names: 'external_barcode'",
            "barcoding_no_alias": "Missing 'alias' column",
            "alias_no_barcoding": "'alias' column supplied, but no other barcode information in sample sheet",
            "type_no_barcoding": "'type' column supplied, but no other barcode information in sample sheet",
            "no_user_info_columns": "Sample sheet contains no user info. "
            + "Should contain 'sample_id', 'experiment_id' or some barcode information",
        }

        for filename, message in expected_messages.items():
            with self.assertRaisesRegex(
                SampleSheetParseError,
                "^" + re.escape(message) + "$",
                msg="Test file: " + filename,
            ):
                load_sample_sheet_csv(
                    sample_sheet_csv_path("bad_column_names", filename),
                    exception_on_unknown_field=True,
                )

            if filename != "invalid_columns":
                with self.assertRaisesRegex(
                    SampleSheetParseError,
                    "^" + re.escape(message) + "$",
                    msg="Test file: " + filename,
                ):
                    load_sample_sheet_csv(
                        sample_sheet_csv_path("bad_column_names", filename),
                        exception_on_unknown_field=False,
                    )

    def test_bad_records(self):
        expected_messages = {
            "sample_type": "Line 2: Invalid sample type: 'invalid_type'",
            "experiment_id": "Line 3: Mismatch in 'experiment_id' value",
            "sample_id": "Line 3: Mismatch in 'sample_id' value",
            "barcode": "Line 2: Bad 'barcode' name 'bad'; expected a name like 'barcode01'",
            "internal_barcode": "Line 2: Bad 'internal_barcode' name 'bad'; expected a name like 'internal01'",
            "external_barcode": "Line 2: Bad 'external_barcode' name 'bad'; expected a name like 'external01'",
            "rapid_barcode": "Line 2: Bad 'rapid_barcode' name 'bad'; expected a name like 'barcode01'",
            "fip_barcode": "Line 2: Bad 'fip_barcode' name 'bad'; expected a name like 'FIP01'",
            "duplicate_barcode": "Line 3: Duplicate barcode: 'barcode01'",
            "duplicate_alias": "Line 3: Duplicate alias: 'alias'",
        }

        for filename, message in expected_messages.items():
            with self.assertRaisesRegex(
                SampleSheetParseError,
                "^" + re.escape(message) + "$",
                msg="Test file: " + filename,
            ):
                load_sample_sheet_csv(sample_sheet_csv_path("bad_records", filename))

    def test_no_error_on_unknown_fields(self):
        sample_sheet = load_sample_sheet_csv(
            sample_sheet_csv_path("bad_column_names", "invalid_columns"),
            exception_on_unknown_field=False,
        )

        # Should have an empty sample sheet, since no entries
        self.assertFalse(sample_sheet)


if __name__ == "__main__":
    unittest.main()
