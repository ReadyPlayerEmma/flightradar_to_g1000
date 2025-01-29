# flightradar_to_g1000

This Python project provides a CLI to convert ADSB data from a FlightRadar24 CSV file into Garmin G1000 flight log CSV format. One use for this project is for converting the ADSB CSVs into the G1000 format for loading into ForeFlight for review.

## Requirements

- Python 3.12 or higher
- pandas library (automatically installed if you use `pip install flightradar-to-g1000`)
- uv package manager (only required if you build from source)

## Installation

### From PyPi

```bash
pip install flightradar-to-g1000
```
This will install both the library and a CLI command called `flightradar-to-g1000`.

### From Source

Clone the repository:

```bash
git clone https://github.com/ReadyPlayerEmma/flightradar_to_g1000.git
```

Make sure you have uv installed, and then use it to install the required dependencies:

```bash
uv sync
```

Build the package and install it:

```bash
uv build
pip install dist/<filename>.whl 
```

## Usage

To convert a CSV file to Garmin G1000 format, run the following command:

```bash
flightradar-to-g1000 <input_file_path>
```

Replace `<input_file_path>` with the path to your input CSV file.

For more options, see the help output:

```bash
flightradar-to-g1000 --help
```

## Example

```bash
flightradar-to-g1000 sample_data/source/38e7ef15.csv
```

The converted file will be saved with a `_g1000` suffix before the file extension.

## License

This project is licensed under the MIT License.
