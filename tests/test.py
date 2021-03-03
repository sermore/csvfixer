import unittest, tempfile, csv, os
from csvfixer import CsvFixer

class TestProcess(unittest.TestCase):

    def test_processLine(self):
        c = CsvFixer(None, None, '"', ',')
        self.assertEqual(r'1,"Content with a ""quote""","Another ""quote"" here"', 
                         c.processLine(r'1,"Content with a "quote"","Another "quote" here"'))
        self.assertEqual(r'"""First quote not òà closed",123,"A quote as last ""char"""', 
                         c.processLine(r'""First quote not òà closed",123,"A quote as last "char""'))

    def test_process(self):
        with open('resources/test.csv', 'r') as source:
            with tempfile.TemporaryDirectory(prefix='csvfixer') as tempDir:
                tempFile = os.path.join(tempDir, 'out.csv')                 
                with open(tempFile, 'w') as outp:
                    c = CsvFixer(source, outp, '"', ',')
                    c.process()
                with open(tempFile, 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        print(row)
                        self.assertEquals(3, len(row))

if __name__ == '__main__':
    unittest.main()
