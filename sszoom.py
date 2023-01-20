#!/usr/bin/env python3


import pathlib
import pandas as pd
import readline
from rich.prompt import Prompt
from rich import print
import sys
import tomli

banner = '''
[bold purple]
███████ ███████ ███████  ██████   ██████  ███    ███ 
██      ██         ███  ██    ██ ██    ██ ████  ████ 
███████ ███████   ███   ██    ██ ██    ██ ██ ████ ██ 
     ██      ██  ███    ██    ██ ██    ██ ██  ██  ██ 
███████ ███████ ███████  ██████   ██████  ██      ██ 
                                                     
               Version 0.0 + DEV

'''


def main(argv):

    print(banner)

    #############################################
    ## FILE/PATH HANDLING
    #############################################

    # TODO: create the .sszoom and log folders, if they don't exist already. Probably a first time setup thing.

    # Build dictionary for all file paths
    paths = {}
    # Make paths
    paths['SETTINGS'] = pathlib.Path.home() / '.sszoom' / 'settings.toml'
    paths['HOSTS'] = pathlib.Path.home() / '.sszoom' / 'hosts.csv'
    paths['CREDENTIALS'] = pathlib.Path.home() / '.sszoom' / 'credentials.csv'

    # Open all the files needed
    df_hosts = pd.read_csv(paths['HOSTS'], index_col=0, keep_default_na=False)
    df_creds = pd.read_csv(paths['CREDENTIALS'], index_col=0)


    #############################################
    ## 
    #############################################

    # loop to get down to single hostname
    while True: 

        print('')
        k_input = Prompt.ask('[bold cyan]Enter hostname (full or partial) or previous # number')
        # allows up arrow to get last entry entered
        readline.add_history(k_input) 

        # First, check if a hostname matches exactly 
        ## TODO REMOVE df_filter = df_hosts[df_hosts.index.isin([k_input])]
        df_filter = df_hosts[df_hosts.index == k_input]
        # Match found, we can exit loop with the hostname
        if not df_filter.empty:
            print(f"Hostname found of {df_filter.index[0]}")
            # TODO variable return
            break

        
        # Filter down on rows that contain (or equal) the user input
        df_hostmatches = df_hosts[df_hosts.index.str.contains(k_input)]
        name_matches_count = df_hostmatches.sum()

        print (df_hostmatches)


if __name__== '__main__':
    main(sys.argv[1:])