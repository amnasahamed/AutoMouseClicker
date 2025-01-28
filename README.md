# Auto Mouse Clicker

Auto Mouse Clicker is a Python-based application that automates mouse clicks at specified locations and intervals. This tool can be used for repetitive clicking tasks, saving time and effort.

## Features
- Supports multiple click locations.
- Allows users to set intervals for each click.
- Runs in the background and performs actions as scheduled.
- Lightweight and easy to use.

## Requirements
To use the script or build the executable, ensure you have the following installed:
- Python 3.13 or later
- Required Python libraries (see `requirements.txt`)

## Installation and Usage

### 1. Running the Script
To run the Python script directly:
1. Install Python from [python.org](https://www.python.org/).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python automouse.py
   ```

### 2. Using the Executable
An executable version of the application is available for those who don't have Python installed.

#### **Location of Executable File**
The executable file is located in the `dist/` folder. To use it:
1. Navigate to the `dist` folder:
   ```cmd
   cd dist
   ```
2. Run the executable:
   ```cmd
   automouse.exe
   ```

You can distribute this file to others who can run it on their Windows machines without installing Python.

## Building the Executable
To build the executable from the script:
1. Ensure Python and `PyInstaller` are installed:
   ```bash
   pip install pyinstaller
   ```
2. Build the executable:
   ```bash
   pyinstaller --onefile automouse.py
   ```
3. The executable will be generated in the `dist/` directory.

## How to Use
1. Open the application (either by running the script or using the executable).
2. Select the locations to click by specifying the screen coordinates.
3. Set the time interval for each click.
4. Minimize the application, and the clicks will be executed as per the schedule.

## File Structure
```
AutoMouseClicker/
│
├── automouse.py          # Python script for the application
├── dist/                 # Contains the generated executable file
│   └── automouse.exe     # Executable file
├── build/                # Temporary build files created by PyInstaller
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .gitignore            # Git ignore file
```

## Contributing
Feel free to fork the repository and make contributions. If you encounter any issues, please open an issue on the GitHub repository.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or suggestions, contact:
- **Name:** Amnas Ahamed
- **Email:** amnasahmd@gmail.com
