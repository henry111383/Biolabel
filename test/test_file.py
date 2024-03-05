import unittest
import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from biolabel.model.File import *

class File_FileShouldBeCorrect(unittest.TestCase):
    def setUp(self):
        self.empty_File = File()

    def tearDown(self):
        del self.empty_File
        
    def test_EmptyFileShouldHaveEmptyLocation(self):
        expected = self.empty_File.GetFileLocation()
        result = None
        self.assertEqual(expected, result)

    def test_EmptyFileShouldHaveEmptyName(self):
        expected = self.empty_File.GetFileName()
        result = None
        self.assertEqual(expected, result)
        
    def test_EmptyFileShouldHaveEmptyFileFormat(self):
        expected = self.empty_File.GetFileFormat()
        result = None
        self.assertEqual(expected, result)

    def test_EmptyFileShouldHaveEmptyFileFormat(self):
        expected = self.empty_File.GetDirectory()
        result = None
        self.assertEqual(expected, result)

    def test_FileLocationSetterShouldBeCorrect(self):
        Location = '/mnt/c/test/empty/file'
        self.empty_File.SetFileLocation(Location)
        expected = Location
        result = self.empty_File.GetFileLocation()
        self.assertEqual(expected, result)

    def test_FileNameSetterShouldBeCorrect(self):
        Name = 'IamFile'
        self.empty_File.SetFileName(Name)
        expected = Name
        result = self.empty_File.GetFileName()
        self.assertEqual(expected, result)

    def test_FileFormatSetterShouldBeCorrect(self):
        Format = 'biolabel'
        self.empty_File.SetFileFormat(Format)
        expected = Format
        result = self.empty_File.GetFileFormat()
        self.assertEqual(expected, result)

    def test_FileSetterShouldBeCorrect(self):
        Directory = '/mnt/c/test/empty/'
        self.empty_File.SetDirectory(Directory)
        expected = Directory
        result = self.empty_File.GetDirectory()
        self.assertEqual(expected, result)
    
    
    


  