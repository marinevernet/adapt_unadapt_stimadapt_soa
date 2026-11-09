import numpy as np
import pandas as pd
import os
import os.path as op
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import glob
import warnings

# For linear mixed models
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

from scipy.stats import shapiro, ttest_rel, ttest_1samp, wilcoxon, rankdata, chi2
from scipy.signal import butter, filtfilt
from statsmodels.stats.multitest import multipletests

############# FUNCTIONS ###############

def detect_and_repair_artifacts(trial, printing=False):
    x = np.array(trial.strip("[]").split(",")).astype(float)

    # Calculate velocity and set threshold
    diffs = np.diff(x)
    # Threshold: 2x the standard deviation of velocity for a data-driven approach.
    threshold = 2 * np.std(diffs) 

    # The "Verify Return" loop
    repaired_indices = []
    # We loop through the differences to find a 'spike'
    # A spike is a huge jump out, followed immediately by a huge jump back.
    for i in range(len(diffs) - 1):
        v1 = diffs[i]     # Velocity into the point
        v2 = diffs[i+1]   # Velocity out of the point
        
        # Check if v1 is a massive jump
        if abs(v1) > threshold:
            # Verify Return: Is the next move opposite and roughly equal?
            # This confirms it's a 1-sample artifact and not a fast intentional move.
            if np.sign(v1) != np.sign(v2) and abs(v2) > (threshold * 0.8):
                
                # Linear Interpolation: Replace the artifact with the average 
                # of the point before and the point after.
                artifact_index = i + 1
                x[artifact_index] = (x[i] + x[i+2]) / 2
                
                repaired_indices.append(artifact_index)

    total_samples = len(x)
    num_repaired = len(repaired_indices)
    percent_altered = (num_repaired / total_samples) * 100

    if printing:
        print(f"Artifacts found at indices: {repaired_indices}")
        print(f"Percentage of data altered: {percent_altered:.4f}%")
        print(f"Threshold used: {threshold} pixels/sample")

    return x

def parse_list(text):
    # The trajectories are saved by PsychoPy as text: "[x1, x2, ...]"
    return np.array(text.strip("[]").split(",")).astype(float)

# ---------- Old cleaning (first version), kept for comparison ----------

# Trials (index within the participant, both sessions) whose first samples were reset by hand, and number of samples reset
# (in the old cleaning, the first 10 samples of all the trials are reset; s033 trial 137 was commented out)
OLD_START_RESET = {
    "s034": {81: 15},
    "s036": {120: 12, 143: 13, 161: 12},
    "s037": {15: 12, 162: 15, 186: 15},
    "s038": {30: 15, 202: 13},
    "s039": {97: 12},
    "s042": {36: 14},
    "s043": {59: 15},
    "s044": {53: 13},
    "s048": {178: 13, 197: 12, 202: 14},
    "s049": {31: 15, 81: 12},
    "s054": {79: 14, 146: 14, 174: 14},
    "s055": {164: 14, 227: 30},
}
# Trials removed by hand
OLD_REMOVED = {
    "s034": [217], "s035": [56], "s036": [64, 67, 86, 118, 129, 187], "s037": [69, 109, 121],
    "s039": [3, 31, 56, 161], "s040": [24, 25, 65], "s041": [80, 231], "s042": [223], "s043": [124, 144],
    "s044": [226, 228], "s045": [23], "s046": [109], "s047": [102], "s048": [4, 96, 188, 211, 214],
    "s049": [105], "s050": [45], "s051": [61, 92, 120, 133, 155, 190, 212, 213], "s052": [181],
    "s053": [61], "s054": [206], "s056": [12],
}

def clean_trajectory_old(x_text, y_text, participant, index_trial):
    """
    First version of the cleaning: repair of the spikes, reset of the first 10 samples (more for some trials), manual removal.
    Returns x, y and the reason for the exclusion (None if the trial is kept).
    """
    if index_trial in OLD_REMOVED.get(participant, []):
        return None, None, 'removed by hand'
    x = detect_and_repair_artifacts(x_text)
    y = detect_and_repair_artifacts(y_text)
    n_reset = OLD_START_RESET.get(participant, {}).get(index_trial, 10)
    x[0:n_reset] = START_X
    y[0:n_reset] = START_Y
    return x, y, None

def movement_parameters_old(x, y, t):
    """
    First version of the movement parameters: computed on the raw samples, without filtering.
    Movement start / end: first / last sample with a change of position.
    """
    dx, dy, dt = np.diff(x), np.diff(y), np.diff(t)
    vx, vy = dx/dt, dy/dt
    speeds = np.sqrt(vx**2 + vy**2)
    ax, ay = np.diff(vx)/dt[:-1], np.diff(vy)/dt[:-1]
    accel_magnitudes = np.sqrt(ax**2 + ay**2)
    path_length = np.sum(np.sqrt(dx**2 + dy**2))
    straight_line_distance = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2)

    moving = np.where((x != x[0]) | (y != y[0]))[0]
    idx_move_start = moving[0]
    idx_move_end = max(np.where(x != x[-1])[0][-1], np.where(y != y[-1])[0][-1] if np.any(y != y[-1]) else 0)
    idx_peak_speed = np.argmax(speeds)

    return {
        "peak_speed": np.max(speeds),
        "peak_acceleration": np.max(accel_magnitudes),
        "mean_speed": np.mean(speeds[speeds > 0]),
        "mean_acceleration": np.mean(accel_magnitudes[accel_magnitudes > 0]),
        "path_length": path_length,
        "tortuosity": path_length/straight_line_distance if straight_line_distance != 0 else np.inf,
        "overshoot": detect_right_side_overshoot(x, y, x0=0, y0=0, r=2)["any_right_overshoot"],
        "movement_duration": t[idx_move_end+1] - t[idx_move_start],
        "pause_beginning_duration": t[idx_move_start],
        "acceleration_time": t[idx_peak_speed] - t[idx_move_start],
        "onset_time": t[idx_move_start],
        "offset_time": t[idx_move_end+1],
    }

# ---------- New cleaning ----------

def clean_trajectory_new(x_raw, y_raw, t):
    """
    At the beginning of many trials (28%), the position of the cursor stays frozen at its previous position
    (far from the start) for 1 to 29 frames, then comes back to the start position (cursor set by PsychoPy).
    These frozen samples are replaced by a linear interpolation between the start position and the first valid sample.
    The trial is excluded if the cursor was already far from the start at the first valid sample
    (the movement started during the frozen samples, so its onset and peak speed are unknown),
    or if there is an implausible jump later in the trial (none in the data).
    Returns x, y, the number of frozen samples, and the reason for the exclusion (None if the trial is kept).
    """
    x, y = x_raw.copy(), y_raw.copy()

    # Frozen samples: identical to sample 1, and more than 1 cm from the start
    n_frozen = 0
    if np.hypot(x[1] - START_X, y[1] - START_Y) > 1:
        n_frozen = 1
        while n_frozen + 1 < len(x) and x[n_frozen+1] == x[1] and y[n_frozen+1] == y[1]:
            n_frozen += 1
    if n_frozen > 0:
        first_valid = n_frozen + 1
        if first_valid >= len(x):
            return None, None, n_frozen, 'frozen until the end'
        if np.hypot(x[first_valid] - START_X, y[first_valid] - START_Y) > MAX_DISTANCE_AFTER_FROZEN:
            return None, None, n_frozen, 'movement started during the frozen samples'
        x[1:first_valid] = np.interp(t[1:first_valid], [t[0], t[first_valid]], [x[0], x[first_valid]])
        y[1:first_valid] = np.interp(t[1:first_valid], [t[0], t[first_valid]], [y[0], y[first_valid]])

    # Safety check: implausible jump between two frames
    if np.max(np.hypot(np.diff(x), np.diff(y))) > MAX_JUMP:
        return None, None, n_frozen, 'jump larger than %g cm in one frame' %(MAX_JUMP)

    return x, y, n_frozen, None

def movement_parameters_new(x, y, t):
    """
    Movement parameters on the cleaned trajectory.
    Speed and acceleration: the positions are resampled at 60 Hz (a few frames are late), low-pass filtered
    (Butterworth, 4th order, 10 Hz, forward and backward, so without delay), then differentiated.
    Movement onset: speed crossing 5% of the peak speed, before the peak.
    Movement offset: last time the speed is above 5% of the peak speed, so that the corrective movements are included
    (offset = end of the recording if the participant clicked while still moving).
    Path length, tortuosity and overshoot: on the cleaned (not filtered) positions.
    """
    t_regular = np.arange(t[0], t[-1] + 1e-9, 1/SAMPLING_RATE)
    b, a = butter(4, CUTOFF_FREQUENCY/(SAMPLING_RATE/2))
    x_filtered = filtfilt(b, a, np.interp(t_regular, t, x))
    y_filtered = filtfilt(b, a, np.interp(t_regular, t, y))

    vx, vy = np.gradient(x_filtered, 1/SAMPLING_RATE), np.gradient(y_filtered, 1/SAMPLING_RATE)
    speed = np.hypot(vx, vy)
    acceleration = np.hypot(np.gradient(vx, 1/SAMPLING_RATE), np.gradient(vy, 1/SAMPLING_RATE))

    idx_peak = np.argmax(speed)
    threshold = ONSET_THRESHOLD*speed[idx_peak]
    below_before = np.where(speed[:idx_peak] < threshold)[0]
    idx_onset = below_before[-1] + 1 if len(below_before) else 0
    # Offset after the last sample above the threshold, so that the corrective movements are included
    idx_offset = min(np.where(speed >= threshold)[0][-1] + 1, len(speed) - 1)
    during = slice(idx_onset, idx_offset + 1)

    path_length = np.sum(np.hypot(np.diff(x), np.diff(y)))
    straight_line_distance = np.hypot(x[-1] - x[0], y[-1] - y[0])

    return {
        "peak_speed": speed[idx_peak],
        "peak_acceleration": np.max(acceleration[during]),
        "mean_speed": np.mean(speed[during]),
        "mean_acceleration": np.mean(acceleration[during]),
        "path_length": path_length,
        "tortuosity": path_length/straight_line_distance if straight_line_distance != 0 else np.inf,
        "overshoot": detect_right_side_overshoot(x, y, x0=0, y0=0, r=NOSE_RADIUS)["any_right_overshoot"],
        "movement_duration": t_regular[idx_offset] - t_regular[idx_onset],
        "pause_beginning_duration": t_regular[idx_onset],
        "acceleration_time": t_regular[idx_peak] - t_regular[idx_onset],
        "onset_time": t_regular[idx_onset],
        "offset_time": t_regular[idx_offset],
    }

def plot_cleaning_examples(examples, file_name):
    """
    x and y over time for a few trials: raw, after the old cleaning, after the new cleaning.
    examples: list of (title, participant, index_trial, x_raw text, y_raw text, t)
    """
    fig, axes = plt.subplots(len(examples), 3, figsize=(15, 3.0*len(examples)), sharex='row', sharey='row')
    for row, (title, participant, index_trial, x_text, y_text, t) in enumerate(examples):
        x_raw, y_raw = parse_list(x_text), parse_list(y_text)
        x_old, y_old, excluded_old = clean_trajectory_old(x_text, y_text, participant, index_trial)
        x_new, y_new, _, excluded_new = clean_trajectory_new(x_raw, y_raw, t)
        for column, (x, y, excluded, method) in enumerate([(x_raw, y_raw, None, 'Raw'),
                                                            (x_old, y_old, excluded_old, 'Old cleaning'),
                                                            (x_new, y_new, excluded_new, 'New cleaning')]):
            ax = axes[row, column]
            if excluded is not None:
                ax.text(0.5, 0.5, 'Trial excluded:\n' + excluded, transform=ax.transAxes, ha='center', va='center', fontsize=11)
            else:
                ax.plot(t*1000, x, '.-', color='tab:blue', label='x', markersize=4)
                ax.plot(t*1000, y, '.-', color='tab:red', label='y', markersize=4)
                parameters = movement_parameters_old(x, y, t) if column == 1 else (movement_parameters_new(x, y, t) if column == 2 else None)
                if parameters is not None: # Movement onset and offset found by each method
                    for time in [parameters['onset_time'], parameters['offset_time']]:
                        ax.axvline(time*1000, color='gray', linestyle='--', linewidth=1)
            if row == 0:
                ax.set_title(method, fontsize=13, fontweight='bold', pad=28)
            ax.grid(True, alpha=0.3)
            if column == 0:
                ax.set_ylabel('Position (cm)', fontsize=10)
                # Description of the example, above the row
                ax.text(0, 1.06, '%s, trial %d: %s' %(participant, index_trial, title), transform=ax.transAxes,
                        ha='left', va='bottom', fontsize=11)
            if row == len(examples) - 1:
                ax.set_xlabel('Time since the moose appeared (ms)')
    axes[0, 0].legend(loc='center right', fontsize=9)
    fig.text(0.5, 0.995, 'Dashed lines: movement onset and offset found by each method', ha='center', va='top', fontsize=11)
    # Spacing set by hand (tight_layout would make room for the long descriptions above the rows)
    fig.subplots_adjust(left=0.06, right=0.99, bottom=0.04, top=0.94, hspace=0.6, wspace=0.12)
    fig.savefig(op.join(figures_folder, file_name), dpi=150, bbox_inches='tight')
    plt.close(fig)
def detect_right_side_overshoot(x, y, x0, y0, r):
    """
    Detect whether cursor goes beyond the right boundary of a circle.

    Parameters
    ----------
    x, y : array-like
        Cursor trajectory
    x0, y0 : float
        Circle center
    r : float
        Circle radius

    Returns
    -------
    dict with:
        any_right_overshoot (bool)
        overshoot_indices (np.ndarray)
        max_overshoot_distance (float)
    """

    x = np.asarray(x)
    y = np.asarray(y)

    dy2 = (y - y0)**2

    # valid region where circle boundary exists
    inside_vertical_span = dy2 <= r**2

    # initialize boundary with NaN for invalid y
    x_right = np.full_like(x, np.nan, dtype=float)

    # compute boundary only where valid
    valid = inside_vertical_span
    x_right[valid] = x0 + np.sqrt(r**2 - dy2[valid])

    # overshoot condition (only meaningful where valid)
    overshoot = valid & (x > x_right)

    if not np.any(overshoot):
        return {
            "any_right_overshoot": False,
            "overshoot_indices": np.array([]),
            "max_overshoot_distance": 0.0
        }

    overshoot_distance = x - x_right
    overshoot_distance[~overshoot] = 0

    return {
        "any_right_overshoot": True,
        "overshoot_indices": np.where(overshoot)[0],
        "max_overshoot_distance": float(np.max(overshoot_distance))
    }

def save_summary_figure(result, file_name):
    # Figure with the summary of the model
    summary_text = result.summary().as_text()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')  # Hide axes
    ax.text(0, 1, summary_text, fontsize=10, va='top', family='monospace')
    plt.tight_layout()
    fig.savefig(op.join(figures_folder, file_name), dpi=150, bbox_inches='tight')
    plt.close(fig)

def plot_coefficients(result, file_name):
    """
    Coefficient plot: each fixed effect (except the intercept) as a dot with its 95% confidence interval.
    Black: significant (the interval does not include 0); gray: not significant.
    """
    readable_names = {
        'stim': 'Stimulation (rAG vs sham)',
        'delay': 'Delay',
        'delay:stim': 'Stimulation × delay',
        'block': 'Block',
        'pause_w': 'Pause before movement (within)',
        'duration_w': 'Movement duration (within)',
        'speed_w': 'Peak speed (within)',
        'pause_b': 'Pause before movement (between)',
        'duration_b': 'Movement duration (between)',
        'speed_b': 'Peak speed (between)',
    }

    # Same order in all figures: the experimental effects first, then the movement parameters
    effects = [name for name in readable_names if name in result.fe_params.index]
    effects += [name for name in result.fe_params.index if name not in effects and name != 'Intercept']
    estimates = result.fe_params[effects]
    ci = result.conf_int().loc[effects]
    pvalues = result.pvalues[effects]

    fig, ax = plt.subplots(figsize=(8, 0.5*len(effects) + 1.5))
    ax.axvline(0, color='gray', linestyle='--', linewidth=1)
    for position, effect in enumerate(effects[::-1]): # From top to bottom in the order of the model
        color = 'black' if pvalues[effect] < 0.05 else 'darkgray'
        ax.plot([ci.loc[effect, 0], ci.loc[effect, 1]], [position, position], color=color, linewidth=2)
        ax.plot(estimates[effect], position, 'o', color=color, markersize=8)
        ax.text(1.02, position, 'p = %.3f' %(pvalues[effect]) if pvalues[effect] >= 0.001 else 'p < .001',
                transform=ax.get_yaxis_transform(), va='center', fontsize=11, color=color)
    ax.set_yticks(range(len(effects)))
    ax.set_yticklabels([readable_names.get(effect, effect) for effect in effects[::-1]], fontsize=12)
    ax.set_xlabel('Coefficient (standardized rating) and 95% CI', fontsize=12)
    ax.tick_params(axis='x', labelsize=11)
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    fig.savefig(op.join(figures_folder, file_name), dpi=300, bbox_inches='tight')
    plt.close(fig)

class Tee:
    """
    Write what is printed both to the console and to a file
    """

    def __init__(self, file_path):
        self.console = sys.stdout
        self.file = open(file_path, 'w', encoding='utf-8')

    def write(self, text):
        self.console.write(text)
        self.file.write(text)

    def flush(self):
        self.console.flush()
        self.file.flush()

############### PARAMETERS ###############

# adapt_unadapt_stimadapt_soa is the parent of the analysis folder containing this script
project_folder = op.dirname(op.dirname(op.abspath(__file__)))
path_data = op.join(project_folder, "DATA", "stim_adapt")
blind_file = op.join(project_folder, "psychopy", "stim_adapt", "blind", "double_blind.csv")
results_folder = op.join(project_folder, "results", "movement")
figures_folder = op.join(project_folder, "figures", "movement")
os.makedirs(results_folder, exist_ok=True)
os.makedirs(figures_folder, exist_ok=True)

# Cleaning of the trajectories: 'new' (automatic rules, see clean_trajectory_new) or 'old' (first version, with corrections by hand)
cleaning_method = 'new'
START_X, START_Y = -9.71875, 0 # Start position of the cursor (cm), as recorded
NOSE_RADIUS = 1.85 # cm
MAX_DISTANCE_AFTER_FROZEN = 0.5 # cm: trials excluded if the cursor is further from the start at the end of the frozen samples
MAX_JUMP = 6 # cm: trials excluded if the cursor moves more than this in one frame (largest real movement: 5.3 cm)
SAMPLING_RATE = 60 # Hz
CUTOFF_FREQUENCY = 10 # Hz, low-pass filter before computing speed and acceleration
ONSET_THRESHOLD = 0.05 # Movement onset / offset: speed crossing this proportion of the peak speed

participants = [
    "s033", "s034", "s035", "s036", "s037", "s038",
    "s039", "s040", "s041", "s042", "s043", "s044",
    "s045", "s046", "s047", "s048", "s049", "s050",
    "s051", "s052", "s053", "s054", "s055", "s056",]

sessions = ['session1', 'session2']
sessions_cap = ['Session1', 'Session2']

################## MAIN ######################

# Everything printed from now on is also saved in a text file
sys.stdout = Tee(op.join(results_folder, "statistics_output_movement.txt"))

Blinding_file = pd.read_csv(blind_file, sep=",")

list_df_all_participants = []

for n_participant, participant in enumerate(participants):

    for n_session, session in enumerate(sessions):

        file_load = glob.glob(op.join(path_data, participant, session, "*clean.csv"))
        df_participant = pd.read_csv(file_load[0], sep=",")
        df_participant.insert(0, "participant_id", participant)

        # Add the session type for every trial
        # The blind code is the prefix of the file name (F1_session1_..., F10_session1_...)
        # (searching for the code in the file name matched F10, F11, F12 to F1, and M10, M11, M12 to M1)
        blind_code = op.basename(file_load[0]).split("_")[0]

        stim_type_name = Blinding_file.loc[Blinding_file["Participant"] == blind_code, sessions_cap[n_session]].iloc[0]
        if stim_type_name[-1] == 'A' :
            stim_type = 'real'
        elif stim_type_name[-1] == 'B':
            stim_type = 'sham'

        df_participant.insert(1, "stim_type", stim_type)

        list_df_all_participants.append(df_participant)


df_all_participant = pd.concat(list_df_all_participants, ignore_index=True)
df_test_trials = df_all_participant[df_all_participant["block_type"] == "test"]

# # remove useless columns
df_test_trials_clean = df_test_trials.drop(columns=["date", "number (1-12)", "expName", "psychopyVersion"])
df_all_participant_clean = df_all_participant.drop(columns=["date", "number (1-12)", "expName", "psychopyVersion"])

df_test_trials_clean['rating'] = (df_test_trials_clean['rating']
                        .astype(float))
# Only keep correct trials (click on time on the target)
df_test_trials_clean = df_test_trials_clean[df_test_trials_clean["click"] == 'inside']

# ************* Cleaning of the trajectories and movement parameters of each trial *************

list_df_test_processed = []
exclusions = {'old': {}, 'new': {}} # Reason for the exclusion: number of trials
n_frozen_all = [] # Number of frozen samples at the beginning of each trial
n_trials_old_artifact_left = 0 # Trials in which the old cleaning left frozen samples (more than the samples reset)

for participant in participants:
    df_tmp = df_test_trials_clean[df_test_trials_clean["participant_id"] == participant]

    keep = []
    list_parameters = []
    for index_trial, (x_text, y_text, t_text) in enumerate(zip(df_tmp["mouse.x"], df_tmp["mouse.y"], df_tmp["mouse.time"])):
        t = parse_list(t_text) # time in second for each sample, since the moose appeared

        # Old cleaning, only to count its exclusions (and to compute its parameters if cleaning_method == 'old')
        x_old, y_old, excluded_old = clean_trajectory_old(x_text, y_text, participant, index_trial)
        if excluded_old is not None:
            exclusions['old'][excluded_old] = exclusions['old'].get(excluded_old, 0) + 1

        # New cleaning
        x_new, y_new, n_frozen, excluded_new = clean_trajectory_new(parse_list(x_text), parse_list(y_text), t)
        n_frozen_all.append(n_frozen)
        if excluded_new is not None:
            exclusions['new'][excluded_new] = exclusions['new'].get(excluded_new, 0) + 1
        if excluded_old is None and n_frozen + 1 > OLD_START_RESET.get(participant, {}).get(index_trial, 10):
            n_trials_old_artifact_left += 1

        if cleaning_method == 'new':
            excluded = excluded_new
            if excluded is None:
                list_parameters.append(movement_parameters_new(x_new, y_new, t))
        else:
            excluded = excluded_old
            if excluded is None:
                list_parameters.append(movement_parameters_old(x_old, y_old, t))
        keep.append(excluded is None)

    # Keep the trials that are not excluded, and add their movement parameters
    df_tmp_cleaned = pd.concat([df_tmp[keep].reset_index(drop=True), pd.DataFrame(list_parameters)], axis=1)
    list_df_test_processed.append(df_tmp_cleaned)

n_frozen_all = np.array(n_frozen_all)
print("\n*************** Cleaning of the trajectories (method used: %s) ***************" %(cleaning_method))
print("Trials: %d" %(len(n_frozen_all)))
print("Trials with frozen samples at the beginning: %d (%.1f%%); 1 sample: %d; 2 to %d samples: %d" %(
    (n_frozen_all > 0).sum(), 100*(n_frozen_all > 0).mean(), (n_frozen_all == 1).sum(), n_frozen_all.max(), (n_frozen_all > 1).sum()))
for method in ['old', 'new']:
    n_excluded = sum(exclusions[method].values())
    print("%s cleaning: %d trials excluded (%.1f%%) %s" %(method.capitalize(), n_excluded, 100*n_excluded/len(n_frozen_all), exclusions[method]))
print("Old cleaning: %d kept trials still contain frozen samples (more than the samples reset)" %(n_trials_old_artifact_left))

# ************* Figure: examples of trajectories before and after the cleaning *************

example_trials = [
    ('frozen for 1 sample (the most frequent case)', 's033', 0),
    ('frozen for 29 samples (corrected by hand in the old cleaning)', 's055', 227),
    ('frozen for 14 samples (removed by hand in the old cleaning)', 's036', 64),
    ('frozen for 10 samples (correction commented out in the old cleaning)', 's033', 137),
    ('movement started while frozen (excluded in the new cleaning)', 's045', 23),
    ('small offset at the start (the old reset of 10 samples creates a jump, taken as the movement onset)', 's041', 171),
    ('real sample changed by the old spike repair (y, at about 470 ms)', 's035', 4),
]
examples = []
for title, participant, index_trial in example_trials:
    trial = df_test_trials_clean[df_test_trials_clean["participant_id"] == participant].iloc[index_trial]
    examples.append((title, participant, index_trial, trial["mouse.x"], trial["mouse.y"], parse_list(trial["mouse.time"])))
plot_cleaning_examples(examples, "cleaning_examples.png")

df_test_processed = pd.concat(list_df_test_processed, ignore_index=True)

# Save the movement parameters of each trial (without the trajectories, which are in the data files)
df_test_processed.drop(columns=["mouse.x", "mouse.y", "mouse.leftButton", "mouse.midButton", "mouse.rightButton", "mouse.time"],
                       errors="ignore").to_csv(op.join(results_folder, "movement_parameters_per_trial.csv"), index=False)

# ************* Did the stimulation change the movements? (rAG vs sham, paired, one mean per participant) *************

# All the kept trials: the movement is made before the bellow, so it does not depend on the delay
movement_variables = {
    'pause_beginning_duration': ('Pause before movement', 's'),
    'movement_duration': ('Movement duration', 's'),
    'acceleration_time': ('Acceleration time', 's'),
    'clickTime': ('Click time', 's'),
    'peak_speed': ('Peak speed', 'cm/s'),
    'mean_speed': ('Mean speed', 'cm/s'),
    'peak_acceleration': ('Peak acceleration', 'cm/s²'),
    'path_length': ('Path length', 'cm'),
    'tortuosity': ('Tortuosity', ''),
    'overshoot': ('Overshoot', 'proportion of trials'),
}
df_movement = df_test_processed.copy()
df_movement['overshoot'] = df_movement['overshoot'].astype(float)
means = df_movement.groupby(['participant_id', 'stim_type'])[list(movement_variables)].mean().unstack('stim_type')
means.to_csv(op.join(results_folder, "movement_parameters_per_participant.csv"))

rows = []
for variable, (label, unit) in movement_variables.items():
    real, sham = means[(variable, 'real')], means[(variable, 'sham')]
    difference = real - sham
    normal = shapiro(difference)[1] > 0.05
    if normal:
        test = ttest_rel(real, sham)
        statistic = 't(%d) = %.2f' %(len(difference) - 1, test.statistic)
        effect_size = 'd = %.2f' %(difference.mean()/difference.std(ddof=1))
    else:
        test = wilcoxon(real, sham, zero_method='zsplit')
        statistic = 'W = %.1f' %(test.statistic)
        # Rank-biserial correlation (positive: rAG > sham)
        ranks = rankdata(np.abs(difference))
        effect_size = 'r_rb = %.2f' %((ranks[difference > 0].sum() - ranks[difference < 0].sum())/ranks.sum())
    rows.append({'Parameter': label, 'Unit': unit, 'rAG': '%.3g ± %.2g' %(real.mean(), real.std()),
                 'Sham': '%.3g ± %.2g' %(sham.mean(), sham.std()), 'Shapiro p': round(shapiro(difference)[1], 3),
                 'Test': statistic, 'p': test.pvalue, 'Effect size': effect_size})
df_stim_movement = pd.DataFrame(rows)
df_stim_movement['p (Holm)'] = multipletests(df_stim_movement['p'], method='holm')[1]
print("\n*************** Movement parameters: rAG vs sham (paired, two-sided, Holm correction across the %d parameters) ***************" %(len(rows)))
print(df_stim_movement.round(3).to_string(index=False))
df_stim_movement.to_csv(op.join(results_folder, "movement_rAG_vs_sham.csv"), index=False)

# Figure: one panel per parameter, each participant as two points (rAG, sham) joined by a line
fig, axes = plt.subplots(2, 5, figsize=(17, 7))
for ax, (variable, (label, unit)), p_holm in zip(axes.flat, movement_variables.items(), df_stim_movement['p (Holm)']):
    for _, row in means.iterrows():
        ax.plot([0, 1], [row[(variable, 'real')], row[(variable, 'sham')]], color='gray', alpha=0.6, linewidth=1)
    ax.scatter(np.zeros(len(means)), means[(variable, 'real')], color=(0.2, 0.7, 0.2), s=25, zorder=3)
    ax.scatter(np.ones(len(means)), means[(variable, 'sham')], color=(0.3, 0.5, 1.0), s=25, zorder=3)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['rAG\nstim.', 'Sham\nstim.'], fontsize=11)
    ax.set_xlim(-0.4, 1.4)
    ax.set_title('%s\np (Holm) = %.2f' %(label, p_holm), fontsize=12)
    ax.set_ylabel(unit, fontsize=10)
    ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
fig.savefig(op.join(figures_folder, "movement_rAG_vs_sham.png"), dpi=300, bbox_inches='tight')
plt.close(fig)

# ************* Do the movements predict the ratings, trial by trial? (exploratory) *************

# Three movement parameters chosen in advance, one per aspect of the movement (not redundant):
# pause before movement (preparation), movement duration (execution), peak speed (vigor)
model_variables = {'pause_beginning_duration': 'pause', 'movement_duration': 'duration', 'peak_speed': 'speed'}

# Same delays as for R: 50 to 250 ms
# (the trials with the bellow before the click, -1, are already removed, as there is no click inside the nose)
df_LMM = df_test_processed[~df_test_processed['scheduled_sound_delay'].isin([0, 1.25])].copy()
df_LMM['stim'] = df_LMM['stim_type'].map({'sham': 0, 'real': 1})
df_LMM['block'] = df_LMM['block_nb']
zscore = lambda values: (values - values.mean())/values.std()
df_LMM['rating_z'] = zscore(df_LMM['rating'])
df_LMM['delay'] = zscore(df_LMM['scheduled_sound_delay'])
# Within-participant (_w): deviation of the trial from the mean of the participant (trial-by-trial link with the rating)
# Between-participant (_b): mean of the participant (do the participants who move differently rate differently?)
for variable, name in model_variables.items():
    participant_mean = df_LMM.groupby('participant_id')[variable].transform('mean')
    df_LMM[name + '_w'] = zscore(df_LMM[variable] - participant_mean)
    df_LMM[name + '_b'] = zscore(participant_mean)
within = [name + '_w' for name in model_variables.values()]
between = [name + '_b' for name in model_variables.values()]
print("\n*************** Movement parameters and ratings: %d trials, delays 50-250 ms ***************" %(len(df_LMM)))

# Collinearity of the movement predictors
vif_matrix = np.column_stack([np.ones(len(df_LMM)), df_LMM[within + between].values])
print("Variance inflation factors: " + ", ".join('%s %.2f' %(name, variance_inflation_factor(vif_matrix, i + 1))
                                                 for i, name in enumerate(within + between)))

base_formula = "rating_z ~ delay*stim + block + " + " + ".join(between)
full_formula = base_formula + " + " + " + ".join(within)

def fit_mixed_model(formula, re_formula="~delay*stim", vc_formula=None, reml=True):
    # Returns the fit and the list of the warnings (convergence, boundary)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        fit = smf.mixedlm(formula, df_LMM, groups=df_LMM['participant_id'], re_formula=re_formula, vc_formula=vc_formula).fit(reml=reml)
    messages = sorted(set(str(warning.message) for warning in caught
                          if 'converge' in str(warning.message) or 'boundary' in str(warning.message) or 'Hessian' in str(warning.message)))
    return fit, messages

# Random effects: from the maximal structure to simpler ones, until the model converges without warning
# (stimulation x delay is always kept: without it, its fixed effect is tested as if all trials were independent)
random_structures = [
    ('maximal: random slopes for delay x stimulation and for the movement parameters, correlated',
     "~delay*stim + " + " + ".join(within), None),
    ('random slopes for the movement parameters, not correlated',
     "~delay*stim", {name: '0 + ' + name for name in within}),
    ('no random slopes for the movement parameters', "~delay*stim", None),
]
for description, re_formula, vc_formula in random_structures:
    result, messages = fit_mixed_model(full_formula, re_formula, vc_formula)
    print("\nRandom structure: %s\n  converged: %s; warnings: %s" %(description, result.converged, messages if messages else 'none'))
    if result.converged and not messages:
        break
print("\n*************** Model kept ***************")
print(result.summary())
save_summary_figure(result, "LMM_movement_model.png")
plot_coefficients(result, "LMM_movement_model_coefficients.png")

p_within = result.pvalues[within]
print("Within-participant movement effects, Holm correction: " + ", ".join(
    '%s p = %.3f' %(name, p) for name, p in zip(within, multipletests(p_within, method='holm')[1])))

# One test for the three within-participant movement effects together (likelihood ratio, maximum likelihood)
full_ml, messages_full = fit_mixed_model(full_formula, re_formula, vc_formula, reml=False)
reduced_ml, messages_reduced = fit_mixed_model(base_formula, re_formula, vc_formula, reml=False)
lr_statistic = 2*(full_ml.llf - reduced_ml.llf)
print("Likelihood ratio test, the 3 within-participant movement effects together: chi2(%d) = %.2f, p = %.3f (warnings: %s)" %(
    len(within), lr_statistic, chi2.sf(lr_statistic, len(within)), messages_full + messages_reduced if messages_full + messages_reduced else 'none'))

# Two-stage approach (check): regression within each participant and session, then test across the participants
coefficients = []
for (participant, stim), df_session in df_LMM.groupby(['participant_id', 'stim']):
    fit = smf.ols("rating_z ~ delay + " + " + ".join(within), df_session).fit()
    coefficients.append({'participant': participant, 'stim': stim, **fit.params[within]})
coefficients = pd.DataFrame(coefficients).groupby('participant')[within].mean() # Mean of the two sessions
print("\nTwo-stage approach (one coefficient per participant, mean of the two sessions, n = %d):" %(len(coefficients)))
p_two_stage = []
for name in within:
    values = coefficients[name]
    if shapiro(values)[1] > 0.05:
        test = ttest_1samp(values, 0)
        text = 't(%d) = %.2f, p = %.3f, d = %.2f' %(len(values) - 1, test.statistic, test.pvalue, values.mean()/values.std(ddof=1))
    else:
        test = wilcoxon(values)
        text = 'Wilcoxon W = %.0f, p = %.3f' %(test.statistic, test.pvalue)
    p_two_stage.append(test.pvalue)
    print("  %s: %.3f +/- %.3f; %s" %(name, values.mean(), values.std(), text))
print("  Holm correction: " + ", ".join('%s p = %.3f' %(name, p) for name, p in zip(within, multipletests(p_two_stage, method='holm')[1])))

# ************* Stop saving what is printed *************

sys.stdout.file.close()
sys.stdout = sys.stdout.console

