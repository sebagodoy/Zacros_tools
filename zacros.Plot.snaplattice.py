#!/usr/bin/env python3
# read and plot lattices

# Check files
with open('./lattice_output.txt') as f:
    latout = f.readlines()

# attempt to get site types, surf spaces and dentates
with open('./lattice_input.dat') as g:
    for iLine in g.readlines():
        if 'site_type_names' in iLine:
            site_names = [i for i in iLine.split()[1:]]

# attempt to get site types, surf spaces and dentates
with open('./simulation_input.dat') as h:
    for iLine in h.readlines():
        if 'surf_specs_names' in iLine:
            surf_specs_names = iLine.split()[1:]
        if 'surf_specs_dent' in iLine:
            surf_specs_dent = [int(i) for i in iLine.split()[1:]]




# Get coords: site_dict dictionary of sites by index
lat_cell = [[float(i) for i in latout[j].split()[1:3]] for j in range(2)]
site_dict = {}
site_type = {}
nsites = 0
for isite in latout[2:]:
    isite_ = isite.split()
    site_type[int(isite_[3])] = {'x':[], 'y':[], 'site_num':[]}
    site_dict[int(isite_[0])] = {'site_type': int(isite_[3]),
                                 'position':[float(i) for i in isite_[1:3]],
                                 'coordination': int(isite_[4]),
                                 'neighbours': [int(i) for i in isite_[5:] if not i=='0']
                                 }
    nsites += 1
# for debug dictionary of sites by index
[print(str(i)+' = '+site_dict[i].__str__()) for i in site_dict]; print('-'*80)

# Get coords: site_types dictionary of sites by site type
for i in list(site_dict.keys()):
    isite = site_dict[i]
    site_type[isite['site_type']]['x'].append(isite['position'][0])
    site_type[isite['site_type']]['y'].append(isite['position'][1])
    site_type[isite['site_type']]['site_num'].append(i)

# debug
# for i in list(site_type.keys()):
#     [print(str(i)+'-'+str(j)+'='+str(site_type[i][j])) for j in list(site_type[i].keys())]
#     print('.'*20)
# print('-'*80)

# -----------------------------------------------------------------------
# Read history
with open('./history_output.txt') as h:
    snapfile = h.readlines()

# species dict: {1: SpecieName1, 2: SpecieName2, ... }
species_dct = {i+1:j for i,j in enumerate(snapfile[1].split()[1:])}
# species in sites dict: {1: [], 2:[], 3:[] , ...}
snapspecies = {i:[] for i in list(species_dct.keys())} # {specie number : [site list]}




# find starting last snap
iLine = len(snapfile)-1
while iLine>0 and 'configuration' not in snapfile[iLine]:
    iLine-=1

# Fill snapspecies with last snapshot
try:
    for isite in range(nsites):
        thisSite = snapfile[iLine+isite+1].split()
        if not thisSite[2] == '0':
            snapspecies[int(thisSite[2])].append(int(thisSite[0]))
except IndexError:
    print('  > '+'!'*80)
    print('  > '+'!'*4+' The last snapshot is not complete, check what happened!')
    print('  > ' + '!' * 80)
    quit()


# ----------------------------------------------------------------------
# plotting
import matplotlib.pyplot as plt
ncolspecies = int(len(species_dct)/8) if int(len(species_dct)/8) > 0 else 1
fig, ax = plt.subplots(1,1, figsize=(7+1.06*ncolspecies,4.), dpi=80)
plt.subplots_adjust(left=0.09, right=0.94-.11*ncolspecies+.01*(ncolspecies-1),
                    top=0.95, bottom=0.12)
ax.set_aspect('equal', adjustable='box')


# add sites
for itype in list(site_type.keys()):
    plt.scatter(site_type[itype]['x'], site_type[itype]['y'],
                alpha=.15, marker='o', s=80, edgecolors='k',
                zorder=2
                )

# add box
if input('  > Add box (*/def=False) ?: '):
    draw_box = [[0,0], lat_cell[0], [i+j for i, j in zip(lat_cell[0], lat_cell[1])], lat_cell[1], [0,0]]
    plt.plot([i[0] for i in draw_box], [i[1] for i in draw_box], color='k', alpha=.5, linestyle='dashed')

# add species
for ispecie in snapspecies:
    if len(snapspecies[ispecie]) == 0:
        pass
    else:
        plt.scatter([site_dict[j]['position'][0] for j in snapspecies[ispecie]],
                    [site_dict[j]['position'][1] for j in snapspecies[ispecie]],
                    label=species_dct[ispecie],
                    marker='$'+str(ispecie)+'$',
                    s=60, alpha=.9, zorder=4
                    )

# Titles and legend --------------------------------------------------
plt.annotate('Species :', xy=(1.02, .95), xycoords='axes fraction',
             fontweight='bold')
plt.legend(loc='upper left', bbox_to_anchor=(1., .95)
           )

plt.show()





