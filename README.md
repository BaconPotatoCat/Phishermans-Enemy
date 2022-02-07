# Phishermans-Enemy
![python version](https://img.shields.io/badge/Python-%3D%3D%203.9.7-blue.svg?style=for-the-badge&logo=Python)

Phisherman's Enemy is a tool developed in Python with the aim of identifying Phishing sites through the use of Machine Learning. This tool was designed for Windows and Google Chrome.

# Features!
 -    Input a URL and predict if it is a Phishing link based on a dataset of known Phishing sites.

### Installation

Phisherman's Enemy requires [python](https://www.python.org/) v3.9.7 to run, as well as the tools it was built upon. (see config directory)
```sh
$ git clone https://github.com/BaconPotatoCat/Phishermans-Enemy/
$ cd ./Phishermans-Enemy/Config
$ python3 setup.py
```

### Usage
```bash
# Phisherman's Enemy
$ python Phishermans-Enemy.py -u <url>
# Example
$ python Phishermans-Enemy.py -u https://www.phishingsite.com
```
### License

This project is under the MIT License.
