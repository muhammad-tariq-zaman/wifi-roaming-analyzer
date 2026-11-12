# wifi-roaming-analyzer

Analyse Wi-Fi roaming from a CSV of device association records: a roam is the same device seen on a different access point than its previous record, and a latest signal below -75 dBm is flagged WEAK — most roams first.

## How to run

```sh
python3 main.py associations.csv
```

## Example output

```
Laptop-1: 1 roam(s), 2 AP(s) seen, latest AP-2 (-65 dBm) — OK
Phone-2: 0 roam(s), 1 AP(s) seen, latest AP-1 (-80 dBm) — WEAK
1 device(s) on a weak signal.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
