#!/usr/bin/env python3

import re, argparse

def main():
    args = parseArgs()
    source = open(args.source.name, 'r', encoding=args.encoding) if args.encoding else args.source
    outp = args.output if args.output.name == '<stdout>' else open(args.output.name, 'w', encoding=args.encoding) if args.encoding else args.output
    CsvFixer(source, outp, args.quote, args.delimiter).process()

def parseArgs():
    parser = argparse.ArgumentParser(description="Process CSV file with quoted fields doubling quotes inside fields")
    parser.add_argument('source', type=argparse.FileType('r', encoding='UTF-8'), help="Source CSV file")
    parser.add_argument('-d', '--delimiter', type=str, default=',', help="Delimiter char, default to ','")
    parser.add_argument('-q', '--quote', type=str, default='"', help='Quoting char used, default to \'"\'')
    parser.add_argument('-e', '--encoding', type=str, default='UTF-8', help="Use a specific encoding for input and output, such as UTF-8, Latin-1, default to UTF-8")
    parser.add_argument('-o', '--output', type=argparse.FileType('w', encoding='UTF-8'), default='-')
    args = parser.parse_args(['tests/resources/test.csv'])
    return args

class CsvFixer:
    def __init__(self, source, outp, quote, delimiter):
        self.source = source
        self.outp = outp
        self.quote = quote
        self.delimiter = delimiter
        self.reg = re.compile(f'(")(.+?)("{self.delimiter}|"$)')    
    
    def process(self):
        with self.source as inp:
            for line in inp:
                print(self.processLine(line), end='', file=self.outp)
    
    def processLine(self, line):
        end = 0
        lr = ''
        for m in self.reg.finditer(line):
            lr += line[end:m.start()]
            lr += m.group(1)
            lr += m.group(2).replace(self.quote, self.quote + self.quote)
            lr += m.group(3)
            end = m.end()
        
        if end > 0:
            lr += line[end:]
            line = lr
        return line

if __name__ == "__main__":
    main()