# flightradar-to-g1000

This project converts flight data from a CSV file into Garmin G1000 flight log CSV format. One use for this project is for converting FlightRadar ADSB CSVs into the G1000 format for loading into ForeFlight for review.

## Requirements

- Python 3.12 or higher
- pandas library
- uv package manager

## Installation

Install the required dependencies using uv:

```bash
uv sync
```

## Usage

To convert a CSV file to Garmin G1000 format, run the following command:

```bash
uv run flightradar_to_g1000.py <input_file_path>
```

Replace `<input_file_path>` with the path to your input CSV file.

## Example

```bash
uv run flightradar_to_g1000.py sample_data/source/38e7ef15.csv
```

The converted file will be saved with a `_g1000` suffix before the file extension.

## License

This project is licensed under the MIT License.
