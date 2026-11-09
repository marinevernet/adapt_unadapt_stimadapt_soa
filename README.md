# Adaptation of the sense of agency to action–outcome delays, and HD-tDCS of the right angular gyrus

Experiment scripts, anonymised data and analysis scripts for two experiments on the sense of agency (SoA).
Participants clicked on the nose of a moose, which then bellowed after a variable delay, and rated how much
they felt that their click had controlled the bellow (0–100%).

- **Experiment 1** (N = 20): each participant did two sessions, an **Adapt** session (adaptation to a 250-ms
  action–outcome delay, as in Haering & Kiesel, 2015) and an **Unadapt** session (test blocks only, all delays
  equally frequent). Question: does adaptation change the sensitivity of the SoA to delay?
- **Experiment 2** (N = 24): each participant did the Adapt session twice, during cathodal high-definition
  transcranial direct current stimulation (HD-tDCS) of the right angular gyrus (**rAG**) or during **sham**
  stimulation (double-blind, counterbalanced). Question: does rAG stimulation reduce the adaptation?

The main measure is **R**, the Pearson correlation between delay (50 to 250 ms) and agency rating, computed for
each participant and session. The **mean SoA** is the mean of the mean ratings at each delay (50 to 250 ms).

## Authors

The scripts were created by **Andréa AUVRAY**, **Romaric THIBOUD** and **Marine VERNET**.
They were reviewed and edited with the help of **Claude Code** (Anthropic).

## Contents

```
DATA/
  adapt_unadapt/
    adapt250/        Experiment 1: participants P01 to P20 (one Adapt and one Unadapt session each)
    immediate/       Additional pilot (participants I01 to I10, adaptation to a 0-ms delay): incomplete, not reported
  stim_adapt/
    s033 ... s056/   Experiment 2: one folder per participant
      session1/, session2/   Task data (file names start with the blinding code of the participant, e.g. F3, M10)
      questionnaires/        BIS, AMI, AABS (Adaptive Agency Beliefs Scale, created for this study) and Edinburgh Handedness Inventory
    blinding_participants.csv   Sensations before / after each session, and guess of the stimulation (blinding check)
psychopy/
  adapt_unadapt/     Experiment 1 task (PsychoPy 2020.2.10): moose_adapt, moose_unadapt (and moose_immediate, pilot)
  stim_adapt/        Experiment 2 task, with the control of the stimulator (starstim_controller.py)
    blind/double_blind.csv   Stimulation protocol of each participant and session: A = rAG stimulation, B = sham
  questionnaire/     Questionnaires
analysis/            Analysis scripts (see below)
results/             Statistics (text files) and summary tables (csv) written by the analysis scripts
figures/             Figures written by the analysis scripts
```

**Task data files.** For each session, PsychoPy saves a `.csv` file and a `.log` file; the task script also saves
`_raw.csv` (all the columns) and `_clean.csv` (the columns used in the analyses). The analysis scripts read the
`_clean.csv` files. Only the test-block trials with a correct click (`block_type == "test"`, `correct == 1`) are
analysed. In Experiment 2, the mouse trajectory of each trial is saved in the columns `mouse.x`, `mouse.y` (cm)
and `mouse.time` (s).

**Anonymisation.** Participants are identified only by a code (P01–P20, I01–I10, s033–s056). Names and the table
linking these codes to the original identifiers are not shared.

## Analysis scripts

| Script | What it does | Main outputs |
|---|---|---|
| `analyze_adapt_unadapt_20261105.py` | Experiment 1: R and mean SoA per participant and session, Adapt vs Unadapt, session order, stability of the individual differences (ICC, split-half reliability) | `results/adapt_unadapt/`, Fig. 2 and Fig. 3 in `figures/adapt_unadapt/` |
| `analyze_stim_adapt_20261105.py` | Experiment 2: R and mean SoA, rAG vs sham, session order, first session only, Bayes factor (prior from Experiment 1), stability of the individual differences | `results/stim_adapt/`, Fig. 5 and Fig. 6 in `figures/stim_adapt/` |
| `analyze_blinding_20261106.py` | Experiment 2: blinding check (sensations, guess of the stimulation) | `results/blinding/`, Fig. 8 in `figures/blinding/` |
| `analyse_questionnaire_20261105.py` | Experiment 2: questionnaire scores and their correlations with R and the mean SoA (sham session) | `results/questionnaire/`, Fig. 9 in `figures/questionnaire/` |
| `analyze_movement_stim_adapt_20261107.py` | Experiment 2: cleaning of the mouse trajectories, movement parameters, rAG vs sham comparison of the movements, and (exploratory) links between the movements and the ratings | `results/movement/`, `figures/movement/` |

**Order.** Run `analyze_adapt_unadapt_20261105.py` before `analyze_stim_adapt_20261105.py` (the Bayes factor
uses the results of Experiment 1), and `analyze_stim_adapt_20261105.py` before `analyse_questionnaire_20261105.py`
(the correlations use the results of Experiment 2). The other scripts are independent.

`analyze_stim_adapt_20261105.py` analyses R by default; set `comp_value = 'soa_mean'` at the top of the script to
analyse the mean SoA (or `'slope'` for the slope of the ratings over delays).

The paths are relative to this folder, so the scripts can be run from anywhere, once the folder is downloaded.

## Software

- Tasks: PsychoPy 2020.2.10 (environment in `psychopy/*/py36.yml`).
- Analyses: Python 3.12, with numpy 1.26.4, pandas 2.1.1, scipy 1.16.3, matplotlib 3.8.4, seaborn 0.13.2,
  pingouin 0.5.5 and statsmodels 0.15.0.

## Reference

Haering, C., & Kiesel, A. (2015). Was it me when it happened too early? Experience of delayed effects shapes
sense of agency. *Cognition*, 136, 38–42.

## How to cite

If you use these data or scripts, please cite the associated article:

> Auvray, A., Thiboud, R., & Vernet, M. (in preparation). *[Title of the article]*. *[Journal]*. https://doi.org/[DOI]

## License

- Code (`analysis/`, `psychopy/`): MIT License (see `LICENSE`).
- Data, results and figures (`DATA/`, `results/`, `figures/`): Creative Commons Attribution 4.0 International
  (CC BY 4.0, see `LICENSE-DATA`). You may reuse them for any purpose, provided that you cite the associated
  article (see "How to cite").
