from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def get_files(data_path):
	# Get all items that are files
	return [f.name for f in Path(data_path).iterdir() if f.is_file()]


TIME_COL = "Time"
VALUE_COL = "Intensity"
REF_DATA = "data/signal_data/reference/"
EXP_DATA = "data/signal_data/experimental/"
PLOT_PATH = "data/plots/"

if __name__ == "__main__":

	# Fetch Signal Data
	reference_files = sorted(get_files(REF_DATA))
	experimental_files = sorted(get_files(EXP_DATA))

	# Load in reference signal
	for ref_file in reference_files:
		ref_fig = go.Figure()
		ref_df = pd.read_csv(REF_DATA + ref_file)

		# Add ref signal to plot
		ref_fig.add_trace(
			go.Scatter(
				x=ref_df[TIME_COL],
				y=ref_df[VALUE_COL],
				name="Reference Signal",
			)
		)

		# Split values into halves
		ref_values = ref_df[VALUE_COL].to_numpy()
		ref_diffs, time_offsets = [], []

		# Load in experimental signals
		for exp_file in experimental_files:
			exp_diffs = []
			exp_df = pd.read_csv(EXP_DATA + exp_file)
			exp_values = exp_df[VALUE_COL].to_numpy()

			# Apply all possible offsets
			for time_offset in range(50):
				offset_values = ref_values[time_offset : time_offset + 50]

				# calculate relative error for slice from reference signal
				exp_diffs.append(
					np.average(
						np.abs(exp_values - offset_values) / np.abs(offset_values)
					)
				)

			# Find best time offset for exp signal
			best_offset = np.argmin(exp_diffs)
			time_offsets.append(best_offset)
			ref_diffs.append(exp_diffs[best_offset])

		# Find top 2 signal match
		for idx, best_match_idx in enumerate(np.argpartition(ref_diffs, 2)[:2]):
			# best_match_idx = np.argmin(ref_diffs)
			exp_df = pd.read_csv(EXP_DATA + experimental_files[best_match_idx])
			ref_fig.add_trace(
				go.Scatter(
					x=exp_df[TIME_COL] + time_offsets[best_match_idx],
					y=exp_df[VALUE_COL],
					name=f"Experimental Signal {idx + 1}: {ref_diffs[best_match_idx] * 100}%",
				)
			)

		ref_fig.update_layout(title="Top Two Measured Signals", xaxis_title=TIME_COL, yaxis_title=VALUE_COL)

		# Save plot
		ref_fig.write_html(PLOT_PATH + ref_file.split(".")[0] + ".html")

		# print(p1_match, p2_match)
		# print(p1_diffs, p2_diffs)
