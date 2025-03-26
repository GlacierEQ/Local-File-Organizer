#!/bin/bash
# Ensure the workspace exists (if not already created)
mkdir -p Sorting_Area/{Incoming_Files,Sorted_Files,Logs,Backups,Dependencies,Recovered_Files}
# Run the auto‑optimization cycle
python auto_optimize.py
