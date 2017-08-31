# Pass_Pwned
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/acd3694ebf3048da830bbfd861b3af6f)](https://www.codacy.com/app/sehlat57/pass_pwned?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sehlat57/pass_pwned&amp;utm_campaign=Badge_Grade)
[![Python3](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203%2C6-blue.svg)](https://www.python.org/)
[![requests](https://img.shields.io/badge/requests-2.18.4-yellowgreen.svg)](http://docs.python-requests.org/en/master/)
## Demo:
![](https://github.com/sehlat57/instalike_bot/blob/master/src.gif)
## Description
On august 2017 Troy Hunt web security expert from Australia introduced a new service **"Pwned Passwords"**  on his [website](https://haveibeenpwned.com/Passwords) that provides opportunity to check passwords against those obtained from previous data breaches (more than 320+ million passwords).

This python script allows you to check if password (or list of passwords) in the HIBP data base.
It generates a hash of password with SHA1 algorithm and compares it to the other hashes of passwords in HIBP DB by using [API](https://haveibeenpwned.com/API/v2).

## Other options
You can also check if password was **PWNED** by:

*  Passing password or hash of password directly to the HIBP [form](https://haveibeenpwned.com/Passwords). But please think twice before entering your sensitive information...anywhere actually...and consider to use any other tools for generating hash of the password than online services
*  By downloading **Pwned Passwords list** (5GB+) and check it offline. Download link (torrent is also available) can be found on website
*  By using [API](https://haveibeenpwned.com/API/v2) provided py Troy Hunt



## Installation

- You need **Python 3** to be installed and linux or OSx

---
1. Clone/Download this repo
```bash
$ git clone https://github.com/sehlat57/pass_pwned.git
```
1. Install the dependencies with [pip](https://pypi.python.org/pypi/pip)
```bash
$ pip3 install -r requirements.txt
```

## Usage
1. Navigate to the directory with ```cd```
```bash
$ cd pass_pwned
```
2. Run script
* for single password check:
```bash 
$ python3 pass_pwned.py -p
```
* for several passwords create the txt file, write passwords to it. Split up passwords with comma (pass1, pass2, ... etc.):
```bash 
$ python3 pass_pwned.py -f PATH_TO_THE_FILE
```
