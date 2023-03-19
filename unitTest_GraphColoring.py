from unittest import TestCase

from main import main


class Test(TestCase):
    def test_gc_78317094521100(self):
        inputTextFile = "inputFiles/gc_78317094521100.txt"
        result = main(inputTextFile)
        self.assertTrue(result != False)

    def test_gc_78317097930400(self):
        inputTextFile = "inputFiles/gc_78317097930400.txt"
        result = main(inputTextFile)
        self.assertTrue(result != False)

    def test_gc_78317097930401(self):
        inputTextFile = "inputFiles/gc_78317097930401.txt"
        result = main(inputTextFile)
        self.assertTrue(result == False)


    def test_gc_78317100510400(self):
        inputTextFile = "inputFiles/gc_78317100510400.txt"
        result = main(inputTextFile)
        self.assertTrue(result != False)

    def test_gc_78317103208800(self):
        inputTextFile = "inputFiles/gc_78317103208800.txt"
        result = main(inputTextFile)
        self.assertTrue(result != False)

    def test_gc_1378296846561000(self):
        inputTextFile = "inputFiles/gc_1378296846561000.txt"
        result = main(inputTextFile)
        self.assertTrue(result != False)

    def test_test(self):
        inputTextFile = "inputFiles/test.txt"
        result = main(inputTextFile)
        self.assertTrue(result != False)
