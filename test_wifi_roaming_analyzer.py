import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import analyse

def row(device, ts, ap, signal):
    return {"device": device, "timestamp": ts, "ap": ap, "signal_dbm": str(signal)}

class TestWifiRoaming(unittest.TestCase):
    def test_roam_counted(self):
        r = analyse([row("Laptop-1", "2026-11-08T09:00:00", "AP-1", -60),
                     row("Laptop-1", "2026-11-08T09:05:00", "AP-2", -65)])
        self.assertEqual(r[0][1], 1)
    def test_same_ap_no_roam(self):
        r = analyse([row("Laptop-1", "2026-11-08T09:00:00", "AP-1", -60),
                     row("Laptop-1", "2026-11-08T09:05:00", "AP-1", -62)])
        self.assertEqual(r[0][1], 0)
    def test_roam_back_counts_again(self):
        r = analyse([row("Laptop-1", "2026-11-08T09:00:00", "AP-1", -60),
                     row("Laptop-1", "2026-11-08T09:05:00", "AP-2", -65),
                     row("Laptop-1", "2026-11-08T09:10:00", "AP-1", -61)])
        self.assertEqual(r[0][1], 2)
    def test_weak_signal_flag(self):
        r = analyse([row("Laptop-1", "2026-11-08T09:00:00", "AP-1", -80)])
        self.assertEqual(r[0][5], "WEAK")
    def test_boundary_minus_75_is_ok(self):
        r = analyse([row("Laptop-1", "2026-11-08T09:00:00", "AP-1", -75)])
        self.assertEqual(r[0][5], "OK")
    def test_aps_seen_listed(self):
        r = analyse([row("Laptop-1", "2026-11-08T09:00:00", "AP-1", -60),
                     row("Laptop-1", "2026-11-08T09:05:00", "AP-2", -65)])
        self.assertEqual(r[0][2], ["AP-1", "AP-2"])
    def test_most_roams_first(self):
        r = analyse([row("A", "2026-11-08T09:00:00", "AP-1", -60),
                     row("B", "2026-11-08T09:00:00", "AP-1", -60),
                     row("B", "2026-11-08T09:05:00", "AP-2", -65)])
        self.assertEqual(r[0][0], "B")
    def test_empty_input(self):
        self.assertEqual(analyse([]), [])
