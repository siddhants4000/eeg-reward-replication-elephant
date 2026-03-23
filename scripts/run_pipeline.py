from pathlib import Path
import pandas as pd
import sys
import logging
import numpy as np

# --------------------------------------------------
# GLOBAL RANDOM SEED (CRITICAL FOR REPRODUCIBILITY)
# --------------------------------------------------
np.random.seed(42)

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import config as cfg
from scripts import load_data as ld
from scripts import preprocess as pp
from scripts import epoch as ep
from scripts import erp
from scripts import statistics as stats
from scripts import figures as figs


def main():

    # --------------------------------------------------
    # CREATE OUTPUT FOLDERS
    # --------------------------------------------------
    for folder in [
        cfg.FIGURES_DIR,
        cfg.RESULTS_DIR,
        cfg.SANITY_DIR,
        cfg.LOGS_DIR
    ]:
        folder.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # LOGGING SETUP
    # --------------------------------------------------
    logging.basicConfig(
        filename=cfg.LOGS_DIR / "pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("=== PIPELINE STARTED ===")

    results = []

    for sub in cfg.SUBJECTS:
        print("\nProcessing", sub)
        logging.info(f"Processing {sub}")

        sub_path = cfg.DATA_ROOT / sub

        try:
            raw = ld.load_raw(sub_path)
            raw = pp.preprocess_raw(raw)

            epochs, cond_map = ep.create_epochs(
                raw, cfg.TMIN, cfg.TMAX, cfg.BASELINE
            )

            evokeds = erp.compute_evokeds(epochs)

            # Save ERP plot
            figs.save_erp_plot(
                evokeds,
                cfg.P300_CH,
                cfg.FIGURES_DIR / f"{sub}_erp.png"
            )

            # Compute values
            row = {"subject": sub}

            for cond, ev in evokeds.items():
                row[f"{cond}_FRN"] = erp.mean_amplitude(
                    ev, cfg.FRN_CH, *cfg.FRN_WIN
                )
                row[f"{cond}_P300"] = erp.mean_amplitude(
                    ev, cfg.P300_CH, *cfg.P300_WIN
                )

            results.append(row)
            logging.info(f"{sub} processed successfully")

        except Exception as e:
            print("Skipped", sub, ":", e)
            logging.error(f"{sub} failed: {str(e)}")

    # --------------------------------------------------
    # CREATE DATAFRAME
    # --------------------------------------------------
    df = pd.DataFrame(results)

    if df.empty:
        logging.error("No data processed. Exiting.")
        return

    # --------------------------------------------------
    # CONVERT TO MICROVOLTS (µV)
    # --------------------------------------------------
    for col in df.columns:
        if col != "subject":
            df[col] = df[col] * 1e6

    # --------------------------------------------------
    # COMPUTE GROUP MEAN
    # --------------------------------------------------
    mean_row = df.mean(numeric_only=True)
    mean_row["subject"] = "GroupMean"

    df = pd.concat([df, pd.DataFrame([mean_row])], ignore_index=True)

    # --------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------
    df.to_csv(cfg.RESULTS_DIR / "mean_amplitudes.csv", index=False)

    # --------------------------------------------------
    # STATISTICS (exclude GroupMean)
    # --------------------------------------------------
    df_stats = df[df["subject"] != "GroupMean"]

    stats_df = stats.compute_stats(df_stats)
    stats_df.to_csv(cfg.RESULTS_DIR / "statistics.csv", index=False)

    # --------------------------------------------------
    # SANITY CHECKS (STRONG VERSION)
    # --------------------------------------------------
    sanity_file = cfg.SANITY_DIR / "sanity_checks.txt"

    with open(sanity_file, "w") as f:
        f.write("=== SANITY CHECKS ===\n\n")

        f.write("Subjects processed:\n")
        f.write(str(df["subject"].tolist()) + "\n\n")

        f.write("Data shape:\n")
        f.write(str(df.shape) + "\n\n")

        f.write("Summary statistics:\n")
        f.write(str(df.describe()) + "\n\n")

        f.write("Group Mean:\n")
        f.write(str(df[df["subject"] == "GroupMean"]) + "\n\n")

        # Value range check (VERY IMPORTANT)
        f.write("Value range check (µV):\n")
        f.write("Expected: approx -10 to +10 µV\n")
        f.write(str(df.describe()) + "\n\n")

    logging.info("Sanity checks generated")
    logging.info("=== PIPELINE FINISHED SUCCESSFULLY ===")

    print("\nDONE — Everything saved (results, logs, sanity checks)!")


if __name__ == "__main__":
    main()