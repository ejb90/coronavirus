'''
https://coronavirus.data.gov.uk/developers-guide#methods
'''

import matplotlib.pyplot as plt

import coronavirus


def plot_data_in_time(args, data, var1, var2):
    '''
    '''
    rolling_av = 7
    cutoff = -1*(rolling_av // 2)
    
    
    
    fig = plt.figure(figsize=(18,15))
    
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax2.invert_yaxis()

    ax1.set_ylabel(var1)
    ax2.set_ylabel(var2)
    
    # Plots
    ax1.bar(data.raw_dates, 
            data.values[var1], 
            fc='grey', 
            alpha=0.3,
            label=var1)
    
    ax2.bar(data.raw_dates, 
            data.values[var2], 
            fc='grey', 
            alpha=0.3,
            label=var2)
    
    ax1.plot(range(len(data.dates))[:cutoff], 
             coronavirus.moving_average(data.values[var1], rolling_av)[:cutoff], 
             c='r', 
             lw=2,
             label=f'{var1} 7-day Rolling Average')
    
    ax2.plot(range(len(data.dates))[:cutoff], 
             coronavirus.moving_average(data.values[var2], rolling_av)[:cutoff], 
             c='r', 
             lw=2,
             label=f'{var2} 7-day Rolling Average')
    
    ax1.plot(range(len(data.dates))[:cutoff], 
             10*coronavirus.moving_average_rate(data.values[var1], rolling_av)[:cutoff], 
             c='b', 
             lw=1,
             ls=':',
             label=f'{var1} 7-day Rolling Average Rate (arb. scale)')
    
    
    ax2.plot(range(len(data.dates))[:cutoff], 
             2*coronavirus.moving_average_rate(data.values[var2], rolling_av)[:cutoff], 
             c='b', 
             lw=1,
             ls=':',
             label=f'{var2} 7-day Rolling Average Rate (arb. scale)')
    
    ax1.plot([data.raw_dates.index('2020-03-23')]*2, 
             [0, max(data.values[var1])*1.1], 
             c='g', 
             ls='--',
             label='Day of National Lockdown')
    
    ax2.plot([data.raw_dates.index('2020-03-23')]*2, 
             [0, max(data.values[var2])*1.1], 
             c='g', 
             ls='--',
             label='Day of National Lockdown')
    
    # add legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='lower left')
    
    # Sort out combo ticks
    ax2.xaxis.tick_top()
    ax2.set_xticklabels([None] * len(data.dates))
    
    sparse_xticks = []
    for date in data.dates:
        if date.strftime('%a') == 'Mon':
            sparse_xticks.append(date.strftime('%d %b'))
        else:
            sparse_xticks.append(None)
    ax1.set_xticklabels(sparse_xticks, rotation=90)
    
    ax1.grid(axis='y', which='major')
    ax2.grid(axis='y', which='major')
    plt.xticks(rotation='vertical')

    plt.tight_layout()
    plt.show()




args, data = coronavirus.main()
#plot_data_in_time(args, data, 'newCasesByPublishDate', 'newDeaths28DaysByPublishDate')
plot_data_in_time(args, data, 'newCasesByPublishDate', 'newCasesByPublishDateRate')
    
