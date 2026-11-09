import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.stats import binomtest, shapiro, ttest_rel, wilcoxon, rankdata


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


# ==========================================
# Paths
# ==========================================

# adapt_unadapt_stimadapt_soa is the parent of the analysis folder containing this script
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
blinding_file = os.path.join(project_folder, 'DATA', 'stim_adapt', 'blinding_participants.csv')
results_folder = os.path.join(project_folder, 'results', 'blinding')
figures_folder = os.path.join(project_folder, 'figures', 'blinding')

os.makedirs(results_folder, exist_ok=True)
os.makedirs(figures_folder, exist_ok=True)

# Everything printed from now on is also saved in a text file
sys.stdout = Tee(os.path.join(results_folder, 'statistics_output.txt'))

# Comments that are not related to what happened during the stimulation (coded 0)
comments_not_during_stimulation = [('s055', 'S1'), ('s044', 'S2'), ('s054', 'S2')]

# ==========================================
# Load and reorganize the data
# ==========================================

df = pd.read_csv(blinding_file, dtype={'S1_comments': str, 'S2_comments': str})

# Which session was real, which one was sham
df['first_session'] = df['S1_truth'].map({'stim': 'real', 'sham': 'sham'})
real_session = np.where(df['first_session'] == 'real', 'S1', 'S2')
sham_session = np.where(df['first_session'] == 'real', 'S2', 'S1')

for condition, sessions in [('real', real_session), ('sham', sham_session)]:
    for time in ['before', 'after']:
        df[f'{condition}_{time}'] = [df.loc[i, f'{session}_{time}'] for i, session in zip(df.index, sessions)]
    df[f'{condition}_increase'] = df[f'{condition}_after'] - df[f'{condition}_before']

# Sensations reported during the stimulation, in each session
for session in ['S1', 'S2']:
    df[f'{session}_sensation_during'] = [
        (comment != '0') and ((participant, session) not in comments_not_during_stimulation)
        for participant, comment in zip(df['participant'], df[f'{session}_comments'])]
for condition, sessions in [('real', real_session), ('sham', sham_session)]:
    df[f'{condition}_sensation_during'] = [df.loc[i, f'{session}_sensation_during'] for i, session in zip(df.index, sessions)]

# The yes/no questions
questions = {
    'Increase\nafter\nrAG stim.': df['real_increase'] > 0,
    'Increase\nafter\nsham stim.': df['sham_increase'] > 0,
    'Sensations\nduring\nrAG stim.': df['real_sensation_during'],
    'Sensations\nduring\nsham stim.': df['sham_sensation_during'],
    'Noticed a\ndifference': df['notice_anything'] == 'oui',
    'Identified\nrAG stim.\nsession': df['S1_guess'] == df['S1_truth'],
}

# ==========================================
# Statistics
# ==========================================

print('N = %d participants (%d real first, %d sham first)' %(
    len(df), (df['first_session']=='real').sum(), (df['first_session']=='sham').sum()))

print('\n*************** Sensations (mean +/- SD, median) ***************')
for column in ['real_before', 'real_after', 'sham_before', 'sham_after', 'real_increase', 'sham_increase']:
    print('%s: %.2f +/- %.2f, median %.1f' %(column, df[column].mean(), df[column].std(), df[column].median()))
print('Same increase for real and sham: %d participants' %((df['real_increase'] == df['sham_increase']).sum()))

print('\n*************** Yes / No ***************')
for question, answer in questions.items():
    print('%s: yes %d, no %d' %(question.replace('\n', ' '), answer.sum(), (~answer).sum()))

for condition in ['real', 'sham']:
    print('Participants reporting sensations during the %s stimulation: %s' %(
        condition, ', '.join(df.loc[df[f'{condition}_sensation_during'], 'participant'])))

correct = df['S1_guess'] == df['S1_truth']
test = binomtest(int(correct.sum()), len(df), 0.5)
print('\nCorrect identification of the real session against chance (binomial test, two-sided): %d/%d, p=%.3g' %(
    correct.sum(), len(df), test.pvalue))


def paired_test(var1, var2, label):
    """
    Paired comparison (two-sided): paired t-test if the differences are normal (Shapiro), Wilcoxon signed-rank test otherwise.
    The ratings are integers, so many participants have a difference of 0: the Wilcoxon test uses the zero-split method,
    which keeps them (their ranks are split equally between the positive and negative sides), so that all participants are included.
    """
    difference = var1 - var2
    print('%s: %.2f +/- %.2f vs %.2f +/- %.2f' %(label, var1.mean(), var1.std(), var2.mean(), var2.std()))
    if shapiro(difference)[1] > 0.05:
        a = ttest_rel(var1, var2)
        print('   (Paired t-test): t(%d)=%.2f; p=%.3g; Cohen\'s d=%.2f' %(a.df, a.statistic, a.pvalue, np.abs(difference.mean()/difference.std(ddof=1))))
    else:
        a = wilcoxon(var1, var2, zero_method='zsplit')
        # Rank-biserial correlation, with the ranks of the zero differences split equally between both sides
        ranks = rankdata(np.abs(difference))
        positive = ranks[difference > 0].sum() + ranks[difference == 0].sum()/2
        negative = ranks[difference < 0].sum() + ranks[difference == 0].sum()/2
        print('   (Wilcoxon signed-rank test, zero-split, n=%d): W=%.1f; p=%.3g; effect size (RBC)=%.2f; participants with a difference of 0: %d' %(
            len(difference), a.statistic, a.pvalue, (positive - negative)/(positive + negative), (difference == 0).sum()))


def mcnemar_test(yes1, yes2, label):
    """
    Exact McNemar test (two-sided): binomial test on the participants who answered differently in the two sessions
    """
    only1 = int((yes1 & ~yes2).sum())
    only2 = int((~yes1 & yes2).sum())
    p = binomtest(only1, only1 + only2, 0.5).pvalue if only1 + only2 > 0 else 1
    print('%s: real yes %d, sham yes %d; yes for real only %d, yes for sham only %d; (exact McNemar test): p=%.3g' %(
        label, yes1.sum(), yes2.sum(), only1, only2, p))


print('\n*************** Real vs sham (paired, two-sided) ***************')
paired_test(df['real_before'], df['sham_before'], 'Sensation rating before, real vs sham')
paired_test(df['real_after'], df['sham_after'], 'Sensation rating after, real vs sham')
paired_test(df['real_increase'], df['sham_increase'], 'Change in sensation rating (after - before), real vs sham')

mcnemar_test(df['real_increase'] > 0, df['sham_increase'] > 0, 'Increase of sensations')
mcnemar_test(df['real_sensation_during'], df['sham_sensation_during'], 'Sensations reported during the stimulation')

print('\n*************** After vs before, within each session (paired, two-sided) ***************')
paired_test(df['real_after'], df['real_before'], 'Real: after vs before')
paired_test(df['sham_after'], df['sham_before'], 'Sham: after vs before')

# ==========================================
# Figure
# ==========================================

green = (0.2, 0.8, 0.2, 0.12)
blue = (0.3, 0.5, 1.0, 0.20)
order_styles = {'real': ('-', 'rAG first'), 'sham': (':', 'Sham first')}


def spread(values, step=0.045):
    """
    Horizontal offsets: the participants with the same rating are placed side by side, so that they can be counted
    """
    values = np.asarray(values)
    offsets = np.zeros(len(values))
    for value in np.unique(values):
        same = np.flatnonzero(values == value)
        offsets[same] = (np.arange(len(same)) - (len(same) - 1)/2) * step
    return offsets

fig, axes = plt.subplots(1, 2, figsize=(17, 7), gridspec_kw={'width_ratios': [1, 1.35]})

# ---------- Panel A: sensations before and after each session ----------
ax = axes[0]
columns = ['real_before', 'real_after', 'sham_before', 'sham_after']
palette = [green, green, blue, blue]
df_plot = df[columns].melt(var_name='condition', value_name='value')

sns.violinplot(data=df_plot, x='condition', y='value', hue='condition', legend=False, order=columns,
               inner='box', palette=palette, cut=0, ax=ax)

# Make the colors pale (seaborn does not apply the transparency of the palette)
for violin, color in zip(ax.collections, palette):
    violin.set_facecolor(color)

# Ratings are integers: participants with the same rating are spread horizontally
jitter = {column: spread(df[column].values) for column in columns}

for i, row in df.reset_index(drop=True).iterrows(): # For each participant
    linestyle = order_styles[row['first_session']][0]
    for first, second in [(0, 1), (2, 3)]:
        ax.plot([first + jitter[columns[first]][i], second + jitter[columns[second]][i]],
                [row[columns[first]], row[columns[second]]],
                color='gray', alpha=0.8, linewidth=1 if linestyle == '-' else 1.5, linestyle=linestyle)

for position, column in enumerate(columns):
    ax.scatter(position + jitter[column], df[column], color='black', s=22, zorder=3)

ax.set_xticks(range(4))
ax.set_xticklabels(['before', 'after', 'before', 'after'])
for position, label in [(0.5, 'rAG stimulation'), (2.5, 'Sham stimulation')]:
    ax.text(position, -0.13, label, transform=ax.get_xaxis_transform(), ha='center', va='top', fontsize=20)
ax.set_xlabel('')
ax.set_ylabel('Sensation rating', fontsize=20)
ax.tick_params(axis='both', labelsize=18)
handles = [Line2D([0], [0], color='gray', linestyle=style, linewidth=1.5, label=label)
           for style, label in order_styles.values()]
ax.legend(handles=handles, frameon=False, fontsize=14, loc='upper right')

# ---------- Panel B: yes / no questions ----------
ax = axes[1]
positions = np.arange(len(questions))
yes = np.array([answer.sum() for answer in questions.values()])
no = len(df) - yes

# Real in green, sham in blue (light: yes, dark: no); questions about both sessions in white/gray
yes_colors = ['#e3f6e3', '#dbe5ff', '#e3f6e3', '#dbe5ff', 'white', 'white']
no_colors = ['#8fd18f', '#8fa9e6', '#8fd18f', '#8fa9e6', '#bdbdbd', '#bdbdbd']
ax.bar(positions, yes, width=0.6, color=yes_colors, edgecolor='black', linewidth=1.2)
ax.bar(positions, no, width=0.6, bottom=yes, color=no_colors, edgecolor='black', linewidth=1.2)
for position, n_yes, n_no in zip(positions, yes, no):
    if n_yes > 0:
        ax.text(position, n_yes/2, str(n_yes), ha='center', va='center', fontsize=16)
    if n_no > 0:
        ax.text(position, n_yes + n_no/2, str(n_no), ha='center', va='center', fontsize=16)

ax.set_xticks(positions)
ax.set_xticklabels(list(questions), fontsize=13)
ax.set_ylim([0, len(df)])
ax.set_yticks([0, 6, 12, 18, 24])
ax.set_ylabel('Number of participants', fontsize=20)
ax.tick_params(axis='y', labelsize=18)
ax.legend(handles=[Patch(facecolor='#8fd18f', edgecolor='black', label='rAG stim.: no'),
                   Patch(facecolor='#e3f6e3', edgecolor='black', label='rAG stim.: yes'),
                   Patch(facecolor='#8fa9e6', edgecolor='black', label='Sham stim.: no'),
                   Patch(facecolor='#dbe5ff', edgecolor='black', label='Sham stim.: yes'),
                   Patch(facecolor='#bdbdbd', edgecolor='black', label='No'),
                   Patch(facecolor='white', edgecolor='black', label='Yes')],
          frameon=False, fontsize=14, loc='upper left', bbox_to_anchor=(1, 1))

fig.tight_layout(rect=[0, 0, 1, 0.94])

# Panel letters, aligned with the left of the y-axis labels
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for ax, letter in zip(axes, 'AB'):
    label_box = ax.yaxis.get_label().get_window_extent(renderer)
    x = fig.transFigure.inverted().transform((label_box.x0, 0))[0]
    fig.text(x, ax.get_position().y1 + 0.02, letter, fontsize=22, fontweight='bold', ha='left', va='bottom')

fig.savefig(os.path.join(figures_folder, 'Fig8_blinding.png'), dpi=300, bbox_inches='tight')
plt.show()

# ==========================================
# Stop saving what is printed
# ==========================================

sys.stdout.file.close()
sys.stdout = sys.stdout.console
