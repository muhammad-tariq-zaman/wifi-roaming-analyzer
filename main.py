"""Analyse Wi-Fi roaming from device association records.

Usage: python3 main.py associations.csv
CSV columns: device,timestamp (ISO),ap,signal_dbm.
A roam is the same device seen on a different access point
than its previous record. WEAK means the device's latest
signal is below -75 dBm. Report per device: roam count, APs
seen, latest AP and signal, WEAK flag. Most roams first.
"""
import argparse, csv, sys
from collections import defaultdict

WEAK_DBM = -75

def analyse(rows):
    per_device = defaultdict(list)
    for row in rows:
        per_device[row["device"].strip()].append(row)
    out = []
    for device in sorted(per_device):
        records = sorted(per_device[device], key=lambda r: r["timestamp"].strip())
        roams = 0
        aps = []
        previous_ap = None
        for record in records:
            ap = record["ap"].strip()
            if ap not in aps:
                aps.append(ap)
            if previous_ap is not None and ap != previous_ap:
                roams += 1
            previous_ap = ap
        latest = records[-1]
        signal = int(latest["signal_dbm"])
        verdict = "WEAK" if signal < WEAK_DBM else "OK"
        out.append((device, roams, aps, latest["ap"].strip(), signal, verdict))
    return sorted(out, key=lambda r: (-r[1], r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = analyse(list(csv.DictReader(f)))
    for device, roams, aps, latest_ap, signal, verdict in results:
        print(f"{device}: {roams} roam(s), {len(aps)} AP(s) seen, "
              f"latest {latest_ap} ({signal} dBm) — {verdict}")
    print(f"{sum(1 for *_, v in results if v == 'WEAK')} device(s) on a weak signal.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
