from pathlib import Path
import mne

def find_vhdr(subject_dir: Path):
    files = list(subject_dir.rglob("*.vhdr"))
    if not files:
        raise FileNotFoundError(f"No .vhdr found in {subject_dir}")
    return files[0]

def load_raw(subject_dir: Path):
    vhdr = find_vhdr(subject_dir)
    print("Loading:", vhdr)
    return mne.io.read_raw_brainvision(vhdr, preload=True, verbose=False)