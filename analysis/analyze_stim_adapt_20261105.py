import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, ttest_rel, ttest_ind, shapiro, ttest_1samp, spearmanr
import glob, os, sys
import pingouin as pg

# ==========================================
# General settings
# ==========================================

plotting_the_sanity_check = False
plotting_the_sanity_check2 = False
plotting_the_correlation = False
plotting_the_article_figures = True
add_participants_initial = False
comp_value = 'R' # 'slope'
# comp_value = 'slope'
# comp_value = 'soa_mean'
delays_to_eliminate = [-1, 0, 1.25]
# delays_to_eliminate = [-1, 1.25]
corrchoice = 'pearson'


# ==========================================
# Functions
# ==========================================

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


def sanity_check2(df_all, participants):
    """
    Plotting the figure to check that all values are in the correct range
    """

    columns_float = ['fixation_time', 'scheduled_sound_delay',
       'scheduled_jitter', 'clickTime', 'click_x', 'click_y',
       'soundON', 'scheduled_moose_time', 'moose_time', 'rating',
       'rating_time']
    
    df_all[columns_float] = df_all[columns_float].astype(float)

    df_all["delta_sound"] = df_all["scheduled_sound_delay"] - (df_all["soundON"]-df_all["clickTime"])
    df_all["delta_moose_time"] = df_all["moose_time"] - df_all["scheduled_moose_time"]

    columns_to_plot = ['fixation_time', 'scheduled_jitter', 
        'rating_time','rating',
        'clickTime', 'click_x', 'click_y',
        'scheduled_moose_time', 'moose_time', 'delta_moose_time', 
        'scheduled_sound_delay', 'soundON', 'delta_sound']

    for col in columns_to_plot:
        fig, axes = plt.subplots(4, 12, figsize=(28, 8), constrained_layout=True)
        for participant_nb, participant in enumerate(df_all['participant'].unique()):
            for session_nb, session in enumerate(['session1', 'session2']):
                df = df_all[(df_all['participant'] == participant) & (df_all['session'] == session)]
                j = participant_nb % 12
                base_row = (participant_nb // 12) * 2 
                i = base_row + session_nb
                df[col].plot(kind="hist", ax=axes[i, j], title=participant)
                if j != 0:
                    axes[i, j].set_ylabel('')
                if i != 3:
                    axes[i, j].set_xlabel('')
        fig.suptitle(col)
        plt.tight_layout()
        fig.savefig(os.path.join(figures_folder,'sanity_check2_'+col+'.png'), dpi=300)
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
    # Calculate the mean SoA (mean of the means per delay, so that the many 250 ms trials do not dominate)
    soa_mean = df_calcul.groupby('scheduled_sound_delay')['rating'].mean().mean()

    return r, p, slope, soa_mean
    
    

def plotting_correlation(df_participant, delays_to_eliminate): # Replace session by stim_condition

    fig, axes = plt.subplots(1, 2, figsize=[14, 7])

    for stim_condition in df_participant['stim_condition'].unique():
        df_test = df_participant[df_participant['stim_condition']==stim_condition].copy()
        if stim_condition == "real":
            column = 0
        else:
            column = 1

        r, p, slope, soa_mean = computing_correlation(df_test, delays_to_eliminate)

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
        if stim_condition == 'sham':
            line_color = 'blue'
        elif stim_condition == 'real':
            line_color = 'green'
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
        axes[column].set_title(stim_condition, fontsize=20)
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


def variables_for_specific_comparisons(comparison, wide, comp_value):

    if comparison == 'main':
        title='real vs sham'
        df = wide
        if comp_value == 'R': columns = ['R_real', 'R_sham']
        elif comp_value == 'slope': columns = ['slope_real', 'slope_sham']
        elif comp_value == 'soa_mean': columns = ['soa_mean_real', 'soa_mean_sham']
        order = ['real', 'sham']
        x = None
        y = None
        # Hypothesis: the stimulation impairs the adaptation, so R real < R sham (no prediction for the mean SoA)
        if comp_value in ['R', 'slope']: alternative = 'less'
        else: alternative = 'two-sided'
        pairing = 'paired'
        light_green = (0.2, 0.8, 0.2, 0.12)
        light_blue = (0.3, 0.5, 1.0, 0.20)
        palette = [light_green, light_blue]

    if comparison == 'order':
        title='Session order'
        df = wide
        if comp_value == 'R': columns = ['R_session1', 'R_session2']
        elif comp_value == 'slope': columns = ['slope_session1', 'slope_session2']
        elif comp_value == 'soa_mean': columns = ['soa_mean_session1', 'soa_mean_session2']
        order = [1.0, 2.0]
        x = None
        y = None
        alternative = 'two-sided'       
        pairing = 'paired'
        palette = ['lightgrey', 'lightgrey']

    if comparison == 'first_session':
        title='First session (real first vs sham first)'
        df = wide
        if comp_value == 'R': columns = ['first_session', 'R_session1']
        elif comp_value == 'slope': columns = ['first_session', 'slope_session1']
        elif comp_value == 'soa_mean': columns = ['first_session', 'soa_mean_session1']
        order = ['real', 'sham']
        x = columns[0]
        y = columns[1]
        # Stimulation effect in the first session only (before participants could compare the two conditions): same hypothesis as the main comparison
        if comp_value in ['R', 'slope']: alternative = 'less'
        else: alternative = 'two-sided'
        pairing = 'unpaired'
        light_green = (0.2, 0.8, 0.2, 0.12)
        light_blue = (0.3, 0.5, 1.0, 0.20)
        palette = [light_green, light_blue]

    if comparison == 'real_alone':
        title='real vs 0'
        df = wide
        if comp_value == 'R': columns = ['R_real']
        elif comp_value == 'slope': columns = ['slope_real']
        elif comp_value == 'soa_mean': columns = ['soa_mean_real']
        alternative = 'greater'
        pairing = 'against_0'
        order = None
        x = None
        y = None
        palette = None
        
    if comparison == 'sham_alone':
        title='sham vs 0'
        df = wide
        if comp_value == 'R': columns = ['R_sham']
        elif comp_value == 'slope': columns = ['slope_sham']
        elif comp_value == 'soa_mean': columns = ['soa_mean_sham']
        alternative = 'greater'
        pairing = 'against_0'
        order = None
        x = None
        y = None
        palette = None

    return df, title, columns, order, x, y, palette, pairing, alternative


def plot_the_violin(comparison, wide, comp_value):

    df, title, columns, order, x, y, palette, pairing, _ = variables_for_specific_comparisons(comparison, wide, comp_value)
    
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
            if add_participants_initial: # Add participant label near the real point
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
    if comp_value == 'R':
        plt.ylim([-1, 1]) 
        ax.set_yticks([-1, -0.5, 0, 0.5, 1])
        ax.set_yticklabels([-1, -0.5, 0, 0.5, 1])
        plt.ylabel('R value', fontsize=20)
    elif comp_value == 'slope':
        plt.ylabel('Slope', fontsize=20)
    elif comp_value == 'soa_mean':
        plt.ylabel('Mean SoA', fontsize=20)
    plt.title(title, fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([{'real': 'rAG', 'sham': 'Sham'}.get(label, label) for label in order])
    ax.set_xlabel('' if x is None else x, fontsize=20)

    # Save and show
    plt.tight_layout()
    plt.savefig(os.path.join(figures_folder,'violin_'+comp_value+'_'+elim+'_'+comparison+'.png'), dpi=300)
    plt.show()


def compute_the_stats(comparison, wide,comp_value):

    df, title, columns, order, _, _, _, pairing, alternative = variables_for_specific_comparisons(comparison, wide, comp_value)

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
        
    elif pairing == 'unpaired':

        var1 = df[df[columns[0]]=='real'][columns[1]]
        var2 = df[df[columns[0]]=='sham'][columns[1]]
        print('real first (n=%d): %.2f +/- %.2f' %(len(var1), var1.mean(), var1.std()))
        print('sham first (n=%d): %.2f +/- %.2f' %(len(var2), var2.mean(), var2.std()))

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


def split_half_reliability(df, delays_to_eliminate, comp_value, n_splits=500):
    """
    Split-half reliability of R (or slope or soa_mean) across participants, within one condition.

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
    metric = {'R': 0, 'slope': 2, 'soa_mean': 3}[comp_value] # Position in what computing_correlation returns

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
data_folder = os.path.join(project_folder, 'DATA', 'stim_adapt')
blind_file = os.path.join(project_folder, 'psychopy', 'stim_adapt', 'blind', 'double_blind.csv')
results_folder = os.path.join(project_folder, 'results', 'stim_adapt')
figures_folder = os.path.join(project_folder, 'figures', 'stim_adapt')

os.makedirs(results_folder, exist_ok=True)
os.makedirs(figures_folder, exist_ok=True)

# This goes in the name of the saved files
if 0 in delays_to_eliminate:
    elim = 'without-0-ms'
else:
    elim = 'with-0-ms'

# Everything printed from now on is also saved in a text file
sys.stdout = Tee(os.path.join(results_folder,'statistics_output_'+comp_value+'_'+elim+'.txt'))

participants = ['s033', 's034', 's035', 's036', 's037', 's038', 's039', 's040', 's041', 's042',
                's043', 's044', 's045', 's046', 's047', 's048', 's049', 's050', 's051', 's052',
                's053', 's054', 's055', 's056']
sessions = ['session1', 'session2']

dataframes = []
results = []

blind = pd.read_csv(blind_file, index_col=0)

# ************* Load the files and append the results *************

for participant in participants:

    for session in sessions:

        pattern = os.path.join(data_folder, participant, session, "*_clean.csv")
        files = glob.glob(pattern)
        if files:
            file_path = files[0]
            filename = os.path.basename(file_path)
            prefix = filename.split("_")[0]
            df = pd.read_csv(file_path)
            stim_condition_AB = blind.loc[prefix, session.capitalize()]
            stim_condition = {
                'SoA_Angular_Gyrus_A': 'real',
                'SoA_Angular_Gyrus_B': 'sham'
            }.get(stim_condition_AB)            
            print(f"Processing: " + participant + ' (' + prefix + ') ' + session + ' ' + stim_condition)
            print("Last trial time since stimulation begin: " + str(df['stim_time'].iloc[-1]))


            df = df.replace("None", np.nan)
            df[["scheduled_sound_delay", "rating"]] = df[["scheduled_sound_delay", "rating"]].astype(float)
            df = df[(df["block_type"] == "test") & (df["correct"] == 1)]
            df = df.drop([
                'gender (M/F)', 'number (1-12)', 'session (1-2)','date','expName','experiment','absolute_time',
                'block_nb','total_trial_nb','this_block_trial_nb','correct_trial_nb',
                'test','correct','psychopyVersion','frameRate','Unnamed: 74','Unnamed: 46', 'Unnamed: 82',
                'mouse.x', 'mouse.y',
                'mouse.leftButton', 'mouse.midButton', 'mouse.rightButton',
                'mouse.time'
            ], axis=1, errors='ignore')

            # Add a few columns
            df['participant'] = participant # Code of the participant's folder (s033, s034...), used for the article
            df['stim_condition'] = stim_condition
            df['session'] = session

            # This is for creating the single dataframe
            dataframes.append(df)

df_all = pd.concat(dataframes, ignore_index=True)

# ************* Plotting the sanity check *************

if plotting_the_sanity_check:
    for participant in df_all['participant'].unique():
        for session in df_all[df_all['participant']==participant]['session'].unique():
            df_small = df_all[(df_all['participant'] == participant) & (df_all['session'] == session)]
            sanity_check(df_small, participant, session)

# ************* Plotting the sanity check2 *************

if plotting_the_sanity_check2:

    sanity_check2(df_all, participants)

# ************* Plotting the correlations *************

if plotting_the_correlation:
    for participant in df_all['participant'].unique():
        df_participant = df_all[df_all['participant']==participant]
        plotting_correlation(df_participant, delays_to_eliminate)

# ************* Calculate the correlations *************

for participant in df_all['participant'].unique():

    df_participant = df_all[df_all['participant']==participant]

    for stim_condition in df_participant['stim_condition'].unique():

        df_stim_condition = df_participant[df_participant['stim_condition']==stim_condition]
        r, p, slope, soa_mean = computing_correlation(df_stim_condition, delays_to_eliminate)

        results.append({
            "participant": participant,
            "stim_condition": stim_condition,
            "order": df_stim_condition['session'].unique()[0],
            "R": r,
            "p": p,
            "slope": slope,
            "soa_mean": soa_mean
            })

# Create summary DataFrame
df_results = pd.DataFrame(results)
print("\nSummary of results:")
print(df_results)


#************* Reorganize the data in wide format*************

# Tell us which session is first
first_sessions = (
    df_results[df_results['order'] == 'session1']
    .set_index('participant')['stim_condition']
)
df_results['first_session'] = df_results['participant'].map(first_sessions)

# Pivot to wide format (real vs sham)
wide = df_results.pivot_table(
    index=['participant','first_session'],
    columns='stim_condition',
    values=['R','p','slope', 'soa_mean'],
    aggfunc='first'  # because pivot_table requires an aggregation
)

# Flatten multi-index columns
wide.columns = [f"{metric}_{sess}" for metric, sess in wide.columns]

# Reorder columns
col_order = [
    'R_real', 'p_real', 'slope_real', 'soa_mean_real',
    'R_sham', 'p_sham', 'slope_sham', 'soa_mean_sham'
]
wide = wide[[c for c in col_order if c in wide.columns]]

# Reset index 
wide = wide.reset_index()

# Add directly 
wide.loc[wide['first_session']=='real', 'R_session1'] = wide.loc[wide['first_session']=='real', 'R_real']
wide.loc[wide['first_session']=='sham', 'R_session1'] = wide.loc[wide['first_session']=='sham', 'R_sham']
wide.loc[wide['first_session']=='real', 'R_session2'] = wide.loc[wide['first_session']=='real', 'R_sham']
wide.loc[wide['first_session']=='sham', 'R_session2'] = wide.loc[wide['first_session']=='sham', 'R_real']
wide.loc[wide['first_session']=='real', 'slope_session1'] = wide.loc[wide['first_session']=='real', 'slope_real']
wide.loc[wide['first_session']=='sham', 'slope_session1'] = wide.loc[wide['first_session']=='sham', 'slope_sham']
wide.loc[wide['first_session']=='real', 'slope_session2'] = wide.loc[wide['first_session']=='real', 'slope_sham']
wide.loc[wide['first_session']=='sham', 'slope_session2'] = wide.loc[wide['first_session']=='sham', 'slope_real']
wide.loc[wide['first_session']=='real', 'soa_mean_session1'] = wide.loc[wide['first_session']=='real', 'soa_mean_real']
wide.loc[wide['first_session']=='sham', 'soa_mean_session1'] = wide.loc[wide['first_session']=='sham', 'soa_mean_sham']
wide.loc[wide['first_session']=='real', 'soa_mean_session2'] = wide.loc[wide['first_session']=='real', 'soa_mean_sham']
wide.loc[wide['first_session']=='sham', 'soa_mean_session2'] = wide.loc[wide['first_session']=='sham', 'soa_mean_real']

# Add delta_R column
wide["delta_R"] = wide["R_real"] - wide["R_sham"]

# Export
wide.to_csv(os.path.join(results_folder,'results_'+elim+'.csv'))
print(wide)

# ************* Figures for the article *************

if plotting_the_article_figures:

    # All participants: those who started with the real stimulation (two first rows),
    # then those who started with the sham; within each group, sorted by R in the sham session
    participants_sorted = (wide
        .assign(group=wide['first_session'].map({'real': 0, 'sham': 1}))
        .sort_values(['group', 'R_sham'], ascending=[True, False])['participant'].tolist())
    plotting_all_participants(df_all, participants_sorted, 'stim_condition', ['real', 'sham'], ['rAG stimulation', 'Sham stimulation'],
                              delays_to_eliminate, 4, 6, 'Fig5_all_participants_'+elim+'.png')

    # Fig. 6: real vs sham, for the R value and for the SoA mean
    palette = [(0.2, 0.8, 0.2, 0.12), (0.3, 0.5, 1.0, 0.20)]
    fig, axes = plt.subplots(1, 2, figsize=(14,6))
    order_styles = {'real': ('-', 'rAG first'), 'sham': (':', 'Sham first')}
    plot_article_violin(axes[0], wide, ['R_real', 'R_sham'], ['rAG\nstimulation', 'Sham\nstimulation'], palette, 'R value', [-0.5, 1], [-0.5, 0, 0.5, 1],
                        group_styles=order_styles, show_legend=False)
    plot_article_violin(axes[1], wide, ['soa_mean_real', 'soa_mean_sham'], ['rAG\nstimulation', 'Sham\nstimulation'], palette, 'Mean SoA', [25, 100], [25, 50, 75, 100],
                        group_styles=order_styles)
    fig.tight_layout(rect=[0, 0, 1, 0.94])

    # Panel letters, aligned with the left of the y-axis labels
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for ax, letter in zip(axes, 'AB'):
        label_box = ax.yaxis.get_label().get_window_extent(renderer)
        x = fig.transFigure.inverted().transform((label_box.x0, 0))[0]
        fig.text(x, ax.get_position().y1 + 0.02, letter, fontsize=22, fontweight='bold', ha='left', va='bottom')
    fig.savefig(os.path.join(figures_folder,'Fig6_violin_R_soa_mean_real_sham_'+elim+'.png'), dpi=300)
    plt.show()

# ************* Violin plots *************

for comparison in ['main', 'order']:
    plot_the_violin(comparison, wide, comp_value)

# ************* Statistical comparison *************

print('\n*************** ' + comp_value + ' ***************')
if 0 in delays_to_eliminate:
    print('\n*************** ' + '0 ms delay is NOT in the correlation' + ' ***************')
else:
    print('\n*************** ' + '0 ms delay IS in the correlation' + ' ***************')

# Comparing the mean SoA against 0 would not be meaningful
if comp_value == 'soa_mean':
    comparisons = ['main', 'order', 'first_session']
else:
    comparisons = ['main', 'real_alone', 'sham_alone', 'order', 'first_session']

for comparison in comparisons:
    compute_the_stats(comparison, wide, comp_value)

# ************* Bayes factors: is the absence of effect meaningful? *************

# The expected effect is the difference adapt-unadapt of Experiment 1 (run analyze_adapt_unadapt first)
file_exp1 = os.path.join(project_folder, 'results', 'adapt_unadapt', 'results_'+elim+'.csv')

if comp_value not in ['R', 'slope']:

    print('\n+ Bayes factors not computed for %s: Experiment 1 does not provide an expected effect for this measure' %(comp_value))

elif not os.path.exists(file_exp1):

    print('\nWARNING: Bayes factors NOT computed, because this file is missing: ' + os.path.relpath(file_exp1, project_folder))
    print('Run analyze_adapt_unadapt_20261105.py first, with the same delays_to_eliminate.')

else:

    df_exp1 = pd.read_csv(file_exp1)
    df_exp1 = df_exp1[df_exp1['experiment']=='adapt250']
    sdtheory = (df_exp1[comp_value+'_adapt'] - df_exp1[comp_value+'_unadapt']).mean()

    distrib = wide[comp_value+'_real'] - wide[comp_value+'_sham']
    obtained = distrib.mean()
    sd = distrib.std(ddof=1)/np.sqrt(distrib.size)

    print('\n*************** Bayes factors (%s) ***************' %(comp_value))
    print('Difference real-sham: %.4f; standard error: %.4f' %(obtained, sd))
    print('SD of p(population value|theory), mean 0: %.4f (difference adapt-unadapt of Experiment 1)' %(sdtheory))
    print('BF<1/3: evidence for no effect; BF>3: evidence for an effect; otherwise: inconclusive')

    for hypothesis, obtained_for_theory, tail in [('real > sham, half-normal', obtained, 1),
                                                  ('real < sham, half-normal', -obtained, 1),
                                                  ('real different from sham, normal', obtained, 2)]:
        Bayesfactor = BayesianFactorsNormal(obtained_for_theory, sd, 0, sdtheory, tail)
        # A difference of R cannot be larger than 2 (R between -1 and 1), so the search stops there
        max_sd = 2
        lower, upper, conclusion, no_upper_limit = robustness_region(obtained_for_theory, sd, 0, sdtheory, tail, max_sd)
        upper_text = '>%g' %(max_sd) if no_upper_limit else '%.3f' %(upper)
        print('%s: BF=%.2f; RR[%s] = [%.3f, %s]' %(hypothesis, Bayesfactor, conclusion, lower, upper_text))

# ************* Quick check of the correlation real sham *************

r, p = pearsonr(wide[comp_value+'_real'], wide[comp_value+'_sham'])
print('\n+ Correlation between real and sham (%s): r=%.2f; p=%.3g' %(comp_value, r, p))

# ************* Stability of the individual differences across sessions (ICC) *************

# ICC3 (consistency) rather than absolute agreement, as stimulation could shift the mean between sessions
df_icc = wide.melt(
    id_vars='participant',
    value_vars=[comp_value+'_real', comp_value+'_sham'],
    var_name='stim_condition',
    value_name='value'
)
icc = pg.intraclass_corr(data=df_icc, targets='participant', raters='stim_condition', ratings='value').set_index('Type').loc['ICC3']
print('\n+ ICC(3,1) between the real and sham sessions (%s): ICC=%.2f; 95%% CI [%.2f, %.2f]; F(%d,%d)=%.2f; p=%.3g' %(
    comp_value, icc['ICC'], icc['CI95%'][0], icc['CI95%'][1], icc['df1'], icc['df2'], icc['F'], icc['pval']))

# ************* Split-half reliability within each condition *************

print('\n+ Split-half reliability within each condition (%s)' %(comp_value))
for stim_condition in ['real', 'sham']:
    df_split = df_all[df_all['stim_condition']==stim_condition]
    r_half, r_corrected = split_half_reliability(df_split, delays_to_eliminate, comp_value)
    print('%s: split-half r=%.2f; Spearman-Brown corrected=%.2f' %(stim_condition, r_half, r_corrected))

# ************* Stop saving what is printed *************

sys.stdout.file.close()
sys.stdout = sys.stdout.console
