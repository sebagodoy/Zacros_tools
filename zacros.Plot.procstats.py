#!/usr/bin/env python3

print('  > Check Zacros procstat_output type file')
myfile = input('  > Input file (def = ./procstat_output.txt) : ') or './procstat_output.txt'
try:
    # Open file
    with open(myfile) as f:
        cont = f.readlines()
except FileNotFoundError as notfound:
    print('  >' + '!' * 50 + '\n  >! There is no ' + notfound.filename + ' file. Bye!')
    quit()

# Get events dict
events = cont[0].split()[1:]
allwaittimes =  [float(i) for i in cont[-2].split()[1:]]
alloccurences = [int(i) for i in cont[-1].split()[1:]]
unique_events = list(dict.fromkeys([iev[:-4] if iev[-4:] in ['_rev', '_fwd'] else iev for iev in events]))

# parse into dict
print('  > Parsing ... ')
wait_times = {i: {'fwd': 0, 'rev': 0} for i in unique_events}
event_occurrences = {i: {'fwd': 0, 'rev': 0} for i in unique_events}
for iev, iocc, itim in zip(events, alloccurences, allwaittimes):
    if iev[-4:] in ['_rev', '_fwd']:
        wait_times[iev[:-4]][iev[-3:]] = itim
        event_occurrences[iev[:-4]][iev[-3:]] = iocc
    else:
        wait_times[iev]['fwd'] = itim
        event_occurrences[iev]['fwd'] = iocc

# plot -----------------------------------------------------------------------
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1, figsize=(9, 4.), dpi=80)
plt.subplots_adjust(left=0.25, right=0.98, top=0.95, bottom=0.15)

diff = 0.2
myheight = .3
ypositions = [i+1 for i in range(len(list(event_occurrences.keys())))]
uselog = True

plotwhat = input('  > plot what? (\'time\', def=\'events\') : ') or 'events'

if plotwhat == 'events':
    plotthis = event_occurrences
    myaxis = '# Event occurrences'
elif plotwhat == 'time':
    plotthis = wait_times
    myaxis = 'Average waiting times (all simulation)'
else:
    print('  >! What? ,'+plotwhat+ ' is not an option, use: \'time\', \'events\' or just enter')
    quit()

# plot
ax.barh([i+diff for i in ypositions],
         [plotthis[k]['fwd'] for k in list(plotthis.keys())],
        height=myheight, color='r', log=uselog)
ax.barh([i-diff for i in ypositions],
         [plotthis[k]['rev'] for k in list(plotthis.keys())],
        height=myheight, color='b', log=uselog)

# nice details
nicelabeldict = {'H_diffusion': r'$H* + * \rightarrow * + H*$',
                 'CO_diffusion': r'$CO* + * \rightarrow * + CO*$',
                 'H2_ads': r'$H_2 + 2* \rightarrow 2H*$',
                 'CO2_ads': r'$CO_2 + * \rightarrow CO_2*$',
                 'CO_ads': r'$CO + * \rightarrow CO*$',
                 'H2O_formation': r'$*H + *OH \rightarrow H_2O + 2*$',
                 'OH_formation': r'$*H + *O \rightarrow *OH + *$',
                 'CH4_formation_release': r'$*CH_3 + *H \rightarrow CH_4 + 2*$',
                 'CH3_formation': r'$*CH_2 + *H \rightarrow *CH_3 + *$',
                 'CH2_formation': r'$*CH + *H \rightarrow *CH_2 + *$',
                 'CH_formation': r'$*C + *H \rightarrow *CH + *$',
                 'HCO_dicosc': r'$*HCO + * \rightarrow *O + *CH$',
                 'HCO_formation': r'$*CO + *H \rightarrow *HCO + *$',
                 'COH_disosc': r'$*COH + * \rightarrow *C + *OH$',
                 'COH_formation': r'$*CO + *H \rightarrow *COH + *$',
                 'CO_direct_disoc': r'$*CO + * \rightarrow *C + *O$',
                 'CO2_dissoc': r'$*CO_2 + * \rightarrow *CO + *O$'}
ax.set_ylim(ymin=0)
ax.set_yticks(ypositions,
              [nicelabeldict[i] if i in list(nicelabeldict.keys()) else i for i in list(plotthis.keys())])
plt.xlabel(myaxis, fontweight='bold')
plt.ylabel('procstat: process information', fontweight='bold')
ax.grid(linestyle='dotted')
print('  > Showing plot!')
plt.show()
