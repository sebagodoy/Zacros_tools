# Zacros_tools
Tools to help working with zacros for kinetic montecarlo
* `procstats`: reads procstat_output.txt, plots horizontal bar-plots for forward and reverse events
* `specnum`: reads specnum_output.txt and plots evolution of statistics for species
* `lattice`: reads lattice_input.dat for the site names and lattice_output for site specification. Plots lattice from lattice_output
*  `snaplattice`: reads lattice_output.txt for site specification, lattice_input.dat for site names,
  simulation_input.dat for species names. NOTE: currently not grouping multydentate species. Plots lattice and occupancy at last snapshot.
