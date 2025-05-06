# Real-time Wind Flow Visualization Desktop Wallpaper

Display real-time wind flow data as your desktop background, allowing you to monitor wind direction and speed at any time.

## Project Status

✅ **Implemented**: This project has successfully implemented the functionality to display real-time wind flow data as a desktop background. The program automatically loads the wind flow page from Earth Nullschool, displays it as a desktop background, and refreshes periodically to maintain data accuracy.

## Project Overview

This project creates a dynamic desktop background that displays real-time wind flow data. The program uses PyQt5's WebEngine to directly load the Earth Nullschool wind visualization page, preserving all animations and interactive effects, allowing you to intuitively understand wind direction and speed across the globe.

### Features

- **Real-time Data**: Fetches the latest wind flow data directly from Earth Nullschool
- **Dynamic Display**: Preserves the original webpage's animation effects, showing real-time changes in wind direction and speed
- **Automatic Updates**: Refreshes the page periodically to ensure data is always up-to-date
- **Seamless Integration**: Displays as a desktop background without affecting desktop icons and other applications
- **Simple Controls**: Uses keyboard shortcuts to control the program (ESC to exit, F5 to refresh, F1 to show/hide status)

### Technical Implementation

This project is implemented using the following technologies:

- **PyQt5**: Creates the desktop application
- **PyQtWebEngine**: Loads and displays web content
- **JavaScript**: Automatically processes the webpage, selects wind flow options and hides unnecessary elements
- **Python**: Implements program logic and control flow

## Usage

1. Run the `run_live_wallpaper.bat` batch file
2. The program will automatically install necessary dependencies (PyQt5, PyQtWebEngine)
3. After startup, the program will automatically load the Earth Nullschool wind flow page
4. Once the page is loaded, the program will automatically select the wind flow option and hide unnecessary elements
5. The program will refresh the page periodically to ensure the latest data is displayed

### Controls

- Press `ESC` to exit the program
- Press `F5` to refresh the page
- Press `F1` to show/hide the status label

## System Requirements

- Windows 10/11
- Python 3.6+
- Internet connection (to access Earth Nullschool)

## File Structure

- `run_live_wallpaper.bat`: Main run file to start the program
- `src/wind_flow_live_wallpaper.py`: Main program file that implements the wind flow live wallpaper functionality
- `src/assets/icon.png`: Program icon
- `src/scripts/`: Contains other auxiliary scripts and batch files

## Notes

- The program requires an internet connection to fetch real-time data
- Initial loading may take some time, please be patient
- If you encounter any issues, check the `wind_flow_live_wallpaper.log` file for detailed information

## License

This project is licensed under the MIT License.
