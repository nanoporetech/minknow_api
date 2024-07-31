"""
Load information from a sample sheet csv

Produce a list of extracted information, which includes:
    - `ProtocolRunUserInfo` protobuf message, suitable for passing to the `start_protocol` RPC
    -
"""

import csv
import re
from collections import Counter
from typing import Any, Mapping, MutableMapping, NamedTuple, Optional, Sequence

from minknow_api.protocol_pb2 import BarcodeUserData


# Error raised when the sample sheet cannot be parsed
class SampleSheetParseError(Exception):
    pass


# Some types that are used:


# `Record` contains one record read from the CSV file
# Since it's read with a `csv.DictReader`, it's a mapping
Record = Mapping[str, str]

# `ParsedData` contains the data for one hardware position, read from the sample sheet, and normalised to the same
# general arrangement as is required by MinKNOW
ParsedData = Mapping[str, Any]

# `ParsedDataDict` contains all the data parsed from a sample sheet
# The key is some hardware identifier (the `position_id` or `flow_cell_id`, if specified).  It is just used to look up
# information for a given hardware position
# The value is the information read from the sample sheet
ParsedDataDict = MutableMapping[Optional[str], ParsedData]

KNOWN_FIELDNAMES = {
    "flow_cell_id",
    "position_id",
    "sample_id",
    "experiment_id",
    "alias",
    "type",
    "barcode",
    "internal_barcode",
    "external_barcode",
}


# Check that only expected fieldnames are present in sample sheet
def check_fieldnames(fieldnames: Sequence[str]) -> None:
    if not fieldnames:
        raise SampleSheetParseError("No columns in sample sheet")

    # Check that all fieldnames are unique
    if len(set(fieldnames)) < len(fieldnames):
        counts = Counter(fieldnames)
        duplicate_fieldnames = [k for k, v in counts.items() if v > 1]
        raise SampleSheetParseError(
            "Duplicate columns in sample sheet: "
            + ", ".join("'{}'".format(name) for name in duplicate_fieldnames)
        )

    # Position fields
    # Must have exactly one of `flow_cell_id` or `position_id`, but not both
    has_flow_cell_id = "flow_cell_id" in fieldnames
    has_position_id = "position_id" in fieldnames
    if (not has_flow_cell_id and not has_position_id) or (
        has_flow_cell_id and has_position_id
    ):
        raise SampleSheetParseError(
            "Invalid position information in sample sheet. Must have exactly one of 'flow_cell_id' and 'position_id'"
        )

    # Check the barcode column names
    # Should have at most one of the following sets:
    # { 'barcode' },
    # { 'internal_barcode', 'external_barcode' },
    #
    # If any of the above sets of barcode columns names are present:
    #   - An `alias` column must be present
    #   - A `type` column may be present
    #
    # Otherwise (if none of the above sets of barcode column names are present):
    #   - There must not be an `alias` column
    #   - There must not be a `type` column
    #
    has_barcoding_columns = False

    all_barcoding_column_names = {
        "barcode",
        "internal_barcode",
        "external_barcode",
    }
    barcoding_column_name_sets = [
        {"barcode"},
        {"internal_barcode", "external_barcode"},
    ]
    for barcoding_column_name_set in barcoding_column_name_sets:
        if any(name in fieldnames for name in barcoding_column_name_set):
            if has_barcoding_columns:
                # Found barcoding column names, but we already have barcoding columns
                raise SampleSheetParseError(
                    "Conflicting barcode column names: "
                    + ", ".join(
                        "'{}'".format(name)
                        for name in fieldnames
                        if name in all_barcoding_column_names
                    )
                )

            if all(name in fieldnames for name in barcoding_column_name_set):
                has_barcoding_columns = True
            else:
                # Have some but not all barcoding columns
                missing_column_names = barcoding_column_name_set - set(fieldnames)
                raise SampleSheetParseError(
                    "Missing barcoding column names: "
                    + ", ".join("'{}'".format(name) for name in missing_column_names)
                )

    if has_barcoding_columns:
        # Must have alias
        if "alias" not in fieldnames:
            raise SampleSheetParseError("Missing 'alias' column")

    else:
        # No barcoding info; must not have 'type' or 'alias' column
        for col in {"alias", "type"}:
            if col in fieldnames:
                raise SampleSheetParseError(
                    "'{}' column supplied, but no other barcode information in sample sheet".format(
                        col
                    )
                )

    # Must have something to set in the ProtocolRunUserInfo (otherwise, why are we bothering)
    if not any(col in fieldnames for col in {"sample_id", "experiment_id", "alias"}):
        raise SampleSheetParseError(
            "Sample sheet contains no user info. "
            + "Should contain 'sample_id', 'experiment_id' or some barcode information"
        )

    return fieldnames


# Find the key to use for the data in the current line
#   - If 'position_id' is supplied, look up by position id
#   - Otherwise, `flow_cell_id` must have been supplied, look up by flow cell id
def get_key(record: Record) -> str:
    # We checked above that we had exactly one of `position_id` and `flow_cell_id` in the record
    # So one must be in the record, and the other must not be
    if ("position_id" in record) == ("flow_cell_id" in record):
        raise ValueError(
            "exactly one of 'position_id' and 'flow_cell_id' must be specified in the sample sheet"
        )

    return record.get("position_id") or record.get("flow_cell_id")


# Convert a sample type string to a sample type
def to_sample_type(type_str: Optional[str], line_num: int) -> Optional[int]:
    sample_type_lookup = {
        None: None,
        "test_sample": BarcodeUserData.SampleType.test_sample,
        "positive_control": BarcodeUserData.SampleType.positive_control,
        "negative_control": BarcodeUserData.SampleType.negative_control,
        "no_template_control": BarcodeUserData.SampleType.no_template_control,
    }
    if type_str in sample_type_lookup:
        return sample_type_lookup[type_str]
    else:
        raise SampleSheetParseError(
            "Line {}: Invalid sample type: '{}'".format(line_num, type_str)
        )


# "passenger info" are fields of extra context per barcode. We treat any unknown fields
# in barcode related rows as passenger info
def extract_passenger_info(record: Record) -> Mapping[str, str]:
    return {k: v for k, v in record.items() if k not in KNOWN_FIELDNAMES}


# The per-barcode information
BarcodeInfo = NamedTuple(
    "BarcodeInfo",
    [
        ("barcode_name", str),
        ("barcode_name_internal", str),
        ("alias", str),
        ("type", Optional[int]),
        ("passenger_info", Mapping[str, str]),
    ],
)


# Parse and normalise one record
def parse_record(parsed_data: ParsedDataDict, record: Record, line_num: int):

    # Check that there is only one `experiment_id` across all entries on the sample sheet
    if parsed_data:
        experiment_id = next(iter(parsed_data.values())).get("experiment_id")
        if record.get("experiment_id") != experiment_id:
            raise SampleSheetParseError(
                "Line {}: Mismatch in 'experiment_id' value".format(line_num)
            )

    key = get_key(record)

    if key not in parsed_data:
        parsed_data[key] = {}

    data = parsed_data[key]

    # Check basic fields that should be the same across all keys
    # NB:
    #   - We have already checked `experiment_id` above
    #   - Logically can't have a mismatch in `flow_cell_id` or `position_id` since they are used as the key, and at most
    #     one can be specified
    # No harm in checking again here, though..
    #
    for col in {"flow_cell_id", "position_id", "sample_id", "experiment_id"}:
        if col in record:
            if col in data:
                # Check field matches with existing data
                if data[col] != record[col]:
                    raise SampleSheetParseError(
                        "Line {}: Mismatch in '{}' value".format(line_num, col)
                    )
            else:
                # Add the new data
                data[col] = record[col]

    # Handle the barcoding fields
    # Barcoding data is a map of `some barcode id` -> `alias / type`

    if "barcode_info" not in data:
        data["barcode_info"] = {}

    if "barcode" in record:
        if not re.match(r"barcode(\d{2})", record["barcode"]):
            raise SampleSheetParseError(
                "Line {}: Bad 'barcode' name '{}'; ".format(line_num, record["barcode"])
                + "expected a name like 'barcode01'"
            )

        barcode_name = record["barcode"]
        barcode_name_internal = None
        barcode_key = barcode_name

    elif ("internal_barcode" in record) and ("external_barcode" in record):
        external_barcode = record["external_barcode"]
        internal_barcode = record["internal_barcode"]

        if not re.match(r"internal(\d{2})", internal_barcode):
            raise SampleSheetParseError(
                "Line {}: Bad 'internal_barcode' name '{}'; ".format(
                    line_num, internal_barcode
                )
                + "expected a name like 'internal01'"
            )
        if not re.match(r"external(\d{2})", external_barcode):
            raise SampleSheetParseError(
                "Line {}: Bad 'external_barcode' name '{}'; ".format(
                    line_num, external_barcode
                )
                + "expected a name like 'external01'"
            )

        barcode_name = external_barcode
        barcode_name_internal = internal_barcode
        barcode_key = (external_barcode, internal_barcode)
    else:
        # No barcode data
        # Nothing more to do for this line
        return

    # Check for duplicate barcode name
    if barcode_key in data["barcode_info"]:
        raise SampleSheetParseError(
            "Line {}: Duplicate barcode: '{}'".format(line_num, barcode_key)
        )

    # Check for duplicate alias for the same hardware position
    for val in data["barcode_info"].values():
        if val.alias == record["alias"]:
            raise SampleSheetParseError(
                "Line {}: Duplicate alias: '{}'".format(line_num, record["alias"])
            )

    passenger_info = extract_passenger_info(record)

    data["barcode_info"][barcode_key] = BarcodeInfo(
        barcode_name=barcode_name,
        barcode_name_internal=barcode_name_internal,
        # We know the alias exists because we checked in `check_fieldnames`
        alias=record["alias"],
        type=to_sample_type(record.get("type"), line_num),
        passenger_info=passenger_info,
    )


# Convert BarcodeInfo to BarcodeUserData
def make_barcode_user_data(barcode_info: BarcodeInfo) -> BarcodeUserData:
    barcode_user_data = BarcodeUserData()
    if barcode_info.barcode_name:
        barcode_user_data.barcode_name = barcode_info.barcode_name
    if barcode_info.barcode_name_internal:
        barcode_user_data.barcode_name_internal = barcode_info.barcode_name_internal
    if barcode_info.alias:
        barcode_user_data.alias = barcode_info.alias
    if barcode_info.type:
        barcode_user_data.type = barcode_info.type
    if barcode_info.passenger_info:
        barcode_user_data.passenger_info.update(barcode_info.passenger_info)
    return barcode_user_data


def convert_barcode_info(
    barcode_info: BarcodeInfo,
) -> Optional[Sequence[BarcodeUserData]]:
    if barcode_info:
        return [make_barcode_user_data(val) for val in barcode_info.values()]
    else:
        return None


ParsedSampleSheetEntry = NamedTuple(
    "ParsedSampleSheetEntry",
    [
        ("flow_cell_id", Optional[str]),
        ("position_id", Optional[str]),
        ("sample_id", Optional[str]),
        ("experiment_id", Optional[str]),
        ("barcode_info", Sequence[BarcodeUserData]),
    ],
)


def convert_parsed_data(parsed_data_dict: ParsedDataDict):
    return [
        ParsedSampleSheetEntry(
            flow_cell_id=val.get("flow_cell_id"),
            position_id=val.get("position_id"),
            sample_id=val.get("sample_id"),
            experiment_id=val.get("experiment_id"),
            barcode_info=convert_barcode_info(val.get("barcode_info")),
        )
        for val in parsed_data_dict.values()
    ]


# filename csv file name to load
def load_sample_sheet_csv(filename):
    # Dictionary containing information per hardware position
    parsed_data_dict = {}

    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        check_fieldnames(fieldnames=reader.fieldnames)

        for record in reader:
            parse_record(parsed_data_dict, record, reader.line_num)

    return convert_parsed_data(parsed_data_dict)
