from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
import mne

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import config as cfg
from scripts import load_data as ld
from scripts import preprocess as pp
from scripts import epoch as ep
from scripts import erp


np.random.seed(42)


def main():
    cfg.FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    gain_evokeds = []
    neutral_evokeds = []
    loss_evokeds = []

    for sub in cfg.SUBJECTS:
        print(f"Processing {sub}")
        sub_path = cfg.DATA_ROOT / sub

        try:
            raw = ld.load_raw(sub_path)
            raw = pp.preprocess_raw(raw)

            epochs, cond_map = ep.create_epochs(
                raw,
                cfg.TMIN,
                cfg.TMAX,
                cfg.BASELINE
            )

            evokeds = erp.compute_evokeds(epochs)

            if "Gain" in evokeds:
                gain_evokeds.append(evokeds["Gain"])
            if "Neutral" in evokeds:
                neutral_evokeds.append(evokeds["Neutral"])
            if "Loss" in evokeds:
                loss_evokeds.append(evokeds["Loss"])

        except Exception as e:
            print(f"Skipped {sub}: {e}")

    if not gain_evokeds or not neutral_evokeds or not loss_evokeds:
        raise RuntimeError("Not enough evokeds collected to compute grand average.")

    grand_gain = mne.grand_average(gain_evokeds)
    grand_neutral = mne.grand_average(neutral_evokeds)
    grand_loss = mne.grand_average(loss_evokeds)

    evokeds = {
        "Gain": grand_gain,
        "Neutral": grand_neutral,
        "Loss": grand_loss,
    }

    fig = mne.viz.plot_compare_evokeds(
        evokeds,
        picks=["Pz"],
        combine=None,
        show=False,
        show_sensors=False,
        title="Grand-average ERP at Pz (Gain, Neutral, Loss)"
    )

    if isinstance(fig, list):
        fig = fig[0]

    ax = fig.axes[0]

    ax.axvspan(0.3, 0.6, color='gray', alpha=0.2)

    ax.grid(alpha=0.2)

    ax.legend(loc="upper left")

    out_path = cfg.FIGURES_DIR / "grand_average_pz.png"
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"\nSaved Figure 1 to: {out_path}")


if __name__ == "__main__":
    main()