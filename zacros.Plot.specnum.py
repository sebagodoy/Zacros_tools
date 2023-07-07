#!/usr/bin/env python3

print('  > Check Zacros specnum_output type file')
myfile = input('  > Input file (def = ./specnum_output.txt) : ') or './specnum_output.txt'
try:
    # Open file
    with open(myfile) as f:
        cont = f.readlines()
except FileNotFoundError as notfound:
    print('  >'+'!'*50+'\n  >! There is no '+ notfound.filename + ' file. Bye!')
    quit()

# Get data
species = {i:[] for i in cont[0].split()[5:]}
stats = {i:[] for i in cont[0].split()[:5]}
# Parse
for iLine in cont[1:]:
    [species[i].append(float(j)) for i,j in zip(species, iLine.split()[5:])]
    [stats[i].append(float(j)) for i,j in zip(stats, iLine.split()[:5])]

#### ---- Plot
import matplotlib.pyplot as plt
ncolspecies = int(len(species)/8) if int(len(species)/8) > 0 else 1
fig, ax = plt.subplots(1,1, figsize=(7+1.06*ncolspecies,4.), dpi=80)
plt.subplots_adjust(left=0.09, right=0.94-.11*ncolspecies+.01*(ncolspecies-1),
                    top=0.95, bottom=0.12)

#### ---- Add species

myxaxis = input('  > x axis? (Entry, Nevents, Time=def ): ') or "Time"
if not myxaxis in stats:
    print('    '+myxaxis+' ... what?, just using Time instead')
    myxaxis = "Time"
plt.xlabel(myxaxis, fontweight='bold')

# numeral markers
numeralmarkers = input('  > Use numeral markers? (True/def=False) : ') or False

# plotting
if numeralmarkers:
    # if all are marked it gets too crowded
    numberOfMarkers = 15
    markEvery = max(int(len(stats[myxaxis])/numberOfMarkers), 1)
    # number markers
    [plt.plot(stats[myxaxis], species[i],
              label=i, marker=f"$" + str(j) + "$", markerfacecolor = 'k', markeredgewidth=0.1,
              markevery=markEvery, markersize=9,
              zorder=10, linestyle=None)
     for j, i in enumerate(species)]
else:
    [plt.plot(stats[myxaxis], species[i], label=i, marker='.', zorder=10) for i in species]


plt.annotate('Species :', xy=(1.02, .95), xycoords='axes fraction', fontweight='bold')


plt.legend(loc='upper left', bbox_to_anchor=(1., .95), ncol=ncolspecies)
plt.ylabel('specnum: number of species', fontweight='bold')

# ---- Add temp
if input('  > Include temp? (*/def=False) : '):
    axT = ax.twinx()
    axT.plot(stats[myxaxis], stats['Temperature'], label='Temp.',
             linestyle='solid', linewidth=7., color='r', zorder=0, marker='.', alpha=.3)
    axT.set_axisbelow(True)
    axT.yaxis.label.set_color('r')
    axT.tick_params(axis='y', colors='r')
    axT.spines['right'].set_linestyle('solid')
    axT.spines['right'].set_linewidth(3.)
    axT.spines['right'].set_color('r')
    axT.spines['right'].set_alpha(.3)
    axT.spines['right'].set_position(('axes',.1))
    axT.set_ylabel('Temp. (K)', labelpad=-38, loc='top', fontweight='bold', color='r')
    plt.legend(loc='upper left', bbox_to_anchor=(1., .2), ncol=ncolspecies)

# ---- Add energy
if input('  > Include energy? (*/def=False) : '):
    axE = ax.twinx()
    axE.plot(stats[myxaxis], stats['Energy'], label='Energy.',
             linestyle='solid', linewidth=7., color='b', zorder=0, marker='.', alpha=.3)
    axE.set_axisbelow(True)
    axE.yaxis.label.set_color('r')
    axE.tick_params(axis='y', colors='b')
    axE.spines['right'].set_linestyle('solid')
    axE.spines['right'].set_linewidth(3.)
    axE.spines['right'].set_color('b')
    axE.spines['right'].set_alpha(.3)
    axE.spines['right'].set_position(('axes',.2))
    axE.set_ylabel('Energy.', labelpad=-38, loc='top', fontweight='bold', color='b')
    plt.legend(loc='upper left', bbox_to_anchor=(1., .1), ncol=ncolspecies)

print('  > Showing plot!')
ax.grid(which='both', linewidth=.5)
plt.show()
