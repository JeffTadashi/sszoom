#!/usr/bin/env python3

from datetime import datetime
import os
import pathlib
import pandas as pd
import readline
from rich.prompt import Prompt
from rich.table import Table
from rich import print
import sys
import tomli

banner = '''
[bold white]
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
    paths['LOG'] = pathlib.Path.home() / '.sszoom' / 'log'
    

    # Open all the files needed
    df_hosts = pd.read_csv(paths['HOSTS'], index_col=0, keep_default_na=False)
    df_creds = pd.read_csv(paths['CREDENTIALS'], index_col=0)


    #############################################
    ## 
    #############################################

    # Set blank in case user calls number first on accident
    rnumdict = {}
    # loop to get down to single hostname
    while True: 

        print('')
        k_input = Prompt.ask("[bold white]Enter hostname (full or partial) or previous search's # number")
        # if keyboard input empty, extra space needed in print
        if not k_input: print ('')
        # allows up arrow to get last entry entered
        readline.add_history(k_input) 
        print('')

        # Check if user provided just a number, then check if it mathces the last rnum result
        if k_input.isdigit() and k_input in rnumdict:
            # return hostname/ip from the results dict
            hostname = rnumdict[k_input]
            break

        # Check if a hostname matches exactly 
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
            # reset results table, if it existed before
            rnumdict = {}
            continue
        elif len(df_filter) > 1:

            table = Table(title='Matching Hostnames')
            table.add_column("#", style="yellow")
            table.add_column("Hostname", style="cyan")
            table.add_column("IP", style="magenta")
            table.add_column("Tag", style="green")

            # pandas doens't have row number, so we will keep track of this separately with rnum/rnundict
            rnum = 0
            rnumdict = {}
            # iterate through each result row
            for ind in df_filter.index:
                rnum += 1
                # populate the dict of result number against hostname
                rnumdict[str(rnum)] = ind
                table.add_row(str(rnum),ind,df_filter['ip'][ind],df_filter['tag'][ind])
            print (table)
            continue
 
        print ("[bold red]ERROR! you're not supposed to be here...")

    
    print(f"[bold]Hostname found: [bold cyan]{hostname}")

    #############################################
    ## Username/Password
    #############################################

    while True:

        print('')
        k_input = Prompt.ask("[bold white]Enter username or alias. Leave blank to list all aliases")
        # if keyboard input empty, extra space needed in print
        if not k_input: print ('')
        # allows up arrow to get last entry entered
        readline.add_history(k_input) 
        print('')

        if not k_input: 
            # list all aliases (but not passwords)

            table = Table(title='All Aliases')
            table.add_column("Alias", style="yellow")
            table.add_column("Username", style="cyan")

            # iterate through each alias creds df row
            for ind in df_creds.index:
                table.add_row(ind,df_creds['username'][ind])
            print (table)
            continue        
        elif k_input:
            # Filter/Check if a user input matches an alias
            df_filter = df_creds[df_creds.index == k_input]
            # If match found, get username/password
            if not df_filter.empty:
                # "0" because result should only be a single row
                username = df_filter['username'][0]
                password = df_filter['password'][0]
                print (f"[bold white]Alias found! Using username: [bold cyan]{username}")
                break
            # if no match found, return user input as username, and ask for password
            else:
                username = k_input
                print (f"[bold white]Using username: [bold cyan]{username}")
                print ("")
                password = Prompt.ask("[bold white]Enter password", password=True)
                break

    #############################################
    ## SSH
    #############################################

    # Get timestamp and log filename
    now_time = datetime.now()
    timestamp = now_time.strftime('%Y-%m-%d__%H-%M-%S')
    log_filename = f"{timestamp}__{hostname}.ios"

    # Get IP. Index is the hostname
    ip = df_hosts['ip'][hostname]

    print ("")
    print (f"[bold white]Connecting to: [bold cyan]{ip}[bold white] as [bold cyan]{username}")
    print ("")

    ssh_params = f"-o Ciphers=+aes256-cbc -o HostKeyAlgorithms=+ssh-rsa -o KexAlgorithms=+diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,diffie-hellman-group-exchange-sha1 -o ConnectTimeout=9 -o StrictHostKeyChecking=no {username}@{ip}"

    pipe_params = f"tee {paths['LOG']}/{log_filename}"
    

    # Expect script to enter passwordnon-interactively
    # 2> /dev/null is to suppress errors. Sometime it would display password
    os.system(f" expect -c 'spawn ssh {ssh_params}; expect \"assword\"; send \"{password}\r\"; interact' 2> /dev/null | {pipe_params} ")

    print ("")
    Prompt.ask("[bold white]SSZOOM script concluded. Press ENTER to fully close")



if __name__== '__main__':
    main(sys.argv[1:])