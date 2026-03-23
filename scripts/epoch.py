import mne

def get_event_keys(event_id):
    return [k for k in event_id.keys() if str(k).startswith("Stimulus")]

def create_epochs(raw, tmin, tmax, baseline):
    events, event_id = mne.events_from_annotations(raw, verbose=False)

    stim_keys = get_event_keys(event_id)

    if len(stim_keys) < 3:
        raise ValueError("Not enough stimulus conditions found")

    cond_map = {
        "Gain": event_id[stim_keys[0]],
        "Neutral": event_id[stim_keys[1]],
        "Loss": event_id[stim_keys[2]],
    }

    epochs = mne.Epochs(
        raw,
        events,
        event_id=cond_map,
        tmin=tmin,
        tmax=tmax,
        baseline=baseline,
        preload=True,
        reject_by_annotation=True,
        verbose=False
    )

    return epochs, cond_map