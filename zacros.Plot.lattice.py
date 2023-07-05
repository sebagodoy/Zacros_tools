#!/usr/bin/env python3
# read and plot lattices

# Check files
with open('./lattice_output.txt') as f:
    latout = f.readlines()

# attempt to get site types
with open('./lattice_input.dat') as g:
    for iLine in g.readlines():
        if 'site_type_names' in iLine:
            site_names = [i for i in iLine.split()[1:]]

# Get coords: site_dict dictionary of sites by index
lat_cell = [[float(i) for i in latout[j].split()[1:3]] for j in range(2)]
site_dict = {}
site_type = {}
for isite in latout[2:]:
    isite_ = isite.split()
    site_type[int(isite_[3])] = {'x':[], 'y':[], 'site_num':[]}
    site_dict[int(isite_[0])] = {'site_type': int(isite_[3]),
                                 'position':[float(i) for i in isite_[1:3]],
                                 'coordination': int(isite_[4]),
                                 'neighbours': [int(i) for i in isite_[5:] if not i=='0']
                                 }
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

# plotting
import matplotlib.pyplot as plt
ncolspecies = int(len(site_type)/8) if int(len(site_type)/8) > 0 else 1
fig, ax = plt.subplots(1,1, figsize=(7+1.06*ncolspecies,4.), dpi=80)
plt.subplots_adjust(left=0.09, right=0.94-.11*ncolspecies+.01*(ncolspecies-1),
                    top=0.95, bottom=0.12)
ax.set_aspect('equal', adjustable='box')


for itype in list(site_type.keys()):
    plt.scatter(site_type[itype]['x'], site_type[itype]['y'],
                alpha=.3, marker='o', s=80)
#if input('  > add bonds ? (def=False/*=True) : '):
#    bonds=[]
#    for i in list(site_dict.keys()):
#        for j in site_dict[i]['neighbours']:

# add box
if input('  > Add box (*/def=False) ?: '):
    draw_box = [[0,0], lat_cell[0], [i+j for i, j in zip(lat_cell[0], lat_cell[1])], lat_cell[1], [0,0]]
    plt.plot([i[0] for i in draw_box], [i[1] for i in draw_box], color='k', alpha=.5, linestyle='dashed')


plt.show()





