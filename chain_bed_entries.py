import argparse
import os
import sys


def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        description='This script will chain bed entries that are within a certain distance')
    parser.add_argument(
        '--bed', help='The name of the bed file', required=True)
    parser.add_argument(
        '--dist', help='The name of the reference genome file', default=50000, required=False)
    args = parser.parse_args()

    id_to_bed = {}

    # read bed file input and store in dictionary using id as key and bed as value
    with open(args.bed, 'r') as f:
        for line in f:
            line = line.strip()
            line = line.split('\t')
            # check if id is in dictionary
            if line[3] in id_to_bed:
                # if id is in dictionary, append bed to list
                id_to_bed[line[3]].append(line)
            else:
                # if id is not in dictionary, create new list and append bed
                id_to_bed[line[3]] = [line]

    # iterate through dictionary and sort by chromosome and then start position
    for id in id_to_bed:
        id_to_bed[id].sort(key=lambda x: (x[0], int(x[1])))

    # iterate through dictionary and chain bed entries that are within the distance
    for id in id_to_bed:
        i = 0
        while i < len(id_to_bed[id]) - 1:
            # check if bed entries are within the distance
            if int(id_to_bed[id][i][2]) + int(args.dist) > int(id_to_bed[id][i+1][1]) and id_to_bed[id][i][0] == id_to_bed[id][i+1][0]:
                # if bed entries are within the distance, merge them
                id_to_bed[id][i][2] = id_to_bed[id][i+1][2]
                # remove the bed entry that was merged
                id_to_bed[id].pop(i+1)
            else:
                i = i + 1

    # iterate through dictionary and print bed entries
    for id in id_to_bed:
        for bed in id_to_bed[id]:
            print(*bed, sep='\t')


main()
