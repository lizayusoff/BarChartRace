#---------------------------------
# Bar Chart Race on Malaysia Confirmed Cases of Covid-19 by states
#---------------------------------

import pandas as pd
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


colors = plt.cm.Paired(range(10))

df = pd.read_csv('daily_MY_covid_wide.csv', index_col='Date', parse_dates=['Date'], infer_datetime_format=True)
df_status = pd.read_csv('daily_MY_status.csv', index_col='Date', parse_dates=['Date'], infer_datetime_format=True)



def nice_axes(ax):
    ax.set_facecolor('w')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    [spine.set_visible(False) for spine in ax.spines.values()]


def prepare_data(df, steps=5):
    df = df.reset_index()
    df.index = df.index * steps
    last_idx = df.index[-1] + 1
    df_expanded = df.reindex(range(last_idx))
    df_expanded['Date'] = df_expanded['Date'].fillna(method='ffill')
    df_expanded = df_expanded.set_index('Date')
    df_rank_expanded = df_expanded.rank(axis=1, method='first')
    df_expanded = df_expanded.interpolate()
    df_rank_expanded = df_rank_expanded.interpolate()
    return df_expanded, df_rank_expanded

df_expanded, df_rank_expanded = prepare_data(df)

def init():
    ax.clear()
    nice_axes(ax)
   # ax.set_ylim(.2, 6.8)


def update(i):

    print(i)
    ax.clear()
    for bar in ax.containers:
        bar.remove()
    y = df_rank_expanded.iloc[i]
    width = df_expanded.iloc[i]
    labels = df_rank_expanded.columns
    bar1 = ax.barh(y=y, width=width, color=colors, tick_label=labels)
    dx = width.max() / 200

    date_str = df_expanded.index[i].strftime('%B %d, %Y')
    status_str = df_status['Status'].loc[df_expanded.index[i]]



    # Add counts on the right of the bar graphs
    for c,rect in enumerate(bar1):

        width = rect.get_width()

        if y[c] <= 7:

            ax.text(width + dx, rect.get_y() + rect.get_height() / 2.0, '%d' % int(width), ha='left', va='center',size=14
                   , color='#777777')

        if y[c] > 7:
            ax.text(width + dx, rect.get_y() + rect.get_height() / 2.0, '%d' % int(width), ha='left', va='center',
                    size=14, color='#777777')
            ax.text(width - dx, rect.get_y() + rect.get_height() / 2.0, labels[c], ha='right', va='center', size=12)


    ax.text(0, 1.06, 'Number of cases', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    #ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)


    ax.text(0, 1.15, 'Covid-19 : Number of confirmed cases by States in Malaysia',
            transform=ax.transAxes, size=24, weight=600, ha='left', va='top')
    ax.text(1, 0.4, date_str, transform=ax.transAxes, color='#777777', size=46, ha='right',
            weight=750)
    ax.text(0.96, 0.35, str(status_str), transform=ax.transAxes, color='#777777', size=16, ha='right',
            weight=500)
    ax.text(1, 0, 'by @RedChilLiz; credit @TedPetrou, @pratapvardhan', transform=ax.transAxes, color='#777777',
            ha='right',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)
    plt.axis('tight')


fig, ax = plt.subplots(figsize=(15, 8))

anim = FuncAnimation(fig=fig, func=update, init_func=init, frames=len(df_expanded), interval=100, repeat=False)
anim.save('CovidMY_BarChart_smooth_wStatus.mp4')
