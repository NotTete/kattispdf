import kattispdf
import argparse
import pathlib


def cli():
    parser = argparse.ArgumentParser(prog='kpdf')

    parser.add_argument('problem', help="Problem ID")
    parser.add_argument('-o', '--output', type=pathlib.Path, help="Path to the outputed pdf", dest="path", default=None)
    args = parser.parse_args()

    kattispdf.generate_pdf(args.problem, args.path)

