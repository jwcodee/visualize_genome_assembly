import argparse
import os
import sys


def main():

    # parse arguments
    parser = argparse.ArgumentParser(
        description='This script will output a bed file with an additional colour column for each bed entry. The colours will rotate between light blue and dark blue.')
    parser.add_argument(
        '--bed', help='The name of the bed file', required=True)

    args = parser.parse_args()

    colours = ["light blue", "dark blue"]

    # add rotating colors to bed entries
    with open(args.bed, 'r') as f:
        curr_colour = 0
        for line in f:
            if curr_colour == 0:
                curr_colour = 1
            else:
                curr_colour = 0
            line = line.strip()
            print(line, colours[curr_colour], sep='\t')


main()
