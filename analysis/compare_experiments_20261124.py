import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

# ==========================================
# Comparison between the two experiments (different participants): R in each session of Experiment 2
# (rAG, sham) vs R in each session of Experiment 1 (Adapt, Baseline), with Bayes factors (Dienes, 2014)
# ==========================================

# ==========================================
# Paths
# ==========================================

# adapt_unadapt_stimadapt_soa is the parent of the analysis folder containing this script
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results_folder = os.path.join(project_folder, 'results', 'comparison_between_experiments')
os.makedirs(results_folder, exist_ok=True)

# Results of the two experiments (run analyze_adapt_unadapt and analyze_stim_adapt first)
file_exp1 = os.path.join(project_folder, 'results', 'adapt_unadapt', 'results_without-0-ms.csv')
file_exp2 = os.path.join(project_folder, 'results', 'stim_adapt', 'results_without-0-ms.csv')


# ==========================================
# Functions
# ==========================================

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


# The three following functions are the same as in analyze_stim_adapt_20261105.py

def normaly(mn, variance, x):

    return np.exp(-(x - mn)*(x - mn)/(2*variance))/np.sqrt(2*np.pi*variance)


def BayesianFactorsNormal(obtained, sd, meanoftheory, sdtheory, tail):
    """
    Bayes factor (theory vs null), with p(population value|theory) normal (tail=2) or half-normal (tail=1).
    obtained keeps its sign: it is negative if the effect goes against the direction predicted by a half-normal.
    """
    sd2 = sd*sd
    omega = sdtheory*sdtheory
    incr = sdtheory/200
    theta = meanoftheory - 5*sdtheory + incr*np.arange(1, 2002)

    if tail == 2:
        dist_theta = normaly(meanoftheory, omega, theta)
    else:
        dist_theta = 2*normaly(meanoftheory, omega, theta)*(theta > 0)

    area = np.sum(dist_theta * normaly(theta, sd2, obtained))*incr # integrating p(theta|theory)*p(data|theta) over theta

    return area/normaly(0, sd2, obtained)


def robustness_region(obtained, sd, meanoftheory, sdtheory, tail, max_sd):
    """
    Range of SDs around sdtheory for which the conclusion stays the same (BF<1/3, 1/3<=BF<=3 or BF>3).
    The search goes in steps of sdtheory/100, up to max_sd.
    Returns the lower and upper limits, the conclusion, and whether the upper limit is max_sd (i.e., no upper limit was found).
    """
    def conclusion(sd_to_test):
        BF = BayesianFactorsNormal(obtained, sd, meanoftheory, sd_to_test, tail)
        return 'B<1/3' if BF < 1/3 else ('B>3' if BF > 3 else '1/3<B<3')

    step = sdtheory/100
    lower = sdtheory
    upper = sdtheory
    while lower - step > 0 and conclusion(lower - step) == conclusion(sdtheory):
        lower = lower - step
    while upper + step <= max_sd and conclusion(upper + step) == conclusion(sdtheory):
        upper = upper + step
    no_upper_limit = upper + step > max_sd

    return lower, upper, conclusion(sdtheory), no_upper_limit


def pooled_sd(var1, var2):

    return np.sqrt(((len(var1)-1)*var1.var(ddof=1) + (len(var2)-1)*var2.var(ddof=1)) / (len(var1)+len(var2)-2))


def compare_between_experiments(var_exp2, var_exp1, label, tail, sign, sdtheory_d, sdtheory_R):
    """
    Unpaired comparison of R between a session of Experiment 2 and a session of Experiment 1.
    sign: +1 if the hypothesis predicts Experiment 2 > Experiment 1, -1 if it predicts Experiment 2 < Experiment 1
    (for a half-normal; ignored for a normal).
    Bayes factor on the scale of Cohen's d (between participants), and on the scale of R as a check.
    """
    print('\n*************** ' + label + ' ***************')
    print('Experiment 2 (n=%d): %.2f +/- %.2f; Experiment 1 (n=%d): %.2f +/- %.2f' %(
        len(var_exp2), var_exp2.mean(), var_exp2.std(), len(var_exp1), var_exp1.mean(), var_exp1.std()))

    a = ttest_ind(var_exp2, var_exp1, equal_var=False)
    print('(Welch t-test, two-sided): t(%.1f)=%.2f; p=%.3g' %(a.df, a.statistic, a.pvalue))

    difference = var_exp2.mean() - var_exp1.mean()
    for scale, obtained, sd, sdtheory, max_sd in [
            ("Cohen's d", difference/pooled_sd(var_exp2, var_exp1), np.sqrt(1/len(var_exp2) + 1/len(var_exp1)), sdtheory_d, 5),
            ('R', difference, np.sqrt(var_exp2.var(ddof=1)/len(var_exp2) + var_exp1.var(ddof=1)/len(var_exp1)), sdtheory_R, 2)]:
        obtained_for_theory = sign*obtained if tail == 1 else obtained
        Bayesfactor = BayesianFactorsNormal(obtained_for_theory, sd, 0, sdtheory, tail)
        lower, upper, conclusion, no_upper_limit = robustness_region(obtained_for_theory, sd, 0, sdtheory, tail, max_sd)
        upper_text = '>%g' %(max_sd) if no_upper_limit else '%.3f' %(upper)
        print('BF (%s scale): difference=%.3f; standard error=%.3f; %s, SD=%.3f: BF=%.2f; RR[%s] = [%.3f, %s]' %(
            scale, obtained, sd, 'half-normal' if tail == 1 else 'normal', sdtheory, Bayesfactor, conclusion, lower, upper_text))


# ==========================================
# Main Script
# ==========================================

# Everything printed from now on is also saved in a text file
sys.stdout = Tee(os.path.join(results_folder, 'statistics_output_between_experiments_without-0-ms.txt'))

df_exp1 = pd.read_csv(file_exp1)
df_exp1 = df_exp1[df_exp1['experiment']=='adapt250'] # Without the pilot (adaptation to 0 ms)
df_exp2 = pd.read_csv(file_exp2)

# ************* Expected effect: the adaptation of Experiment 1 (Adapt - Baseline) *************

# The comparisons are between participants, so the effect of adaptation is standardized by the pooled SD of the two sessions
# (and not by the SD of the differences, as for the preregistered dz = 0.74, which applies to paired comparisons)
sdtheory_R = (df_exp1['R_adapt'] - df_exp1['R_baseline']).mean()
sdtheory_d = sdtheory_R/pooled_sd(df_exp1['R_adapt'], df_exp1['R_baseline'])

print('Expected effect (adaptation in Experiment 1, Adapt - Baseline): %.3f in R; d=%.3f (standardized by the pooled SD)' %(sdtheory_R, sdtheory_d))
print('BF<1/3: evidence for no difference; BF>3: evidence for the hypothesis; otherwise: inconclusive')

# ************* Comparisons, with all the participants of Experiment 2, then without the outliers *************

samples = [
    ('EXPERIMENT 2, ALL PARTICIPANTS: N=%d' %(len(df_exp2)), df_exp2),
    ('EXPERIMENT 2, WITHOUT THE OUTLIERS: N=%d' %((~df_exp2['outlier']).sum()), df_exp2[~df_exp2['outlier']]),
]

for sample_title, df_sample in samples:

    print('\n\n################################ ' + sample_title + ' ################################')

    # Does the sham session replicate the adaptation of Experiment 1? No direction predicted
    compare_between_experiments(df_sample['R_sham'], df_exp1['R_adapt'], 'Sham (Exp. 2) vs Adapt (Exp. 1); H1: different, normal',
                                2, 1, sdtheory_d, sdtheory_R)

    # Does the rAG stimulation reduce the adaptation, compared with the Adapt session of Experiment 1?
    compare_between_experiments(df_sample['R_real'], df_exp1['R_adapt'], 'rAG (Exp. 2) vs Adapt (Exp. 1); H1: rAG < Adapt, half-normal',
                                1, -1, sdtheory_d, sdtheory_R)

    # Is there still some adaptation under rAG stimulation, compared with the Baseline session of Experiment 1?
    compare_between_experiments(df_sample['R_real'], df_exp1['R_baseline'], 'rAG (Exp. 2) vs Baseline (Exp. 1); H1: rAG > Baseline, half-normal',
                                1, 1, sdtheory_d, sdtheory_R)

    # For comparison: the sham session vs the Baseline session of Experiment 1
    compare_between_experiments(df_sample['R_sham'], df_exp1['R_baseline'], 'Sham (Exp. 2) vs Baseline (Exp. 1); H1: sham > Baseline, half-normal',
                                1, 1, sdtheory_d, sdtheory_R)

# ************* Stop saving what is printed *************

sys.stdout.file.close()
sys.stdout = sys.stdout.console
