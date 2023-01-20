#!/usr/bin/env python3


import pathlib
import pandas as pd
import readline
from rich.prompt import Prompt
from rich.table import Table
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
        k_input = Prompt.ask('[bold]Enter hostname (full or partial) or previous # number')
        # if keyboard input empty, extra space needed in print
        if not k_input: print ('')
        # allows up arrow to get last entry entered
        readline.add_history(k_input) 
        print('')

        # First, check if a hostname matches exactly 
        df_filter = df_hosts[df_hosts.index == k_input]
        # Match found, we can exit loop with the hostname
        if not df_filter.empty:
            hostname = df_filter.index[0]
            break

        # Filter down on rows that contain the user input
        df_filter = df_hosts[df_hosts.index.str.contains(k_input)]
        # Sort the df filter by index (hostname)
        df_filter = df_filter.sort_index()
        # If filtered df is just 1 row, we found our match
        if len(df_filter) == 1:
            hostname = df_filter.index[0]
            break
        elif len(df_filter) == 0:
            print('No Matches Found!')
            continue
        elif len(df_filter) > 1:

            table = Table(title='Matching Hostnames')
            table.add_column("Hostname", style="cyan")
            table.add_column("IP", style="purple")
            table.add_column("Tag", style="green")

            for ind in df_filter.index:
                table.add_row(ind,df_filter['ip'][ind],df_filter['tag'][ind])
            print (table)

        

    print(f"[bold]Hostname found of [purple]{hostname}")

if __name__== '__main__':
    main(sys.argv[1:])