#!/usr/bin/env python

import pandas as pd
import os
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def convert_to_g1000_format(input_file_path):
    """
    Converts a CSV file with flight data into Garmin G1000 flight log CSV format.

    The output file name will have a '_g1000' suffix before the file extension.

    Args:
        input_file_path (str): Path to the input CSV file.

    Returns:
        None
    """
    try:
        # Define the output file path by adding '_g1000' before the file extension
        base, ext = os.path.splitext(input_file_path)
        output_file_path = f"{base}_g1000{ext}"

        # Load the input CSV file
        data = pd.read_csv(input_file_path)

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

        # Split Position column into Latitude and Longitude
        data[["Latitude", "Longitude"]] = data["Position"].str.split(",", expand=True)

        # Map the data into the required columns, leaving others empty
        g1000_log = pd.DataFrame(columns=g1000_headers)
        g1000_log["Lcl Date"] = pd.to_datetime(data["UTC"]).dt.strftime(
            "%Y-%m-%d"
        )  # Date in YYYY-MM-DD format
        g1000_log["Lcl Time"] = pd.to_datetime(data["UTC"]).dt.strftime(
            "%H:%M:%S"
        )  # Time in HH:MM:SS format
        g1000_log["Latitude"] = data["Latitude"].astype(float)
        g1000_log["Longitude"] = data["Longitude"].astype(float)
        g1000_log["AltMSL"] = data["Altitude"].astype(
            int
        )  # Assign altitude values to AltMSL
        g1000_log["GndSpd"] = data["Speed"].astype(int)  # Ground speed in knots
        g1000_log["TRK"] = data["Direction"].astype(int)  # Track (heading in degrees)

        # Fill default or empty values for other fields
        g1000_log["BaroA"] = 29.92  # Default barometric pressure (inHg)
        g1000_log["volt1"] = 24.0  # Default voltage (example)
        g1000_log.fillna("", inplace=True)  # Fill remaining fields with empty values

        # Save the reformatted data to the specified output file
        g1000_log.to_csv(output_file_path, index=False)

        logging.info(f"Converted file saved to: {output_file_path}")

    except FileNotFoundError:
        logging.error(f"File not found: {input_file_path}")
    except pd.errors.EmptyDataError:
        logging.error(f"No data: {input_file_path}")
    except KeyError as e:
        logging.error(f"Missing column in input file: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_path>")
    else:
        input_file = sys.argv[1]
        convert_to_g1000_format(input_file)
