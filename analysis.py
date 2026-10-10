"""Assignment 03: summarize a telemetry ward's systolic readings.

Run from the assignment directory with the project environment active:

    python3 analysis.py
"""

import numpy as np


def load_readings(filename):
    """Return (patient_ids, monitors, hour_columns, readings) from the supplied CSV.

    readings is a 2D array of integers: one row per patient, one column per
    monitored hour, in the order the header lists them.
    """
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    header = lines[0].strip().split(",")
    rows = [line.strip().split(",") for line in lines[1:] if line.strip()]

    patient_ids = np.array([row[0] for row in rows])
    monitors = np.array([row[1] for row in rows])
    hour_columns = np.array(header[2:])
    readings = np.array([row[2:] for row in rows]).astype(int)
    return patient_ids, monitors, hour_columns, readings


def main():
    patient_ids, monitors, hour_columns, readings = load_readings("data/bp_readings.csv")
    print(f"Loaded {readings.shape[0]} patients x {readings.shape[1]} hours")

     
    patients = readings.shape[0]
    total_readings = readings.size

    mean_sbp = np.mean(readings)
    sd_sbp = np.std(readings)

    min_sbp = np.min(readings)
    max_sbp = np.max(readings)

    patient_means = np.mean(readings, axis=1)

    stage2_patients = np.sum(patient_means >= 140)

    highest_index = np.argmax(patient_means)
    highest_patient = patient_ids[highest_index]
    highest_patient_mean = patient_means[highest_index]

    hour_means = np.mean(readings, axis=0)
    peak_hour_index = np.argmax(hour_means)
    peak_hour_column = hour_columns[peak_hour_index]
    peak_hour_mean = hour_means[peak_hour_index]


    monitor_names = np.unique(monitors)
    monitor_averages = []

    for monitor in monitor_names:
        mask = monitors == monitor
        average = np.mean(patient_means[mask])
        monitor_averages.append(average)

    monitor_averages = np.array(monitor_averages)

    high_monitor_index = np.argmax(monitor_averages)
    high_monitor = monitor_names[high_monitor_index]

    
    other_mask = monitors != high_monitor
    other_means = patient_means[other_mask]

    monitor_offset = (
        monitor_averages[high_monitor_index] - np.mean(other_means)
    )

    stage2_other_monitors = np.sum(other_means >= 140)

    with open("output/vitals_summary.txt", "w") as file:
        file.write(f"patients: {patients}\n")
        file.write(f"readings: {total_readings}\n")
        file.write(f"mean_sbp: {mean_sbp}\n")
        file.write(f"sd_sbp: {sd_sbp}\n")
        file.write(f"min_sbp: {min_sbp}\n")
        file.write(f"max_sbp: {max_sbp}\n")
        file.write(f"stage2_patients: {stage2_patients}\n")
        file.write(f"highest_patient: {highest_patient}\n")
        file.write(f"highest_patient_mean: {highest_patient_mean}\n")
        file.write(f"peak_hour_column: {peak_hour_column}\n")
        file.write(f"peak_hour_mean: {peak_hour_mean}\n")
        file.write(f"high_monitor: {high_monitor}\n")
        file.write(f"monitor_offset: {monitor_offset}\n")
        file.write(f"stage2_other_monitors: {stage2_other_monitors}\n")

if __name__ == "__main__":
    main()
