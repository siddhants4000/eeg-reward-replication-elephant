import mne
import numpy as np

def preprocess_raw(raw):
    raw = raw.copy()

    # Ensure reproducibility
    np.random.seed(42)
    raw.set_montage("standard_1020", verbose=False)

    # --------------------------------------------------
    # FILTER
    # --------------------------------------------------
    raw.filter(0.1, 30., fir_design="firwin", verbose=False)

    # --------------------------------------------------
    # RE-REFERENCE
    # --------------------------------------------------
    raw.set_eeg_reference("average", verbose=False)

    # --------------------------------------------------
    # ICA (CONTROLLED)
    # --------------------------------------------------
    try:
        from mne.preprocessing import ICA

        ica = ICA(
            n_components=20,
            random_state=42,   
            max_iter="auto"
        )

        ica.fit(raw, verbose=False)
        raw = ica.apply(raw.copy(), verbose=False)

    except Exception as e:
        print(f"ICA skipped: {e}")

    return raw