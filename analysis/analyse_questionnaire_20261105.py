import os
import sys
import glob
import numpy as np
import pandas as pd
import pingouin as pg
import seaborn as sns
import matplotlib.pyplot as plt
# import statsmodels.api as sm # For the regressions
# import statsmodels.formula.api as smf # For the regressions


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


#========================================
#Paths
#========================================

# adapt_unadapt_stimadapt_soa is the parent of the analysis folder containing this script
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_path = os.path.join(project_folder, 'DATA', 'stim_adapt')
result_file = os.path.join(project_folder, 'results', 'stim_adapt', 'results_without-0-ms.csv')
results_folder = os.path.join(project_folder, 'results', 'questionnaire')
figures_folder = os.path.join(project_folder, 'figures', 'questionnaire')

os.makedirs(results_folder, exist_ok=True)
os.makedirs(figures_folder, exist_ok=True)

# Everything printed from now on is also saved in a text file
sys.stdout = Tee(os.path.join(results_folder, 'statistics_output_without-0-ms.txt'))

# #========================================
# Questionnaire dimensions
# #========================================

BIS_DIMENSIONS_first_order = {
    "BIS_Attention": [5, 9, 11, 20, 28],
    "BIS_Cognitive_instability": [6, 24, 26],
    "BIS_Motor": [2, 3, 4, 17, 19, 22, 25],
    "BIS_perseverance": [16, 21, 23, 30],
    "BIS_Self_Control": [1, 7, 8, 12, 13, 14],
    "BIS_Cognitive_Complexity": [10, 15, 18, 27, 29],
}


BIS_DIMENSIONS_second_order = {
    "BIS_attentional_second_order": [5, 9, 11, 20, 28, 6, 24, 26],
    "BIS_motor_second_order": [2, 3, 4, 17, 19, 22, 25, 16, 21, 23, 30],
    "BIS_non_planning_second_order": [1, 7, 8, 12, 13, 14, 10, 15, 18, 27, 29],
}


BIS_DIMENSIONS = {**BIS_DIMENSIONS_first_order, **BIS_DIMENSIONS_second_order}


AABS_DIMENSIONS = {
    "AABS_self_to_world": [23, 28, 5, 46],
    "AABS_personality": [6, 16, 24, 42],
    "AABS_intelligence": [26, 33, 9, 38],
    "AABS_world_to_self": [39, 43, 11, 29],
    "AABS_ambition": [21, 37, 25, 44],
    "AABS_achievement": [18, 35, 13, 31],
    "AABS_control": [41, 47, 4, 17],
    "AABS_self_control": [30, 45, 7, 15],
    "AABS_social_potency": [20, 32, 2, 36],
    "AABS_alienation": [3, 14, 19, 22],
    "AABS_self_esteem": [8, 12, 27, 40],
    "AABS_wellbeing": [1, 10, 34, 48],
}

AABS_DIMENSIONS_second_order = {
    "AABS_dweck": (AABS_DIMENSIONS["AABS_self_to_world"] + AABS_DIMENSIONS["AABS_personality"]
                  + AABS_DIMENSIONS["AABS_intelligence"] + AABS_DIMENSIONS["AABS_world_to_self"]),
    "AABS_ambition_achievement": AABS_DIMENSIONS["AABS_ambition"] + AABS_DIMENSIONS["AABS_achievement"],
    "AABS_control_self_control": AABS_DIMENSIONS["AABS_control"] + AABS_DIMENSIONS["AABS_self_control"],
}

AMI_DIMENSIONS = {
    "AMI_Behavioural": [5, 9, 10, 11, 12, 15],
    "AMI_Social": [2, 3, 4, 8, 14, 17],
    "AMI_Emotional": [1, 6, 7, 13, 16, 18],
}

# ======================================
#  QUESTIONNAIRE SCORING RULES
# ======================================

QUESTIONNAIRE_SCORING = {
    "bis": {
        "answer_code": "BIS_score",
        "reverse_items": [1, 7, 8, 9, 10, 12, 13, 15, 20, 29, 30],
        "reverse_bsl": 5,
        "total": "BIS_total",
    },

    "aabs": {
        "answer_code": "AABS_score",
        "reverse_items": [
            24, 42, 9, 38, 5, 46, 11, 29,
            25, 44, 13, 31, 4, 17, 7, 15,
            2, 36, 19, 22, 27, 40, 34, 48,
        ],
        "reverse_bsl": 7,
        "total": "AABS_total",
    },

    "ami": {
        "answer_code": "AMI_score",
        "reverse_items": list(range(1, 19)),
        "reverse_bsl": 5, # Items from 0 to 4 (the answers are coded from 1 to 5), higher score = more apathy
        "total": "AMI_total",
    },

    "ehi": {
        "answer_code": "EHI_score",
        "reverse_items": None,
        "reverse_bsl": None,
        "total": "EHI_total",
    },
}

#========================================
# Load questionnaire Data
#========================================

def load_questions_ratings(path, questionnaire):
    
    all_data = []

    # Loop through all participant folders
    for participant in os.listdir(path):

        participant_path = os.path.join(path, participant)

        # Only continue if it is a folder
        if os.path.isdir(participant_path):

            # Path to questionnaires folder
            questionnaires_path = os.path.join(participant_path, "questionnaires")

            if os.path.exists(questionnaires_path):

                # Search for csv files containing BIS in the filename
                if questionnaire == 'bis':
                    file_to_load = "*BIS*.csv"
                elif questionnaire == 'aabs':
                    file_to_load = "*AABS*.csv"
                elif questionnaire == 'ami':
                    file_to_load = "*AMI*.csv"
                elif questionnaire == 'ehi':
                    file_to_load ='*EHI*.csv'

                files = glob.glob(os.path.join(questionnaires_path, file_to_load))

                # If at least one BIS file exists
                if len(files) > 0:

                    print(f"Loading {questionnaire} files for {participant}")

                    # Take the first matching file
                    file = files[0]

                    # Load csv
                    df = pd.read_csv(file)

                    # Add participant ID column
                    df["participant"] = participant

                    # Append to list
                    all_data.append(df)

                else:
                    print(f"WARNING: no {questionnaire} file found for {participant}")

    # Concatenate all participants together
    df_all = pd.concat(all_data, ignore_index=True)

    return df_all

df_BIS_all = load_questions_ratings(base_path, 'bis')
df_AABS_all = load_questions_ratings(base_path, 'aabs')
df_AMI_all = load_questions_ratings(base_path, 'ami')
df_EHI_all = load_questions_ratings(base_path, 'ehi')


#========================================
# Clean and compute reverse score
#========================================

def clean_and_compute_score(df_all, questionnaire):

    # Get the scoring rules already defined above
    scoring = QUESTIONNAIRE_SCORING[questionnaire]

    answer_code = scoring["answer_code"]
    reverse_items = scoring["reverse_items"]
    reverse_bsl = scoring["reverse_bsl"]
    total = scoring["total"]

    # Keep only the required columns
    df_all = df_all[["participant", "Question_Num", "Answer_Code"]].copy()

    # Rename Answer_Code according to the questionnaire
    df_all = df_all.rename(
        columns={"Answer_Code": answer_code}
    )

    # Item number within each participant
    df_all["item_number"] = df_all["Question_Num"]

    # Copy original scores before reversing
    df_all["reversed_score"] = df_all[answer_code]

    # Reverse scores only when required
    if reverse_items is not None:

        mask = df_all["item_number"].isin(reverse_items)

        df_all.loc[mask, "reversed_score"] = (
            reverse_bsl
            - df_all.loc[mask, answer_code]
        )

    # Compute questionnaire total
    df_scores = (
        df_all
        .groupby("participant", as_index=False)["reversed_score"]
        .sum()
        .rename(columns={"reversed_score": total})
    )

    return df_all, df_scores

df_BIS_all, df_BIS_scores = clean_and_compute_score(df_BIS_all, 'bis')
df_AABS_all, df_AABS_scores = clean_and_compute_score(df_AABS_all, 'aabs')
df_AMI_all, df_AMI_scores = clean_and_compute_score(df_AMI_all, 'ami')
df_EHI_all, df_EHI_scores = clean_and_compute_score(df_EHI_all, 'ehi')


#========================================
# Merge into one df
#========================================

df_questionnaire_scores = (
    df_BIS_scores
    .merge(df_AMI_scores, on="participant", how="outer")
    .merge(df_AABS_scores, on="participant", how="outer")
    .merge(df_EHI_scores, on="participant", how="outer")
)

#========================================
#Create df for each questionnaire with dimensions 
#========================================

def compute_dimensions(df_all, questionnaire):

    if questionnaire == "bis":
        dimensions = BIS_DIMENSIONS

    
    elif questionnaire == "aabs" : 
        dimensions = {**AABS_DIMENSIONS, **AABS_DIMENSIONS_second_order}
    elif questionnaire == "ami": 
        dimensions = AMI_DIMENSIONS


    elif questionnaire == "ehi":
        return None
    
    all_dimensions = []

    for dimension_name, items in dimensions.items():

        temp = (
        df_all[df_all["item_number"].isin(items)]
        .groupby("participant", as_index=False)["reversed_score"]
        .sum()
        .rename(columns={"reversed_score": dimension_name})
    )

        all_dimensions.append(temp)

    df_dimensions = all_dimensions[0]

    for temp in all_dimensions[1:]:
        df_dimensions = df_dimensions.merge(
        temp,
        on="participant",
        how="outer"
    )

    return df_dimensions


df_BIS_dimensions = compute_dimensions(df_BIS_all, 'bis')
df_AABS_dimensions = compute_dimensions(df_AABS_all, 'aabs')
df_AMI_dimensions = compute_dimensions(df_AMI_all, 'ami')
df_EHI_dimensions = compute_dimensions(df_EHI_all, 'ehi')

#========================================
#  Merge all questionnaire dimensions 
#========================================

df_questionnaire_final = (
    df_questionnaire_scores
    .merge(df_BIS_dimensions, on="participant", how="left")
    .merge(df_AABS_dimensions, on="participant", how="left")
    .merge(df_AMI_dimensions, on="participant", how="left")
)
# The participants are identified by the code of their folder (s033, s034...), as in the task results

#========================================
# Merge task results with questionnaire scores
#========================================

df_csv_dimensions = (
    pd.read_csv(result_file, index_col=0)
    .merge(df_questionnaire_final, on="participant", how="left")
)

# ========================================
# FUNCTIONS FOR THE ANALYSES
# ========================================

def holm_correction(pvalues):
    # No correction needed if there is only one test
    if len(pvalues) == 1:
        return list(pvalues)
    return list(pg.multicomp(list(pvalues), method='holm')[1])


def run_correlations(outcome, family, predictors):
    """
    Spearman correlations, Holm-corrected within the family of predictors.
    Predictors with an uncorrected p < 0.05 are plotted.
    """
    print(f"\n----- {outcome}: {family} -----")

    correlations = [pg.corr(df_csv_dimensions[predictor], df_csv_dimensions[outcome], method='spearman')
                    for predictor in predictors]
    corrected = holm_correction([correlation['p-val'].iloc[0] for correlation in correlations])

    for predictor, correlation, p_corrected in zip(predictors, correlations, corrected):
        rho = correlation['r'].iloc[0]
        p = correlation['p-val'].iloc[0]
        ci = correlation['CI95%'].iloc[0]
        print('%s: rho=%.2f; 95%% CI [%.2f, %.2f]; p=%.3g; Holm p=%.3g' %(predictor, rho, ci[0], ci[1], p, p_corrected))

        if p < 0.05:
            plt.figure()
            sns.regplot(data=df_csv_dimensions, x=predictor, y=outcome)
            plt.title('%s vs %s (rho=%.2f, p=%.3g)' %(predictor, outcome, rho, p))
            plt.savefig(os.path.join(figures_folder, f"correlation_{outcome}_{predictor}.png"), dpi=300)
            plt.show()


def plot_figure_correlations(panels, file_name):
    """
    One panel per correlation. The line is a linear fit, shown as a visual guide
    (the statistics, reported in the figure legend, are from the Spearman correlation).
    """
    marker_color = '#3a6ea5'
    line_color = '#1f3f66'
    ink = '#2b2b2b'
    rng = np.random.default_rng(1) # So that the jitter is the same at each run

    fig, axes = plt.subplots(2, 2, figsize=[10, 9.2])

    for ax, panel, letter in zip(axes.flat, panels, 'ABCD'):
        ax.set_title(letter, loc='left', fontsize=14, fontweight='bold', color=ink)
        x = df_csv_dimensions[panel['x']]
        y = df_csv_dimensions[panel['y']]

        # Discrete scores: a small horizontal jitter so that the points do not overlap
        x_jittered = x + rng.uniform(-panel['jitter'], panel['jitter'], len(x))
        ax.scatter(x_jittered, y, s=70, color=marker_color, edgecolors='white', linewidths=1, zorder=3)

        line = np.polyfit(x, y, 1)
        line_x = np.array([x.min(), x.max()])
        ax.plot(line_x, np.polyval(line, line_x), color=line_color, linewidth=2, zorder=2)

        ax.set_ylabel(panel['ylabel'], fontsize=13, color=ink)
        ax.set_xlabel(panel['xlabel'], fontsize=13, color=ink, labelpad=30)
        ax.annotate('← ' + panel['left'], xy=(0, -0.13), xycoords='axes fraction', ha='left', va='top', fontsize=11, color=ink)
        ax.annotate(panel['right'] + ' →', xy=(1, -0.13), xycoords='axes fraction', ha='right', va='top', fontsize=11, color=ink)

        ax.tick_params(colors=ink, labelsize=11)
        ax.grid(axis='y', color='#e6e6e6', linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    fig.tight_layout()
    fig.savefig(os.path.join(figures_folder, file_name), dpi=300)
    plt.show()


# def plot_significant_predictors(model, df, outcome, predictors):
#     """
#     Partial regression plots: the slope and the p value are those of the multiple regression.
#     With a single predictor, there is nothing to adjust for, so this is a simple regression plot.
#     """
#     sig = model.pvalues[model.pvalues < 0.05].index
#     sig = [v for v in sig if v != "Intercept"]
#
#     for predictor in sig:
#         if len(predictors) == 1:
#             plt.figure()
#             sns.regplot(data=df, x=predictor, y=outcome)
#         else:
#             others = [v for v in predictors if v != predictor]
#             sm.graphics.plot_partregress(outcome, predictor, others, data=df, obs_labels=False)
#
#         plt.title('%s vs %s, adjusted (p=%.3g)' %(predictor, outcome, model.pvalues[predictor]))
#         plt.savefig(os.path.join(figures_folder, f"regression_{outcome}_{predictor}.png"), dpi=300)
#         plt.show()
#
#
# def run_ols(outcome, family, predictors):
#     formula = f"{outcome} ~ {' + '.join(predictors)}"
#
#     model = smf.ols(formula, data=df_csv_dimensions).fit()
#
#     print(f"\n===== {outcome}: {family} =====")
#     print(formula)
#     print(model.summary())
#     print('Holm-corrected p values of the predictors:')
#     for predictor, p_corrected in zip(predictors, holm_correction(model.pvalues[predictors])):
#         print('%s: Holm p=%.3g' %(predictor, p_corrected))
#
#     # Plot predictors with p < 0.05
#     plot_significant_predictors(
#         model,
#         df_csv_dimensions,
#         outcome,
#         predictors
#     )
#
#     return model

# ========================================
# PREDICTORS
# ========================================

FAMILIES = {
    "Global scores": ["BIS_total", "AABS_total", "AMI_total"],
    "Detailed dimensions": ["AMI_Behavioural", "BIS_perseverance", "BIS_Self_Control", "AABS_dweck", "AABS_ambition_achievement"],
}

# For the regressions
# MODELS = {
#     "Global": FAMILIES["Global scores"],
#     "Detailed": FAMILIES["Detailed dimensions"],
# }

# ========================================
# ANALYSES
# ========================================

print('\n*************** Correlations (Spearman, Holm correction within each family and outcome) ***************')
for outcome in ["R_sham", "soa_mean_sham"]:
    for family, predictors in FAMILIES.items():
        run_correlations(outcome, family, predictors)

# Figure for the article
plot_figure_correlations(
    [
        {'x': 'AABS_dweck', 'y': 'R_sham', 'jitter': 0,
         'xlabel': 'Entity/incremental beliefs', 'ylabel': 'R value',
         'left': 'Entity beliefs', 'right': 'Incremental beliefs'},
        {'x': 'BIS_total', 'y': 'soa_mean_sham', 'jitter': 0,
         'xlabel': 'BIS total', 'ylabel': 'Mean SoA',
         'left': 'Less impulsivity', 'right': 'More impulsivity'},
        {'x': 'BIS_perseverance', 'y': 'soa_mean_sham', 'jitter': 0.12,
         'xlabel': 'BIS perseverance', 'ylabel': 'Mean SoA',
         'left': 'More perseverance', 'right': 'Less perseverance'},
        {'x': 'BIS_Self_Control', 'y': 'soa_mean_sham', 'jitter': 0.12,
         'xlabel': 'BIS self-control', 'ylabel': 'Mean SoA',
         'left': 'More self-control', 'right': 'Less self-control'},
    ],
    'Fig9_correlations_without-0-ms.png'
)

# print('\n*************** Regressions (Holm correction within each model) ***************')
# for outcome in ["R_sham", "soa_mean_sham"]:
#     for model_name, predictors in MODELS.items():
#         run_ols(outcome, model_name, predictors)

# ========================================
# STOP SAVING WHAT IS PRINTED
# ========================================

sys.stdout.file.close()
sys.stdout = sys.stdout.console
