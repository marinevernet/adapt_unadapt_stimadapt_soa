import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, ttest_rel, ttest_ind, shapiro, ttest_1samp, norm, spearmanr
import glob, os, sys
from datetime import datetime
import pingouin as pg
import math

# ==========================================
# General settings
# ==========================================

plotting_the_sanity_check = False
plotting_the_correlation = False
plotting_the_article_figures = True
add_participants_initial = False
R_or_slope = 'R' # 'slope'
delays_to_eliminate = [-1, 0, 1.25]
# delays_to_eliminate = [-1, 1.25]
corrchoice = 'pearson'

# ==========================================
# Functions
# ==========================================

def extract_info(filename):

    parts = filename.split("_")
    participant = parts[0]
    session = parts[2]
    year = parts[3]
    month = parts[4]
    day = parts[5]

    # Combine into a proper date string
    date_str = f"{year} {month} {day}"

    # Convert to datetime object
    date = datetime.strptime(date_str, "%Y %b %d")

    return participant, session, date


def sanity_check(df, participant, session):
    """
    Plotting the figure to check that all values are in the correct range
    """

    columns_float = ['fixation_time', 'scheduled_sound_delay',
       'scheduled_jitter', 'clickTime', 'click_x', 'click_y',
       'soundON', 'scheduled_moose_time', 'moose_time', 'rating',
       'rating_time']
    
    df[columns_float] = df[columns_float].astype(float)

    df["delta_sound"] = df["scheduled_sound_delay"] - (df["soundON"]-df["clickTime"])
    df["delta_moose_time"] = df["moose_time"] - df["scheduled_moose_time"]

    fig, axes = plt.subplots(5, 3, figsize=[14, 7])

    df["fixation_time"].plot(kind="hist", ax=axes[0, 0], title="fixation_time (s)")
    df["scheduled_jitter"].plot(kind="hist", ax=axes[0, 1], title="scheduled_jitter (s)")

    df["rating_time"].plot(kind="hist", ax=axes[1, 0], title="rating_time (s)")
    df["rating"].plot(kind="hist", ax=axes[1, 1], title="rating (%)")

    df["clickTime"].plot(kind="hist", ax=axes[2, 0], title="clickTime (s)")
    df["click_x"].plot(kind="hist", ax=axes[2, 1], title="click_x (cm)")
    df["click_y"].plot(kind="hist", ax=axes[2, 2], title="click_y (cm)")

    df["scheduled_moose_time"].plot(kind="hist", ax=axes[3, 0], title="scheduled_moose_time (s)")
    df["moose_time"].plot(kind="hist", ax=axes[3, 1], title="moose_time (s)")
    df["delta_moose_time"].plot(kind="hist", ax=axes[3, 2], title="delta_moose_time (s)")

    df["scheduled_sound_delay"].plot(kind="hist", ax=axes[4, 0], title="scheduled_sound_delay (s)")
    df["soundON"].plot(kind="hist", ax=axes[4, 1], title="soundON (s)")
    df_filtered = df[df["scheduled_sound_delay"] != -1]
    df_filtered["delta_sound"].plot(kind="hist", ax=axes[4, 2], title="delta_sound (s) \n(not taking anticipated trials into account)")

    fig.delaxes(axes[0, 2])
    fig.delaxes(axes[1, 2])

    fig.suptitle(participant + ' ' + session)
    plt.tight_layout()
    fig.savefig(os.path.join(figures_folder,'sanity_check_'+participant+'_'+session+'.png'), dpi=300)
    plt.show()


def computing_correlation(df_calcul, delays_to_eliminate):

    for delay in delays_to_eliminate:
        df_calcul = df_calcul[df_calcul['scheduled_sound_delay'] != delay]
    
    # Calculate Pearson correlation
    if corrchoice == 'spearman':
        r, p = spearmanr(df_calcul['scheduled_sound_delay'], df_calcul['rating'])
    else:
        r, p = pearsonr(df_calcul['scheduled_sound_delay'], df_calcul['rating'])
    # Calculate the slope
    z1 = np.polyfit(df_calcul['scheduled_sound_delay'], df_calcul['rating'], 1)
    slope = z1[0]
    # Number of trials used for the correlation
    n = len(df_calcul)

    return r, p, slope, n
    
    

def computing_soa_mean(df_calcul, delays_to_eliminate):
    """
    Mean SoA: mean of the means per delay, so that the many 250 ms trials of the adapt session do not dominate
    """
    for delay in delays_to_eliminate:
        df_calcul = df_calcul[df_calcul['scheduled_sound_delay'] != delay]

    return df_calcul.groupby('scheduled_sound_delay')['rating'].mean().mean()


def plotting_correlation(df_participant, R_or_slope, delays_to_eliminate):

    fig, axes = plt.subplots(1, 2, figsize=[14, 7])

    for session in df_participant['session'].unique():
        df_test = df_participant[df_participant['session']==session].copy()
        if session == "unadapt":
            column = 0
        else:
            column = 1

        r, p, slope, _ = computing_correlation(df_test, delays_to_eliminate)

        df_test["scheduled_sound_delay"] = df_test["scheduled_sound_delay"]*1000
        df_test["scheduled_sound_delay"]=df_test["scheduled_sound_delay"].astype(int)
        df_test_corr = df_test[['scheduled_sound_delay', 'rating']].copy()

        # This is for plotting purpose (aliging the violin plot and the correlation)
        value_map = {50: 2, 100: 3, 150: 4, 200: 5, 250: 6}
        if 0 not in delays_to_eliminate: # So that the regression line matches the R
            value_map[0] = 1
        df_test_corr.loc[:, 'scheduled_sound_delay_mapped'] = df_test_corr['scheduled_sound_delay'].map(value_map)
        df_test_corr.loc[:, 'scheduled_sound_delay'] = df_test_corr['scheduled_sound_delay'].astype('category')

        # Plotting
        sns.violinplot(
            x='scheduled_sound_delay',
            y='rating',
            data=df_test_corr,
            inner=None,
            cut=0,
            ax=axes[column],
            density_norm='width',
            color='lightgrey'
        )

        sns.stripplot(
            x='scheduled_sound_delay',
            y='rating',
            data=df_test_corr,
            jitter=True,
            color='black',
            size=8,
            ax=axes[column]
        )

        # regression line color
        if session == 'unadapt':
            line_color = 'green'
        elif session == 'adapt':
            line_color = 'blue'
        elif session == 'immediate':
            line_color = 'red'
        else:
            line_color = 'black'   

        sns.regplot(
            x='scheduled_sound_delay_mapped',
            y='rating',
            data=df_test_corr,
            ci=None,        # no confidence interval
            scatter_kws={'s':50, 'alpha':0},
            line_kws={'color': line_color, 'linewidth': 6},
            ax=axes[column]
        )

        # Annotate R on the figure
        text = f"R = {r:.2f}"
        axes[column].annotate(
            text=text,
            xy=(0.95, 0.3),      # on the right, where there are usually no data points
            xycoords=axes[column].transAxes,
            ha="right", va="center",
            color=line_color,
            fontsize=20,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7)
        )

        # Breaks to show the discontinuity
        x1_values = [0.5, 0.5+0.10, 6.5, 6.5+0.10]
        for x1 in x1_values: 
            l1, = axes[column].plot([x1-0.05, x1], [-0.015, 0.015],
                                    transform=axes[column].get_xaxis_transform(),
                                    color='black', lw=2)
            l1.set_clip_on(False)

        # Labels and show
        axes[column].set_xlabel("Sound Delay (ms)")
        axes[column].set_ylabel("Perceived control (%)")
        axes[column].set_ylim([0, 100])
        axes[column].set_title(session, fontsize=20)
        axes[column].set_xticks(range(8))
        axes[column].set_xticklabels(["before", 0, 50, 100, 150, 200, 250, 1250])

        # axis font size
        axes[column].tick_params(axis='both', labelsize=15)
        axes[column].xaxis.label.set_size(20)
        axes[column].yaxis.label.set_size(20)

    fig.suptitle(participant, fontsize=20)

    fig.savefig(os.path.join(figures_folder,'correlation_'+elim+'_'+participant+'.png'), dpi=300)
    plt.show()


def plot_article_violin(ax, df, columns, labels, palette, ylabel, ylim, yticks, group_styles=None, show_legend=True, legend_above=False):
    """
    Violin plot of paired data, with the participants as points and gray lines, without a title.
    group_styles: {first session: (line style, label)}, to distinguish the participants by the order of the sessions.
    """
    from matplotlib.lines import Line2D

    df_plot = df[columns].melt(var_name='condition', value_name='value')

    sns.violinplot(data=df_plot, x='condition', y='value', hue='condition', legend=False,
                   inner='box', palette=palette, cut=0, ax=ax)

    # Make the colors pale (seaborn does not apply the transparency of the palette)
    for violin, color in zip(ax.collections, palette):
        violin.set_facecolor(color)

    sns.stripplot(data=df_plot, x='condition', y='value', color='black', size=10, jitter=False, ax=ax)

    for _, row in df.iterrows(): # For each participant
        linestyle = '-' if group_styles is None else group_styles[row['first_session']][0]
        ax.plot([0, 1], [row[columns[0]], row[columns[1]]], color='gray', alpha=0.8,
                linewidth=1 if linestyle == '-' else 1.5, linestyle=linestyle)

    if group_styles is not None and show_legend:
        handles = [Line2D([0], [0], color='gray', linestyle=style, linewidth=1.5, label=label)
                   for style, label in group_styles.values()]
        if legend_above: # Above the plot, away from the violins
            ax.legend(handles=handles, frameon=False, fontsize=14, loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=2)
        else:
            ax.legend(handles=handles, frameon=False, fontsize=14, loc='lower right')

    ax.set_ylim(ylim)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks)
    ax.set_ylabel(ylabel, fontsize=20)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_xlabel('')
    ax.tick_params(axis='both', labelsize=20)


def plotting_all_participants(df_all, participants, column, conditions, labels, delays_to_eliminate, n_rows, n_columns, file_name):
    """
    One panel per participant, with half-violins, the trials and the regression line of the two conditions
    (first condition in green on the left, second condition in blue on the right).
    """

    colors = ['green', 'blue']
    pale_colors = ['#cfeccf', '#d6e0ff']
    offsets = [-0.12, 0.12] # So that the trials of the two conditions do not overlap
    delay_positions = {-1: 0, 0: 1, 0.05: 2, 0.1: 3, 0.15: 4, 0.2: 5, 0.25: 6, 1.25: 7}
    rng = np.random.default_rng(1) # So that the jitter is the same at each run

    fig, axes = plt.subplots(n_rows, n_columns, figsize=[2.8*n_columns, 2.6*n_rows], sharex=True, sharey=True)

    for participant, ax in zip(participants, axes.flat):
        df_participant = df_all[df_all['participant']==participant]

        # Half-violins
        sns.violinplot(
            data=df_participant.assign(position=df_participant['scheduled_sound_delay'].map(delay_positions)),
            x='position',
            y='rating',
            hue=column,
            hue_order=conditions,
            order=list(range(8)),
            split=True,
            inner=None,
            cut=0,
            density_norm='width',
            palette=pale_colors,
            saturation=1,
            linewidth=0.5,
            legend=False,
            ax=ax
        )
        ax.set_xlabel('')
        ax.set_ylabel('')

        for condition, label, color, offset in zip(conditions, labels, colors, offsets):
            df_condition = df_participant[df_participant[column]==condition]
            positions = df_condition['scheduled_sound_delay'].map(delay_positions)

            # Trials
            jitter = rng.uniform(-0.08, 0.08, len(df_condition))
            ax.scatter(positions + offset + jitter, df_condition['rating'], s=5, color=color, alpha=0.3, linewidths=0)

            # Regression line (on the trials used for the correlation)
            kept = ~df_condition['scheduled_sound_delay'].isin(delays_to_eliminate)
            line = np.polyfit(positions[kept], df_condition['rating'][kept], 1)
            line_x = np.array([positions[kept].min(), positions[kept].max()])
            ax.plot(line_x, np.polyval(line, line_x), color=color, linewidth=2.5, label=label)

            # R
            r, _, _, _ = computing_correlation(df_condition, delays_to_eliminate)
            ax.text(0.87, 0.36 if color == colors[0] else 0.22, 'R = %.2f' %(r), color=color, fontsize=10,
                    ha='right', va='center', transform=ax.transAxes,
                    bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.7))

        # Breaks to show the discontinuity
        for x1 in [0.5, 0.5+0.10, 6.5, 6.5+0.10]:
            l1, = ax.plot([x1-0.05, x1], [-0.015, 0.015], transform=ax.get_xaxis_transform(), color='black', lw=1)
            l1.set_clip_on(False)

        ax.set_title(participant, fontsize=11)
        ax.set_ylim([-3, 103])
        ax.set_yticks([0, 50, 100])
        ax.set_xticks(range(8))
        ax.set_xticklabels(["before", 0, 50, 100, 150, 200, 250, 1250], rotation=45, fontsize=9)

    handles, legend_labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, legend_labels, loc='upper center', ncol=2, frameon=False, fontsize=13)
    fig.supxlabel('Sound Delay (ms)', fontsize=14)
    fig.supylabel('Perceived control (%)', fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(os.path.join(figures_folder,file_name), dpi=300)
    plt.show()


def variables_for_specific_comparisons(comparison, wide, df_results, R_or_slope):

    if comparison == 'adapt250':
        title='Experiment 1 (Unadapt vs Adapt 250)'
        df = wide[wide['experiment']=='adapt250']
        if R_or_slope == 'R': columns = ['R_unadapt', 'R_adapt']
        else: columns = ['slope_unadapt', 'slope_adapt']
        order = ['unadapt', 'adapt']
        x = None
        y = None
        alternative = 'less'
        pairing = 'paired'
        light_green = (0.2, 0.8, 0.2, 0.12)
        light_blue = (0.3, 0.5, 1.0, 0.20)
        palette = [light_green, light_blue]

    if comparison == 'adapt250 soa_mean':
        title='Experiment 1 (Unadapt vs Adapt 250), mean SoA'
        df = wide[wide['experiment']=='adapt250']
        columns = ['soa_mean_unadapt', 'soa_mean_adapt']
        order = ['unadapt', 'adapt']
        x = None
        y = None
        alternative = 'two-sided'
        pairing = 'paired'
        light_green = (0.2, 0.8, 0.2, 0.12)
        light_blue = (0.3, 0.5, 1.0, 0.20)
        palette = [light_green, light_blue]

    if comparison == 'adapt250 as unpaired':
        title='Experiment 1 (Unadapt vs Adapt 250) as unpaired'
        df = wide[wide['experiment']=='adapt250']
        if R_or_slope == 'R': columns = ['R_unadapt', 'R_adapt']
        else: columns = ['slope_unadapt', 'slope_adapt']
        order = ['unadapt', 'adapt']
        x = None
        y = None
        alternative = 'less'
        pairing = 'as_unpaired'
        light_green = (0.2, 0.8, 0.2, 0.12)
        light_blue = (0.3, 0.5, 1.0, 0.20)
        palette = [light_green, light_blue]

    if comparison == 'adapt0':
        title='Experiment 2 (Unadapt vs Adapt 0)'
        df = wide[wide['experiment']=='adapt0']
        if R_or_slope == 'R': columns = ['R_unadapt', 'R_adapt']
        else: columns = ['slope_unadapt', 'slope_adapt']
        order = ['unadapt', 'adapt']
        x = None
        y = None
        alternative = 'greater'
        pairing = 'paired'
        light_green = (0.2, 0.8, 0.2, 0.12)
        light_red = (1.0, 0.3, 0.3, 0.20)
        palette = [light_green, light_red]

    if comparison == 'session_order':
        title='Session order (Both experiments)'
        df = wide
        if R_or_slope == 'R': columns = ['R_session1', 'R_session2']
        else: columns = ['slope_session1', 'slope_session2']
        order = [1.0, 2.0]
        x = None
        y = None
        alternative = 'two-sided'       
        pairing = 'paired'
        palette = ['lightgrey', 'lightgrey']

    if comparison == 'session_order_exp1':
        title='Session order - Exp1'
        df = wide[wide['experiment']=='adapt250']
        if R_or_slope == 'R': columns = ['R_session1', 'R_session2']
        else: columns = ['slope_session1', 'slope_session2']
        order = [1.0, 2.0]
        x = None
        y = None
        alternative = 'two-sided'
        pairing = 'paired'
        palette = ['lightgrey', 'lightgrey']

    if comparison == 'session_order_exp2':
        title='Session order - Exp2'
        df = wide[wide['experiment']=='adapt0']
        if R_or_slope == 'R': columns = ['R_session1', 'R_session2']
        else: columns = ['slope_session1', 'slope_session2']
        order = [1.0, 2.0]
        x = None
        y = None
        alternative = 'two-sided'
        pairing = 'paired'
        palette = ['lightgrey', 'lightgrey']

    if comparison == 'adapt':
        title='Adapt sessions (Exp 1 vs 2)'
        df = wide
        if R_or_slope == 'R': columns = ['experiment', 'R_adapt']
        else: columns = ['experiment', 'slope_adapt']
        order = df[columns[0]].unique()
        x = columns[0]
        y = columns[1]
        alternative = 'less'
        pairing = 'unpaired'
        light_red = (1.0, 0.3, 0.3, 0.20)
        light_blue = (0.3, 0.5, 1.0, 0.20)
        palette = [light_red, light_blue]

    if comparison == 'unadapt':
        title='Unadapt sessions (Exp 1 vs 2)'
        df = wide
        if R_or_slope == 'R': columns = ['experiment', 'R_unadapt']
        else: columns = ['experiment', 'slope_unadapt']
        order = df[columns[0]].unique()
        x = columns[0]
        y = columns[1]
        alternative = 'two-sided'
        pairing = 'unpaired'
        light_green = (0.2, 0.8, 0.2, 0.12)
        palette = [light_green, light_green]

    if comparison == 'adapt250_alone':
        title='Adapt250 vs 0'
        df = wide[wide['experiment']=='adapt250']
        if R_or_slope == 'R': columns = ['R_adapt']
        else: columns = ['slope_adapt']
        alternative = 'greater'
        pairing = 'against_0'
        order = None
        x = None
        y = None
        palette = None
        
    if comparison == 'adapt0_alone':
        title='Adapt0 vs 0'
        df = wide[wide['experiment']=='adapt0']
        if R_or_slope == 'R': columns = ['R_adapt']
        else: columns = ['slope_adapt']
        alternative = 'less'
        pairing = 'against_0'
        order = None
        x = None
        y = None
        palette = None
        
    if comparison == 'unadapt_alone':
        title='Unadapt vs 0'
        df = wide
        if R_or_slope == 'R': columns = ['R_unadapt']
        else: columns = ['slope_unadapt']
        alternative = 'two-sided'
        pairing = 'against_0'
        order = None
        x = None
        y = None
        palette = None

    if comparison == 'unadapt_alone_exp1':
        title='Unadapt vs 0 - Exp1'
        df = wide[wide['experiment']=='adapt250']
        if R_or_slope == 'R': columns = ['R_unadapt']
        else: columns = ['slope_unadapt']
        alternative = 'two-sided'
        pairing = 'against_0'
        order = None
        x = None
        y = None
        palette = None

    if comparison == 'unadapt_alone_exp2':
        title='Unadapt vs 0 - Exp2'
        df = wide[wide['experiment']=='adapt0']
        if R_or_slope == 'R': columns = ['R_unadapt']
        else: columns = ['slope_unadapt']
        alternative = 'two-sided'
        pairing = 'against_0'
        order = None
        x = None
        y = None
        palette = None

    if comparison == 'adapt250(exp1) vs unadapt(exp2)':
        title='adapt250(exp1) vs unadapt(exp2)'
        df = df_results.loc[
            ((df_results["experiment"] == "adapt250") & (df_results["session"] == "adapt")) |
            ((df_results["experiment"] == "adapt0") & (df_results["session"] == "unadapt"))
        ].copy()
        if R_or_slope == 'R': columns = ['experiment', 'R']
        else: columns = ['experiment', 'slope']
        order = ['adapt250 (exp1)', 'unadapt (exp2)']
        x = columns[0]
        y = columns[1]
        alternative = 'less'
        pairing = 'unpaired'
        light_green = (0.2, 0.8, 0.2, 0.12)
        light_blue = (0.3, 0.5, 1.0, 0.20)
        palette = [light_blue, light_green]

    return df, title, columns, order, x, y, palette, pairing, alternative

def plot_the_violin(comparison, wide, df_results, R_or_slope):

    df, title, columns, order, x, y, palette, pairing, _ = variables_for_specific_comparisons(comparison, wide, df_results, R_or_slope)
    
    # Preparing the figure
    plt.figure(figsize=(7,6))

    # Long format is needed to assign the hue
    if x is None:
        df_plot = df[columns].melt(var_name='condition', value_name='value')
        x_plot, y_plot = 'condition', 'value'
    else:
        df_plot = df[columns]
        x_plot, y_plot = x, y

    # Plotting the violin
    sns.violinplot(
        data=df_plot,
        x=x_plot,
        y=y_plot,
        hue=x_plot,
        legend=False,
        inner='box',
        palette=palette,
        cut=0)

    # Make the colors pale (seaborn does not apply the transparency of the palette)
    for violin, color in zip(plt.gca().collections, palette):
        violin.set_facecolor(color)

    # Add scatter points (on top, aligned with correct x positions) (chatgpt)
    sns.stripplot(
        data=df_plot,
        x=x_plot,
        y=y_plot,
        color='black',
        size=10,
        jitter=False)

    # Add individual gray lines if paired data
    if pairing == 'paired':

        for _, row in df.iterrows(): # For each participant
            plt.plot(
                [0, 1],
                [row[columns[0]], row[columns[1]]],
                color='gray', alpha=0.8, linewidth=1
            )
            if add_participants_initial: # Add participant label near the adapt point
                plt.text(
                    1 + 0.05,   # move slightly to the right
                    row[columns[1]],
                    row['participant'],
                    fontsize=20,
                    color='black',
                    ha='left',
                    va='center')

    # Add labels and set some limits
    ax = plt.gca()
    if R_or_slope == 'R':
        plt.ylim([-1, 1]) 
        ax.set_yticks([-1, -0.5, 0, 0.5, 1])
        ax.set_yticklabels([-1, -0.5, 0, 0.5, 1])
        plt.ylabel('R value', fontsize=20)
    else:
        plt.ylabel('Slope', fontsize=20)
    plt.title(title, fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([label.capitalize() if isinstance(label, str) else label for label in order])
    ax.set_xlabel('' if x is None else x, fontsize=20)

    # Save and show
    plt.tight_layout()
    plt.savefig(os.path.join(figures_folder,'violin_'+R_or_slope+'_'+elim+'_'+comparison.replace(' ','_')+'.png'), dpi=300)
    plt.show()

def compute_the_stats(comparison, wide, df_results, R_or_slope):

    df, title, columns, order, _, _, _, pairing, alternative = variables_for_specific_comparisons(comparison, wide, df_results, R_or_slope)

    print('\n*************** ' + title + ' ***************')
    print(pairing)
    print('alternative: ' + alternative)

    if pairing == 'paired':

        var1 = df[columns[0]]
        var2 = df[columns[1]]
        print(columns[0] + ': %.2f +/- %.2f' %(var1.mean(), var1.std()))
        print(columns[1] + ': %.2f +/- %.2f' %(var2.mean(), var2.std()))

        if shapiro(var1 - var2)[1]>0.05:
            a = ttest_rel(var1, var2, alternative=alternative)
            d = (var1 - var2).mean() / (var1 - var2).std(ddof=1)
            print("(Paired t-test): t(%d)=%.2f; p=%.3g; Cohen's effect size d=%.2f" %(a.df, a.statistic, a.pvalue, np.abs(d)))
        else:
            a = pg.wilcoxon(var1, var2, alternative=alternative)
            print('(Wilcoxon signed-rank test): W=%2d; p=%3g; effect size (RBC)=%.2f; CLES=%.2f' %(a['W-val'].iloc[0], a['p-val'].iloc[0], a['RBC'].iloc[0], a['CLES'].iloc[0]))
        
    if pairing == 'as_unpaired':

        var1 = df[columns[0]]
        var2 = df[columns[1]]
        print(columns[0] + ': %.2f +/- %.2f' %(var1.mean(), var1.std()))
        print(columns[1] + ': %.2f +/- %.2f' %(var2.mean(), var2.std()))

        if shapiro(var1)[1]>0.05 and shapiro(var2)[1]>0.05:
            a = ttest_ind(var1, var2, equal_var=False, alternative=alternative)
            # cohen_s = ((len(var1)-1)*np.std(var1)**2+(len(var2)-1)*np.std(var2)**2)/(len(var1)+len(var2)-2)
            cohen_s = np.sqrt(
                ((len(var1)-1)*np.std(var1, ddof=1)**2 +
                (len(var2)-1)*np.std(var2, ddof=1)**2)
                / (len(var1)+len(var2)-2)
            )
            cohen_d = np.abs(np.mean(var1)-np.mean(var2))/cohen_s
            print('(Unpaired t-test): t(%.1f)=%.2f; p=%.3g; effect size d=%.2f' %(a.df, a.statistic, a.pvalue, cohen_d))
        else: 
            a2 = pg.mwu(var1, var2, alternative=alternative)
            print('(pingouin Mann-Whitney): U=%.2f; p=%.3g; effect size r(rb)=%.2f' %(a2['U-val'].MWU, a2['p-val'].MWU, a2['RBC'].MWU))

    elif pairing=='unpaired':
        var1 = df[df[columns[0]]=='adapt0'][columns[1]]
        var2 = df[df[columns[0]]=='adapt250'][columns[1]]
        if comparison == 'adapt250(exp1) vs unadapt(exp2)':
            label1, label2 = 'unadapt (exp2)', 'adapt250 (exp1)'
        else:
            label1, label2 = 'adapt0', 'adapt250'
        print(label1 + ': %.2f +/- %.2f' %(var1.mean(), var1.std()))
        print(label2 + ': %.2f +/- %.2f' %(var2.mean(), var2.std()))

        if shapiro(var1)[1]>0.05 and shapiro(var2)[1]>0.05:
            a = ttest_ind(var1, var2, equal_var=False, alternative=alternative)
            cohen_s = np.sqrt(
                ((len(var1)-1)*np.std(var1, ddof=1)**2 +
                (len(var2)-1)*np.std(var2, ddof=1)**2)
                / (len(var1)+len(var2)-2)
            )
            cohen_d = np.abs(np.mean(var1)-np.mean(var2))/cohen_s
            print('(Unpaired t-test): t(%.1f)=%.2f; p=%.3g; effect size d=%.2f' %(a.df, a.statistic, a.pvalue, cohen_d))
        else: 
            a2 = pg.mwu(var1, var2, alternative=alternative)
            print('(pingouin Mann-Whitney): U=%.2f; p=%.3g; effect size r(rb)=%.2f' %(a2['U-val'].MWU, a2['p-val'].MWU, a2['RBC'].MWU))

    elif pairing == 'against_0':

        var1 = df[columns[0]]
        print(comparison)
        print('%.2f +/- %.2f' %(var1.mean(), var1.std()))

        if shapiro(var1)[1]>0.05:
            a = ttest_1samp(var1, 0, alternative=alternative) 
            print('(t-test) t(%d) = %.2f; p = %.3g; Cohen d=%.2f' % (a.df, a.statistic, a.pvalue, np.abs(var1.mean()/var1.std(ddof=1))))
        else: 
            a2 = pg.wilcoxon(var1, alternative=alternative)
            print('(pingouin Wilcoxon) W = %.2f; p = %.3g; effect size r(rb)=%.2f' % (a2['W-val'].Wilcoxon, a2['p-val'].Wilcoxon, a2['RBC'].Wilcoxon))


def fisher_z_diff(r1, r2, n1, n2, alternative='two-sided'):
    """
    Compare two independent correlation coefficients using Fisher's r-to-z.

    Parameters
    ----------
    r1, r2 : float
        Correlation coefficients from sample 1 and sample 2.
    n1, n2 : int
        Sample sizes for each correlation.
    alternative : str
        'two-sided', 'less' (r1 < r2) or 'greater' (r1 > r2).

    Returns
    -------
    Z-score for the difference between correlations, p value.
    """
    # Fisher r-to-z transformation
    z1 = 0.5 * math.log((1 + r1) / (1 - r1))
    z2 = 0.5 * math.log((1 + r2) / (1 - r2))

    # Standard error for independent samples
    se = math.sqrt(1/(n1 - 3) + 1/(n2 - 3))

    # z value for difference
    z = (z1 - z2) / se

    # p-value (norm.sf rather than 1 - norm.cdf, which rounds very small values to 0)
    if alternative == 'less':
        p = norm.cdf(z)
    elif alternative == 'greater':
        p = norm.sf(z)
    else:
        p = 2 * norm.sf(abs(z))

    return z, p


def split_half_reliability(df, delays_to_eliminate, R_or_slope, n_splits=500):
    """
    Split-half reliability of R (or slope) across participants, within one session.

    The trials of each participant are randomly split in two halves, within each delay
    so that both halves have the same delays. R is computed in each half, and the two
    are correlated across participants. This is averaged over n_splits random splits.

    Returns
    -------
    Split-half r, Spearman-Brown corrected r (reliability for the full number of trials).
    """
    rng = np.random.default_rng(1) # So that the result is the same at each run
    df = df[~df['scheduled_sound_delay'].isin(delays_to_eliminate)]
    participants = [df_participant for _, df_participant in df.groupby('participant')]
    metric = 0 if R_or_slope == 'R' else 2 # Position in what computing_correlation returns

    r_splits = []
    for _ in range(n_splits):
        half1 = []
        half2 = []
        for df_participant in participants:
            delays = df_participant['scheduled_sound_delay'].values
            in_half1 = np.zeros(len(delays), dtype=bool)
            for delay in np.unique(delays):
                trials = np.flatnonzero(delays == delay)
                in_half1[rng.permutation(trials)[:len(trials)//2]] = True
            half1.append(computing_correlation(df_participant[in_half1], [])[metric])
            half2.append(computing_correlation(df_participant[~in_half1], [])[metric])
        r_splits.append(pd.Series(half1).corr(pd.Series(half2)))

    r_half = np.mean(r_splits)

    return r_half, 2*r_half/(1+r_half)


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
# Main Script
# ==========================================

# ************* Path to the folder containing *_clean.csv files *************

# adapt_unadapt_stimadapt_soa is the parent of the analysis folder containing this script
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_folder_adapt = os.path.join(project_folder, 'DATA', 'adapt_unadapt', 'adapt250')
data_folder_immediate = os.path.join(project_folder, 'DATA', 'adapt_unadapt', 'immediate')
results_folder = os.path.join(project_folder, 'results', 'adapt_unadapt')
figures_folder = os.path.join(project_folder, 'figures', 'adapt_unadapt')

os.makedirs(results_folder, exist_ok=True)
os.makedirs(figures_folder, exist_ok=True)

file_pattern_adapt = os.path.join(data_folder_adapt, "*_moose_*_clean.csv")
file_pattern_immediate = os.path.join(data_folder_immediate, "*_moose_*_clean.csv")

# This goes in the name of the saved files
if 0 in delays_to_eliminate:
    elim = 'without-0-ms'
else:
    elim = 'with-0-ms'

# Everything printed from now on is also saved in a text file
sys.stdout = Tee(os.path.join(results_folder,'statistics_output_'+R_or_slope+'_'+elim+'.txt'))

experiments = ['adapt250', 'adapt0']

dataframes = []
results = []


# ************* Load the files and append the results *************

for experiment in experiments:

    if experiment == 'adapt250':
        file_pattern = file_pattern_adapt
    elif experiment == 'adapt0':
        file_pattern = file_pattern_immediate

    for file_path in glob.glob(file_pattern):

        print(f"Processing: {os.path.basename(file_path)}")

        # Define participant and session
        filename = os.path.basename(file_path)
        participant, session, date = extract_info(filename)

        # Load and clean data     
        df = pd.read_csv(file_path)
        df = df.replace("None", np.nan)
        df[["scheduled_sound_delay", "rating"]] = df[["scheduled_sound_delay", "rating"]].astype(float)
        df = df[(df["block_type"] == "test") & (df["correct"] == 1)]
        df = df.drop([
            'participant','session','date','expName','experiment','absolute_time',
            'block_nb','total_trial_nb','this_block_trial_nb','correct_trial_nb',
            'test','correct','psychopyVersion','frameRate','Unnamed: 74','Unnamed: 46'
        ], axis=1, errors='ignore')

        # Add a few columns
        df['participant'] = participant
        df['experiment'] = experiment
        df['session'] = session
        df['date'] = date

        # This is for creating the single dataframe
        dataframes.append(df)

df_all = pd.concat(dataframes, ignore_index=True)

# ************* Find the session order and add this info to the dataframe *************

df_order = df_all.drop_duplicates(subset=['participant', 'session'])
df_order = df_order.sort_values(['participant', 'date'])
df_order['session_order'] = df_order.groupby('participant')['date'].rank(method='first').astype(int)

for participant in df_all['participant'].unique():
    for session in df_all[df_all['participant']==participant]['session'].unique():
        df_all.loc[
            (df_all['participant']==participant) & (df_all['session']==session),
            'session_order'
        ] = df_order.loc[
            (df_order['participant']==participant) & (df_order['session']==session),
            'session_order'
        ].values[0]

# ************* Plotting the sanity check *************

if plotting_the_sanity_check:
    for participant in df_all['participant'].unique():
        for session in df_all[df_all['participant']==participant]['session'].unique():
            df_small = df_all[(df_all['participant'] == participant) & (df_all['session'] == session)]
            sanity_check(df_small, participant, session)

# ************* Plotting the correlations *************

if plotting_the_correlation:
    for participant in df_all['participant'].unique():
        df_participant = df_all[df_all['participant']==participant]
        plotting_correlation(df_participant, R_or_slope, delays_to_eliminate)

# ************* Calculate the correlations *************

for participant in df_all['participant'].unique():

    df_participant = df_all[df_all['participant']==participant]

    for session in df_participant['session'].unique():

        df_session = df_participant[df_participant['session']==session]
        r, p, slope, n = computing_correlation(df_session, delays_to_eliminate)

        results.append({
            "experiment": df_participant['experiment'].unique()[0],
            "participant": participant,
            "session": session,
            "session_order": df_session['session_order'].unique()[0],
            "R": r,
            "p": p,
            "slope": slope,
            "n": n,
            "soa_mean": computing_soa_mean(df_session, delays_to_eliminate),
            })

# Create summary DataFrame
df_results = pd.DataFrame(results)
print("\nSummary of results:")
print(df_results)


#************* Reorganize the data in wide format*************

# Immediate is also an adapt session
df_results['session'] = df_results['session'].replace({'immediate': 'adapt'})

# Tell us which session is first
first_sessions = (
    df_results[df_results['session_order'] == 1]
    .set_index('participant')['session']
)
df_results['first_session'] = df_results['participant'].map(first_sessions)

# Pivot to wide format (adapt vs unadapt)
wide = df_results.pivot_table(
    index=['experiment','participant','first_session'],
    columns='session',
    values=['R','p','slope','n','soa_mean'],
    aggfunc='first'  # because pivot_table requires an aggregation
)

# Flatten multi-index columns
wide.columns = [f"{metric}_{sess}" for metric, sess in wide.columns]

# Reorder columns
col_order = [
    'R_adapt', 'p_adapt', 'slope_adapt', 'n_adapt', 'soa_mean_adapt',
    'R_unadapt', 'p_unadapt', 'slope_unadapt', 'n_unadapt', 'soa_mean_unadapt'
]
wide = wide[[c for c in col_order if c in wide.columns]]

# Reset index 
wide = wide.reset_index()

# Add directly 
wide.loc[wide['first_session']=='adapt', 'R_session1'] = wide.loc[wide['first_session']=='adapt', 'R_adapt']
wide.loc[wide['first_session']=='unadapt', 'R_session1'] = wide.loc[wide['first_session']=='unadapt', 'R_unadapt']
wide.loc[wide['first_session']=='adapt', 'R_session2'] = wide.loc[wide['first_session']=='adapt', 'R_unadapt']
wide.loc[wide['first_session']=='unadapt', 'R_session2'] = wide.loc[wide['first_session']=='unadapt', 'R_adapt']
wide.loc[wide['first_session']=='adapt', 'slope_session1'] = wide.loc[wide['first_session']=='adapt', 'slope_adapt']
wide.loc[wide['first_session']=='unadapt', 'slope_session1'] = wide.loc[wide['first_session']=='unadapt', 'slope_unadapt']
wide.loc[wide['first_session']=='adapt', 'slope_session2'] = wide.loc[wide['first_session']=='adapt', 'slope_unadapt']
wide.loc[wide['first_session']=='unadapt', 'slope_session2'] = wide.loc[wide['first_session']=='unadapt', 'slope_adapt']

# Export
wide.to_csv(os.path.join(results_folder,'results_'+elim+'.csv'))
print(wide)

# ************* Figures for the article (Experiment 1) *************

if plotting_the_article_figures:

    wide_exp1 = wide[wide['experiment']=='adapt250']
    df_exp1 = df_all[df_all['experiment']=='adapt250']

    # All participants: those who started with the unadapt session first (two first rows),
    # then those who started with the adapt session; within each group, sorted by R in the adapt session
    participants_sorted = (wide_exp1
        .assign(group=wide_exp1['first_session'].map({'unadapt': 0, 'adapt': 1}))
        .sort_values(['group', 'R_adapt'], ascending=[True, False])['participant'].tolist())
    plotting_all_participants(df_exp1, participants_sorted, 'session', ['unadapt', 'adapt'], ['Unadapt', 'Adapt'],
                              delays_to_eliminate, 4, 5, 'Fig2_all_participants_'+elim+'.png')

    # Fig. 3: unadapt vs adapt, for the R value and for the SoA mean
    palette = [(0.2, 0.8, 0.2, 0.12), (0.3, 0.5, 1.0, 0.20)]
    order_styles = {'unadapt': ('-', 'Unadapt first'), 'adapt': (':', 'Adapt first')}
    fig, axes = plt.subplots(1, 2, figsize=(14,6))
    plot_article_violin(axes[0], wide_exp1, ['R_unadapt', 'R_adapt'], ['Unadapt', 'Adapt'], palette, 'R value',
                        [-0.5, 1], [-0.5, 0, 0.5, 1], group_styles=order_styles, show_legend=False)
    plot_article_violin(axes[1], wide_exp1, ['soa_mean_unadapt', 'soa_mean_adapt'], ['Unadapt', 'Adapt'], palette, 'Mean SoA',
                        [25, 100], [25, 50, 75, 100], group_styles=order_styles)
    fig.tight_layout(rect=[0, 0, 1, 0.94])

    # Panel letters, aligned with the left of the y-axis labels
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for ax, letter in zip(axes, 'AB'):
        label_box = ax.yaxis.get_label().get_window_extent(renderer)
        x = fig.transFigure.inverted().transform((label_box.x0, 0))[0]
        fig.text(x, ax.get_position().y1 + 0.02, letter, fontsize=22, fontweight='bold', ha='left', va='bottom')

    fig.savefig(os.path.join(figures_folder,'Fig3_violin_R_soa_mean_unadapt_adapt_'+elim+'.png'), dpi=300, bbox_inches='tight')
    plt.show()

# ************* Violin plots *************

for comparison in ['adapt250', 'adapt250 as unpaired', 'adapt0', 'adapt', 'unadapt', 'session_order', 'adapt250(exp1) vs unadapt(exp2)']:
    plot_the_violin(comparison, wide, df_results, R_or_slope)

# ************* Statistical comparison *************

print('\n*************** ' + R_or_slope + ' ***************')
if 0 in delays_to_eliminate:
    print('\n*************** ' + '0 ms delay is NOT in the correlation' + ' ***************')
else:
    print('\n*************** ' + '0 ms delay IS in the correlation' + ' ***************')

for comparison in ['adapt250', 'adapt250 as unpaired', 'adapt0', 'adapt', 'unadapt', 'session_order', 'session_order_exp1', 'session_order_exp2', 'adapt250_alone', 'adapt0_alone', 'unadapt_alone', 'unadapt_alone_exp1', 'unadapt_alone_exp2', 'adapt250(exp1) vs unadapt(exp2)']:
    compute_the_stats(comparison, wide, df_results, R_or_slope)

# Mean SoA (independent of R_or_slope)
compute_the_stats('adapt250 soa_mean', wide, df_results, R_or_slope)

# ************* Fisher test *************

# Count the number of significant t-test for p adapt and p unadapt

print('\n+ *************** Tests that Gérard suggested ***************')

print('\n+ 1. Counting the number of participants for which R is significantly different in the 2 sessions, in the predicted direction')
for experiment in ['adapt250', 'adapt0']:
    count = 0
    df_fish = wide[wide['experiment']==experiment]
    if experiment == 'adapt250':
        alternative = 'less' # R_unadapt < R_adapt
    else:
        alternative = 'greater' # R_unadapt > R_adapt
    for _, row in df_fish.iterrows():
        z, p = fisher_z_diff(row['R_unadapt'], row['R_adapt'], row['n_unadapt'], row['n_adapt'], alternative)
        if p < 0.05:
            count += 1
    print('For %s, there are %d participants (out of %d) with a R significantly different in the adapt and unadapt sessions' %(experiment, count, len(df_fish)))

print('\n+ 2. Treating all datapoints from all participants as if it was a single participant')
print('WARNING: this test may not be appropriate, and its p values should be considered as descriptive only.')
print('It assumes that all trials are independent, but trials from the same participant are not.')
print('In addition, for adapt250, adapt0 and session_order, the same participants are in both groups, whereas the test assumes independent correlations.')
print('The p values are therefore probably too small. The paired tests and the ANOVA above and below are more appropriate.')
for comparison in ['adapt250', 'adapt0', 'adapt', 'unadapt', 'session_order']:
    if comparison == 'adapt250':
        df1 = df_all[(df_all['experiment']=='adapt250') & (df_all['session']=='unadapt')]
        df2 = df_all[(df_all['experiment']=='adapt250') & (df_all['session']=='adapt')]
        alternative = 'less'
    if comparison == 'adapt0':
        df1 = df_all[(df_all['experiment']=='adapt0') & (df_all['session']=='unadapt')]
        df2 = df_all[(df_all['experiment']=='adapt0') & (df_all['session']=='immediate')]
        alternative = 'greater'
    if comparison == 'adapt':
        df1 = df_all[(df_all['experiment']=='adapt250') & (df_all['session']=='adapt')]
        df2 = df_all[(df_all['experiment']=='adapt0') & (df_all['session']=='immediate')]
        alternative = 'greater'
    if comparison == 'unadapt':
        df1 = df_all[(df_all['experiment']=='adapt250') & (df_all['session']=='unadapt')]
        df2 = df_all[(df_all['experiment']=='adapt0') & (df_all['session']=='unadapt')]
        alternative = 'two-sided'
    if comparison == 'session_order':
        df1 = df_all[(df_all['session_order']==1)]
        df2 = df_all[(df_all['session_order']==2)]
        alternative = 'two-sided'
    r1, _, _, n1 = computing_correlation(df1, delays_to_eliminate)
    r2, _, _, n2 = computing_correlation(df2, delays_to_eliminate)
    z, p = fisher_z_diff(r1, r2, n1, n2, alternative)
    print('For the comparison ' + comparison +' (' + alternative + '), the p value for testing the difference of R between the two sessions is: '+str(p))

print('\n+ 3. ANOVA on experiment * session')

aov = pg.mixed_anova(
    dv=R_or_slope,
    within='session',
    between='experiment',
    subject='participant',
    data=df_results
)
print(aov)

print('\n+ 4. ANOVA on experiment * session_order')

aov = pg.mixed_anova(
    dv=R_or_slope,
    within='session_order',
    between='experiment',
    subject='participant',
    data=df_results
)
print(aov)

# ************* Quick check of the correlation adapt unadapt *************

wide_quicktest = wide[wide['experiment']=='adapt250']
r, p = pearsonr(wide_quicktest['R_adapt'], wide_quicktest['R_unadapt'])
print('\n+ Correlation between R_adapt and R_unadapt in adapt250: r=%.2f; p=%.3g' %(r, p))

# ************* Stability of the individual differences across sessions (ICC) *************

# ICC3 (consistency) rather than absolute agreement, because adaptation is expected to shift the mean between sessions
df_icc = wide_quicktest.melt(
    id_vars='participant',
    value_vars=[R_or_slope+'_unadapt', R_or_slope+'_adapt'],
    var_name='session',
    value_name='value'
)
icc = pg.intraclass_corr(data=df_icc, targets='participant', raters='session', ratings='value').set_index('Type').loc['ICC3']
print('\n+ ICC(3,1) between the adapt and unadapt sessions in adapt250 (%s): ICC=%.2f; 95%% CI [%.2f, %.2f]; F(%d,%d)=%.2f; p=%.3g' %(
    R_or_slope, icc['ICC'], icc['CI95%'][0], icc['CI95%'][1], icc['df1'], icc['df2'], icc['F'], icc['pval']))

# ************* Split-half reliability within each session *************

print('\n+ Split-half reliability within each session in adapt250 (%s)' %(R_or_slope))
for session in ['unadapt', 'adapt']:
    df_split = df_all[(df_all['experiment']=='adapt250') & (df_all['session']==session)]
    r_half, r_corrected = split_half_reliability(df_split, delays_to_eliminate, R_or_slope)
    print('%s: split-half r=%.2f; Spearman-Brown corrected=%.2f' %(session, r_half, r_corrected))

# ************* Stop saving what is printed *************

sys.stdout.file.close()
sys.stdout = sys.stdout.console