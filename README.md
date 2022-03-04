# Phishermans-Enemy
![python version](https://img.shields.io/badge/Python-%3D%3D%203.9.7-blue.svg?style=for-the-badge&logo=Python)
Phisherman's Enemy is a tool developed in Python with the aim of identifying Phishing sites through the use of Machine Learning. This tool was designed for Windows.
![Report](https://user-images.githubusercontent.com/56866602/156691591-472a1377-19ba-4334-b1eb-5d9bc472172e.gif)
# Features!
 -	Input a URL and predict if it is a Phishing link based on a dataset of known Phishing sites.
 -	Graphical User Interface for user friendliness
 -	Command Line Interface also available
 -	Output is exported as CSV
 -	Flask Server for dynamically displaying content in the report
 -	Visualization in report

### Installation

Phisherman's Enemy requires [Python](https://www.python.org/) v3.9.7 to run, as well as the tools it was built upon. (see config directory)
```sh
$ git clone https://github.com/BaconPotatoCat/Phishermans-Enemy/
$ cd ./Phishermans-Enemy/Config
$ pip install -r requirements.txt
```
![installation](https://user-images.githubusercontent.com/56866602/156617349-a6524ed8-f718-45a0-ac60-b2a9ed3f27df.gif)

### Usage
```bash
# Phisherman's Enemy GUI
$ python Phishermans_Enemy_GUI.py
```
![GUI](https://user-images.githubusercontent.com/56866602/156621804-241ea567-3341-4df0-a403-a683edeb9d4d.gif)
```
# Phisherman's Enemy CLI
$ python Phishermans_Enemy.py -u <URL> -m <MODEL>
$ python Flask_Report.py
# Example
$ python Phishermans-Enemy.py -u https://www.phishingsite.com -m 3
$ python Flask_Report.py
```
### License

This project is under the MIT License.
