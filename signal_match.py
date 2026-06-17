from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import r2_score

TIME_COL = "Time"
VALUE_COL = "Intensity"
REF_DATA = "data/signal_data/reference/"
EXP_DATA = "data/signal_data/experimental/"
PLOT_PATH = "data/plots/"


def get_files(data_path):
	"""
	Get all files in a directory
	Args:
		data_path (str): path to directory to get files from
	Returns:
		list: list of file names
	"""

	# Get all items that are files
	return [f.name for f in Path(data_path).iterdir() if f.is_file()]


def evaluate_signal_match(ref_values, exp_values):
	"""
	Evaluate the match between two signals using R^2 score
	Args:
		ref_values (np.array): reference signal values
		exp_values (np.array): experimental signal values
	Returns:
		float: R^2 score between the two signals
		float: time offset that gives the best match
	"""
	exp_scores = []

	# Apply all possible offsets
	for time_offset in range(50):
		offset_values = ref_values[time_offset : time_offset + 50]

		# calculate R^2 value for offset
		r2_score_value = r2_score(offset_values, exp_values)

		# calculate relative error for offset
		# relative_errors = np.abs(offset_values - exp_values) / np.abs(
		# 	offset_values
		# )
		# average_relative_error = 1 - np.average(relative_errors)

		exp_scores.append(r2_score_value)

	# return best time offset for exp signal and its score
	best_offset = np.argmax(exp_scores)
	return exp_scores[best_offset], best_offset


def evaluate_signal_match_rel_error(truth_values, measured_values):
	"""
	Evaluate the match between two signals using relative error
	Args:
		truth_values (np.array): true signal values
		measured_values (np.array): measured signal values
	Returns:
		float: R^2 score between the two signals
		float: time offset that gives the best match
	"""
	exp_scores = []

	# Apply all possible offsets
	for time_offset in range(50):
		truth_slice_values = truth_values[time_offset : time_offset + 50]

		exp_scores.append(1 - np.average(relative_errors))

	# return best time offset for exp signal and its relative error
	best_offset = np.argmax(exp_scores)
	return exp_scores[best_offset], best_offset


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
		ref_scores, time_offsets = [], []

		# Load in experimental signals
		for exp_file in experimental_files:
			exp_df = pd.read_csv(EXP_DATA + exp_file)
			exp_score, best_offset = evaluate_signal_match(
				ref_values, exp_df[VALUE_COL].to_numpy()
			)

			time_offsets.append(best_offset)
			ref_scores.append(exp_score)

		# Find top 2 signal match
		for _, best_match_idx in enumerate(
			reversed(np.argpartition(ref_scores, -2)[-2:])
		):
			exp_df = pd.read_csv(EXP_DATA + experimental_files[best_match_idx])
			percentage_fit = ref_scores[best_match_idx] * 100
			ref_fig.add_trace(
				go.Scatter(
					x=exp_df[TIME_COL] + time_offsets[best_match_idx],
					y=exp_df[VALUE_COL],
					name=f"Experimental Signal {best_match_idx}: {percentage_fit:.2f}%",
				)
			)

		ref_fig.update_layout(
			title="Top Two Measured Signals",
			xaxis_title=TIME_COL,
			yaxis_title=VALUE_COL,
		)

		# Save plot
		ref_fig.write_html(PLOT_PATH + ref_file.split(".")[0] + ".html")

		# print(p1_match, p2_match)
		# print(p1_diffs, p2_diffs)
