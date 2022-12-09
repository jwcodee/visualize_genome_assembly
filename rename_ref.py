import argparse
import os
import sys


def main():

    # parse arguments
    parser = argparse.ArgumentParser(
        description='This script will rename the reference file beginning with chr1')
    parser.add_argument(
        '--ref', help='The name of the reference file', required=True)

    args = parser.parse_args()

    # read reference file and output chromosome, rename each chromosome with >chr
    curr_chromo_num = 1
    with open(args.ref, 'r') as f:
        for line in f:
            line = line.strip()
            if line[0] == '>':
                print(">" + "chr" + str(curr_chromo_num))
                curr_chromo_num = curr_chromo_num + 1
            else:
                print(line)


main()
