# Etegent Coding Challenge: Time History Association
 
This script compares a set of experimental signals against a library of reference signals. For each reference signal, it slides each experimental signal across the reference's time range, scores the fit at every offset using R², and keeps the offset with the best score. After scoring every experimental signal against a reference, the top 2 matches are plotted against that reference signal.
 
## Approach
 
My approach was to start small, looking at a slice of the data first to work out a methodology for comparing experimental signals to reference signals. I initially calculated the relative error at each (shifted) time index between a reference and an experimental signal, then averaged that error across the signal to get a single match score, and used that to rank and plot the top two matches per reference.
 
The relative error approach passed an initial eye test, but once I added a percentage fit metric, I saw the fits were low (at times ~50%) even for visually strong matches. That sent me looking for a better scoring approach, and I landed on R², a standard goodness-of-fit measurement I'm used to from ML work. Switching to R² significantly improved the fit scores into the high 90s in most cases, and around 78% at worst for the top 2 matches.
 
## How to Run
 
**Requirements:** Python 3.9+, with the following packages:
```
numpy
pandas
plotly
scikit-learn
```
Install with:
```
pip install numpy pandas plotly scikit-learn
```
 
**Run:**
```
python signal_match.py
```
This generates one HTML plot per reference signal in `data/plots/`, each showing the reference signal overlaid with its top 2 matching experimental signals, and prints runtime stats to the console.

## Findings 
- Average runtime per experimental signal match: ~0.0088 seconds
- Total program runtime (all 4 references × 40 experimental signals): ~1.5830 seconds
- Best R² fit observed: 99.03% (Reference 1 vs. Experimental 11)
- Weakest top-2 R² fit observed: 78.75% (Reference 3 vs. Experimental 12)

## Recomendations
Having more time I think this could be a python application or web app with a UI to upload reference and experimental signals. Additionally outputs could be added to .csv or .xlsx format to show the top signals along with their r^2 score. Additionnally further investigations could be made to improve runtime.