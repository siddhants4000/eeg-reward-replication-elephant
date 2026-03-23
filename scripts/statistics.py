import pandas as pd
from scipy.stats import ttest_rel
import numpy as np

def cohens_d(x, y):
    diff = np.array(x) - np.array(y)
    return diff.mean() / diff.std(ddof=1)

def compute_stats(df):
    results = []

    def test(a, b, label):
        stat, p = ttest_rel(df[a], df[b])
        d = cohens_d(df[a], df[b])
        results.append({
            "comparison": label,
            "p_value": p,
            "effect_size": d
        })

    test("Gain_FRN", "Loss_FRN", "Gain vs Loss (FRN)")
    test("Gain_P300", "Neutral_P300", "Gain vs Neutral (P300)")
    test("Loss_FRN", "Neutral_FRN", "Loss vs Neutral (FRN)")

    return pd.DataFrame(results)