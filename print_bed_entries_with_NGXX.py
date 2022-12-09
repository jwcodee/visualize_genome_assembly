import argparse
import os
import sys


def main():

    parser = argparse.ArgumentParser(
        description='This script will output a bed file with the top NGXX entries')
    parser.add_argument(
        '--bed', help='The name of the bed file', required=True)
    parser.add_argument(
        '--ref', help='The name of the reference genome file', required=True)
    parser.add_argument(
        '--draft', help='The name of the draft genome file', required=True)
    parser.add_argument('--ng', help='The NGXX to use',
                        default=95, required=False)
    args = parser.parse_args()

    # process reference genome file and sum the sequence length
    genome_size = 0
    with open(args.ref, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                continue
            else:
                genome_size = genome_size + len(line)

    ngxx_length = genome_size * (int(args.ng)/100)

    length_list = []

    # process draft fasta file add the length and name of each sequence to a list
    with open(args.draft, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                sequence_id = line[1:].split(" ")[0]
                sequence_length = 0
            else:
                sequence_length = sequence_length + len(line)
                length_list.append((sequence_length, sequence_id))

    # sort list by length descending
    length_list.sort(reverse=True)

    sequence_id_white_list = set()

    # iterate through list and add the sequence id to a dictionary if the running sum is less than the NGXX
    running_length = 0
    for i in length_list:
        running_length = running_length + i[0]
        sequence_id_white_list.add(i[1])
        if running_length > ngxx_length:
            break

    # process bed file and print bed entries that are in the white list
    with open(args.bed, 'r') as f:
        for line in f:
            line = line.strip()
            line = line.split('\t')
            if line[3] in sequence_id_white_list:
                print(*line, sep='\t')


main()
