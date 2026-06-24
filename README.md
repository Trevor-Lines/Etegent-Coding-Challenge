# Etegent Coding Challenge: Time History Association

This script compares each experimentally observed signal against a library of reference signals. For each experimental signal, it slides it across every reference signal's time range, scores the fit at every offset using R², and keeps the offset with the best score. After scoring against all references, the top 2 reference matches are plotted alongside the experimental signal and results are saved to a CSV.

## Approach

My approach was to start small, looking at a slice of the data first to work out a methodology for comparing experimental signals to reference signals. I initially calculated the relative error at each (shifted) time index between a reference and an experimental signal, then averaged that error across the signal to get a single match score, and used that to rank and plot the top two matches per experimental signal.

The relative error approach passed an initial eye test, but once I added a percentage fit metric, I saw the fits were low (at times ~50%) even for visually strong matches. That sent me looking for a better scoring approach, and I landed on R², a standard goodness-of-fit measurement I'm used to from ML work. Switching to R² significantly improved the fit scores.

## How to Run

**Requirements:** Python 3.9+, with the following packages:
```
numpy
pandas
plotly
scikit-learn
natsort
```
Install with:
```
pip install numpy pandas plotly scikit-learn natsort
```

**Run:**
```
python signal_match.py
```
This generates one HTML plot per experimental signal in `data/plots/`, each showing the top 2 matching reference signals overlaid with the shifted experimental signal. A summary CSV is saved to `data/run_times.csv` with each experimental signal's top 2 reference matches, their R² fit scores, and per-signal runtime. Runtime stats are also printed to the console.

## Findings

- Average runtime per experimental signal: ~0.05 seconds
- Total program runtime (40 experimental signals × 4 references): ~2.29 seconds
- Best R² fit observed: 0.9903 (Experimental 19 vs. Reference 1)
- Average best R² fit: 0.8338

## Recommendations

With more time, this could be extended into a Python application or web app with a UI to upload reference and experimental signals. Further investigations could be made to improve runtime.
