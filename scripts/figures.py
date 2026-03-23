import matplotlib.pyplot as plt
import mne

def save_erp_plot(evokeds, channel, out_path):
    if isinstance(channel, str):
        picks = [channel]
    else:
        picks = channel

    combine_method = "mean" if len(picks) > 1 else None

    fig = mne.viz.plot_compare_evokeds(
        evokeds,
        picks=picks,
        combine=combine_method,
        show=False,
        show_sensors=False
    )

    if isinstance(fig, list):
        fig = fig[0]

    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)