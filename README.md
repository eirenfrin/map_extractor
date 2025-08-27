# Map extractor 🗺️
A tool for capturing map fragments and joining them into a single .png file for offline viewing.

## Disclaimer 🚩
This tool is intended for personal use in offline settings only. It is tailored for use with the [freemap.sk](https://www.freemap.sk) map, which is based on [OpenStreetMap](https://www.openstreetmap.org) (OSM) data licensed under the [ODbL](https://opendatacommons.org/licenses/odbl/). The users are encouraged to visit [freemap.sk](https://www.freemap.sk) whenever possible, and utilize this tool only when necessary. The author is not responsible for any misuse of this tool or violations of freemap.sk or OSM terms of use.

## Overview📋
Map extractor offers three main functionalities: 
- Collection of coordinates of the map the user wants to save for offline referencing (outputs into `.json` file in `/boundaries` folder).
- Calculation of the target map area, its division into equal size fragments and automated screenshot taking (outputs screenshots as .png images in `/tiles` folder).
- Joining of individual screenshots into a single map (outputs the map as `.png` image into `/maps` folder).

## How it works 🛠️
Selenium web automation tool is used for interacting with the online map during coordinates collection and screenshot taking. 

![Overview of map processing and tiles calculation.](/pics/map_extractor.drawio.svg)

The resulting map is always rectangular. The main steps of coordinate processing are shown on the diagram, and the tool's internal workings are summarized below:

1. The user marks views, or fragments of the map he wants to include by pressing keys <kbd>b</kbd> and <kbd>Enter</kbd>.
2. Central coordinates of each view (which are part of the URL) are then stored in a `.json` file.
3. Stored coordinates are then processed in the following way:
    - Minimum and maximum latitude and longitude values are identified.
    - Lower and upper bounds constitute the corners of the rectangular map.
    - Coordinates are converted to global pixels according to Web Mercator projection (EPSG:3857).
    - Width and height of rectangular map is calculated in pixel units.
    - Number of tiles in vertical and horizontal direction is calculated.
    - The final map is defined as pairs of starting (latitude, longitude) coordinates and number of shift to the right from the starting point at each latitude.
4. Automated screenshot taking happens by opening a new Chrome window at each latitude and shifting the view the calculated number of times; before each shift a screenshot is taken and stored as `capture_y_x`, where y, x are indices indicating its position on the final map.
5. Screenshots are stitched into a single .png map image according to their indices starting from top left corner.

## Installation and usage 🚀
To use the tool clone this repository and navigate to the project directory.
Create a virtual environment and install dependencies from `requirements.txt file`.
```
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
### CLI commands
The tool is managed from the terminal. Four modes are available.

**1\. Only store coordinates of map views**

To collect the fragments of the online map and store their coordinates in .json file use this command:
```
python main.py save-coordinates --name <YOUR_MAP_TITLE> --w <WINDOW_WIDTH> --h <WINDOW_HEIGHT> --z <ZOOM_LEVEL>
```
Folder `/boundaries` will be created (if not already existing) and a `<YOUR_MAP_TITLE>.json` file will be added.

**2\. Only take and store screenshots**

To process already stored coordinates and take screenshots run:
```
python main.py take-screenshots --name <YOUR_MAP_TITLE>
```
Coordinates will be taken from file `/boundaries/<YOUR_MAP_TITLE>.json.` Folder `/tiles/<YOUR_MAP_TITLE>` will be created (if not already existing) and `.png` screenshots of the map will be stored there.

**3\. Only stitch screenshots**

To join already taken screenshots into a single map run:
```
python main.py stitch-map --name <YOUR_MAP_TITLE>
```
Screenshots will be taken from directory `/tiles/<YOUR_MAP_TITLE>`. Folder `/maps` will be created (if not already existing) and `<YOUR_MAP_TITLE>.png` image will be stored there.

**4\. Run full process**

To collect desired map views, take screenshots and stitch the map all in one go run:
```
python main.py run-all --name <YOUR_MAP_TITLE> --w <WINDOW_WIDTH> --h <WINDOW_HEIGHT> --z <ZOOM_LEVEL>
```
Folders `/boundaries`, `/tiles/<YOUR_MAP_TITLE>`, `/maps` will be created (if not already existing) and artifacts will be stored in them accordingly.

**5\. Access help**

To view instructions for the available modes run:
```
python main.py -h
```
To view information about the flags of a specific mode run:
```
python main.py <MODE> -h
```
### Collecting map views (only in modes 1. and 4.)
When running the tool in modes 1. and 4. a Chrome window will appear briefly in the beginning. It is not meant for user interaction. This window opens just to calculate actual map element size given the window size entered by the user.

When a Chrome window opens the second time, you can begin marking views of the map. Just freely navigate the online map and, when you locate the view, press <kbd>b</kbd> on the keyboard to store the coordinates of the view. Continue marking views until you cover the desired map area. To exit and save press <kbd>Enter</kbd>. The coordinates will then appear in .json file.

## Important notes 🚩
The tool enforces the same map title for all artifacts (`.json` file, `.png` of the entire map, folder titles) related to the same map. If a folder or as file with the given name already exists, you can either delete/relocate it or choose a different map title.

When the tool takes screenshots, Chrome window will be opened automatically multiple times. This is expected behaviour, but it is vital not to interact with the windows, since an accidental scroll of the online map will affect final map image quality.


Copyright © 2025. All rights reserved.