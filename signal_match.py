import time
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
		ref_values (np.array): reference signal values.
		exp_values (np.array): experimental signal values.
	Returns:
		tuple (float, int): R^2 score between the two signals and time offset that gives the best match,
		time offset that gives the best match.
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


if __name__ == "__main__":
	# Track program runtime
	program_start_time = time.perf_counter()
	run_times = []

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
				name="Ref Signal",
			)
		)

		# Split values into halves
		ref_values = ref_df[VALUE_COL].to_numpy()
		ref_scores, time_offsets = [], []

		# Load in experimental signals and evaluate match to reference signal
		for exp_file in experimental_files:
			exp_start_time = time.perf_counter()

			exp_df = pd.read_csv(EXP_DATA + exp_file)
			exp_score, best_offset = evaluate_signal_match(
				ref_values, exp_df[VALUE_COL].to_numpy()
			)

			# Store best score and time offset for experimental signal
			time_offsets.append(best_offset)
			ref_scores.append(exp_score)

			# Track runtime for each signal
			exp_end_time = time.perf_counter()
			run_times.append(exp_end_time - exp_start_time)

		# Find top 2 signal match
		for best_match_idx in reversed(np.argpartition(ref_scores, -2)[-2:]):
			exp_df = pd.read_csv(EXP_DATA + experimental_files[best_match_idx])
			percentage_fit = ref_scores[best_match_idx] * 100
			ref_fig.add_trace(
				go.Scatter(
					x=exp_df[TIME_COL] + time_offsets[best_match_idx],
					y=exp_df[VALUE_COL],
					name=f"Exp Signal {best_match_idx}: {percentage_fit:.2f}%",
				)
			)

		ref_fig.update_layout(
			title="Top Two Measured Signals",
			xaxis_title=TIME_COL,
			yaxis_title=VALUE_COL,
			hoverlabel={"namelength": -1},
		)

		# Save plot
		ref_fig.write_html(PLOT_PATH + ref_file.split(".")[0] + ".html")

	program_end_time = time.perf_counter()
	print(f"Average runtime per experimental signal: {np.mean(run_times):.4f} seconds")
	print(
		f"Total runtime of program: {program_end_time - program_start_time:.4f} seconds"
	)
