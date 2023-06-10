# auto-forecasting
GitHub workflow for automatic solar power forecasting

This repository contains a machine learning pipeline that predicts the daily yield of a solar power plant. The pipeline is set up to run automatically every Monday at midnight and can be triggered manually using GitHub Actions. It fetches the data from Firebase, preprocesses it, trains an LSTM model, evaluates its performance, and uploads the predicted data back to Firebase.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Scripts](#scripts)
- [License](#license)

## Requirements

- Python 3.x
- `pip` package manager
- GitHub Actions (configured in the repository)

## Installation

1. Clone the repository:

   `git clone https://github.com/saadz-khan/auto-forecasting.git`


2. Navigate to the project directory:
   `cd auto-forecasting`


3. Install the required Python packages:

    `pip install -r requirements.txt`


## Usage

The pipeline is configured to run automatically every Monday at midnight using GitHub Actions. If you wish to trigger the pipeline manually, follow these steps:

1. Go to the "Actions" tab of your GitHub repository.
2. Click the "Run workflow" button on the right side of the screen.
3. Select the branch where the workflow is configured and click the "Run workflow" button.

## Scripts

- `pipeline.yml` - GitHub Actions workflow configuration file.
- `firebase_add.py` - Script to import 4 weeks of data from JSON files to Firebase Realtime Database.
- `firebase.py` - Script to download data from Firebase Realtime Database and convert it to CSV files.
- `preprocessing.py` - Script to preprocess the downloaded data and create a final CSV file.
- `training_eval.py` - Script to train and evaluate the LSTM model and make predictions.
- `firebase_upload.py` - Script to upload the predicted data back to Firebase Realtime Database.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

