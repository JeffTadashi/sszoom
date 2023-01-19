#!/usr/bin/env python3


import pathlib
import pandas as pd
import readline
import rich
import sys
import tomli




def main(argv):

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
    hosts_df = pd.read_csv(paths['HOSTS'], index_col=0, keep_default_na=False)
    creds_df = pd.read_csv(paths['CREDENTIALS'], index_col=0)
    print (hosts_df)
    print (creds_df)


    #############################################
    ## 
    #############################################





if __name__== '__main__':
    main(sys.argv[1:])