# SSZOOM

SSZOOM is a Python-based enhacement to any SSH utility that adds:
- Organization of hostname/ip's, and username/passwords, based on CSV
- Quick selection of the right IP based on simple hostname searching
- Quick selection of the right username/password to use
- Logging each SSH session to file
- Remembering common SSH parameters (like allowing "diffie-hellman-group1-sha1", etc)

# Requirements

Currently, SSZOOM has only been tested on MacOS. It will most certainly work on other 'nix based operating systems (Ubuntu, even WSL on Windows). Direct use in Windows (CMD, PowerShell) still needs to be tested.

This has been testing on Python 3.10, but it will likely work on earlier Python3.x versions as well.

# Setup

Clone this repository with:
```
git clone https://github.com/JeffTadashi/sszoom.git
```

Create the following folders:
(in the near future, the script will likely create these folders. That feature TBD)
```
mkdir ~/.sszoom
mkdir ~/.sszoom/log
```

In the `/example` folder in the repo, there are three files: `settings.toml`, `credentials.csv`, and `hosts.csv`. Copy these files into the `~/.sszoom` folder, and then modify them to your needs:
- `settings.toml`: All global settings
- `hosts.csv`: All hostname-to-IP mappings. Optionally, fill out the tag field if its useful for viewing the searched inventory.
- `credentials.csv`: All username-to-IP mappings. They are called by the script by typing the Alias field (not the username itself)

Install all python requirements (use virtual environment or `sudo` as needed):
```
python3 -m pip install -r requirements.txt
```

# Run

Simply run the script as:
```
python3 sszoom.py
```