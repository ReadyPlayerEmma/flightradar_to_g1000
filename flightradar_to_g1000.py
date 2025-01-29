#!/usr/bin/env python

import argparse
import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def convert_to_g1000_format(input_file_path, output_dir=None):
    """Converts a CSV file with flight data into Garmin G1000 flight log CSV format.

    Args:
        input_file_path (str): Path to the input CSV file.
        output_dir (str): Optional directory to save the converted CSV file.

    Returns:
        None

    The output file name will have a '_g1000' suffix before the file extension,
    by default placed next to the input file unless output_dir is provided.
    """
    try:
        # Convert the string path to a Path object
        input_path = Path(input_file_path)

        if not input_path.is_file():
            logging.error(f"Input file does not exist: {input_path}")
            return

        # Construct output path
        # If output_dir is set, place the file there; otherwise, place in the same dir as input.
        if output_dir:
            output_dir_path = Path(output_dir)
            output_dir_path.mkdir(parents=True, exist_ok=True)  # Create dirs if needed
            output_file_path = (
                output_dir_path / f"{input_path.stem}_g1000{input_path.suffix}"
            )
        else:
            output_file_path = input_path.with_name(
                f"{input_path.stem}_g1000{input_path.suffix}"
            )

        # Load the input CSV file
        data = pd.read_csv(input_path)

        # Define the Garmin G1000 flight log headers
        g1000_headers = [
            "Lcl Date",
            "Lcl Time",
            "UTCOfst",
            "AtvWpt",
            "Latitude",
            "Longitude",
            "AltB",
            "BaroA",
            "AltMSL",
            "OAT",
            "IAS",
            "GndSpd",
            "VSpd",
            "Pitch",
            "Roll",
            "LatAc",
            "NormAc",
            "HDG",
            "TRK",
            "volt1",
            "FQtyL",
            "FQtyR",
            "E1 FFlow",
            "E1 FPres",
            "E1 OilT",
            "E1 OilP",
            "E1 MAP",
            "E1 RPM",
            "E1 CHT1",
            "E1 CHT2",
            "E1 CHT3",
            "E1 CHT4",
            "E1 EGT1",
            "E1 EGT2",
            "E1 EGT3",
            "E1 EGT4",
            "AltGPS",
            "TAS",
            "HSIS",
            "CRS",
            "NAV1",
            "NAV2",
            "COM1",
            "COM2",
            "HCDI",
            "VCDI",
            "WndSpd",
            "WndDr",
            "WptDst",
            "WptBrg",
            "MagVar",
            "AfcsOn",
            "RollM",
            "PitchM",
            "RollC",
            "PichC",
            "VSpdG",
            "GPSfix",
            "HAL",
            "VAL",
            "HPLwas",
            "HPLfd",
            "VPLwas",
        ]

        # Check if 'Position' exists before splitting
        if "Position" not in data.columns:
            logging.error("The input CSV is missing the 'Position' column.")
            return

        # Split Position column into Latitude and Longitude
        data[["Latitude", "Longitude"]] = data["Position"].str.split(",", expand=True)

        # Create a new DataFrame
        g1000_log = pd.DataFrame(columns=g1000_headers)

        # Populate columns
        g1000_log["Lcl Date"] = pd.to_datetime(data["UTC"]).dt.strftime("%Y-%m-%d")
        g1000_log["Lcl Time"] = pd.to_datetime(data["UTC"]).dt.strftime("%H:%M:%S")

        # Convert columns to float/int as appropriate, ignoring errors in case of non-numeric
        g1000_log["Latitude"] = pd.to_numeric(data["Latitude"], errors="coerce")
        g1000_log["Longitude"] = pd.to_numeric(data["Longitude"], errors="coerce")
        g1000_log["AltMSL"] = pd.to_numeric(data["Altitude"], errors="coerce")
        g1000_log["GndSpd"] = pd.to_numeric(data["Speed"], errors="coerce")
        g1000_log["TRK"] = pd.to_numeric(data["Direction"], errors="coerce")

        # Default values
        g1000_log["BaroA"] = 29.92
        g1000_log["volt1"] = 24.0

        # Fill any remaining NaN fields with empty strings
        g1000_log.fillna("", inplace=True)

        # Save the converted CSV
        g1000_log.to_csv(output_file_path, index=False)
        logging.info(f"Converted file saved to: {output_file_path}")

    except pd.errors.EmptyDataError:
        logging.error(f"No data in file: {input_file_path}")
    except Exception as e:
        logging.error(f"An error occurred while converting {input_file_path}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert FlightRadar24 ADS-B CSV files into Garmin G1000 flight log CSV format."
    )
    parser.add_argument(
        "input_files",
        nargs="+",
        help="One or more input CSV files to convert (allows shell globbing).",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=None,
        help="Optional directory to save converted CSV files. Default: same directory as input.",
    )
    args = parser.parse_args()

    # Iterate through all input files
    for input_file in args.input_files:
        convert_to_g1000_format(input_file, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
