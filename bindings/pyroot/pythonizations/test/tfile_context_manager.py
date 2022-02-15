import os
import unittest

import ROOT

from ROOT import TFile


class TFileContextManager(unittest.TestCase):
    """
    Test of TFile used as context manager
    """

    NBINS = 123
    XMIN = 10
    XMAX = 242

    def test_write_histogram(self):
        """
        Check that an histogram is correctly written to a file within a context
        manager.
        """
        filename = "TFileContextManager_test_write_histogram.root"
        with TFile(filename, "recreate") as outfile:
            hout = ROOT.TH1F("h", "h", self.NBINS, self.XMIN, self.XMAX)
            outfile.WriteObject(hout, "histo")

        self.assertTrue(outfile)  # The TFile object is still there
        self.assertFalse(outfile.IsOpen())  # And it is correctly closed

        with TFile(filename, "read") as infile:
            hin = infile.Get("histo")
            xaxis = hin.GetXaxis()
            self.assertEqual(self.NBINS, hin.GetNbinsX())
            self.assertEqual(self.XMIN, xaxis.GetXmin())
            self.assertEqual(self.XMAX, xaxis.GetXmax())

        os.remove(filename)


if __name__ == '__main__':
    unittest.main()
