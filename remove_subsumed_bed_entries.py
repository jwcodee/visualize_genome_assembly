import argparse
import os
import sys


def main():

    # parse arguments
    parser = argparse.ArgumentParser(
        description='This script will output a bed file with the top NGXX entries')
    parser.add_argument(
        '--bed', help='The name of the bed file', required=True)
    args = parser.parse_args()

    # store bed entries in list
    bed_list = []
    with open(args.bed, 'r') as f:
        for line in f:
            line = line.strip()
            line = line.split('\t')
            bed_list.append(line)

    # sort bed entries by chromosome and then start position
    bed_list.sort(key=lambda x: (x[0], int(x[1])))

    # iterate through list and remove bed entries nested with previous bed entry
    i = 0
    while i < len(bed_list) - 1:
        # check if bed entries are nested by comparing start and end positions
        if int(bed_list[i][1]) <= int(bed_list[i+1][1]) and int(bed_list[i][2]) >= int(bed_list[i+1][2]):
            # if bed entries are nested, remove the nested bed entry
            bed_list.pop(i+1)
        else:
            i = i + 1

    # print bed entries
    for bed in bed_list:
        print(*bed, sep='\t')


main()
