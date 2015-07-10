#halflifes are in seconds
#inhalation (Sv/Bq) 3 months age category
#inhalation (Sv/Bq) 1 year age category
#inhalation (Sv/Bq) 5 years age category
#inhalation (Sv/Bq) 10 years age category
#inhalation (Sv/Bq) 15 years age category
#inhalation (Sv/Bq) adult age category
#external dose cloud (Sv/s * Bq/m3) 5 years - adult age category (for 0-5 years mutiply with 1.5)
#external dose groundshine (Sv/s * Bq/m2) 5 years - adult age category (for 0-5 years mutiply with 1.5)

#breathing rates 3m, 1y, 5y, 10y, 15y and adults(> 17 years) in m3/day
breathing_rates = (2.86, 5.16, 8.72, 15.3, 20.1, 22.2)

d = {
#particulates
'Sb-122': {'halflife': 233280.0, 'inhalation': (8.3e-09, 5.7e-09, 2.8e-09, 1.8e-09, 1.3e-09, 1e-09), 'cloud': 2.02e-14, 'ground': 4.85e-16},
'Sb-124': {'halflife': 5201280.0, 'inhalation': (3.1e-08, 2.4e-08, 1.4e-08, 9.6e-09, 7.7e-09, 6.4e-09), 'cloud': 8.62e-14, 'ground': 1.7e-15},
'Sb-125': {'halflife': 87354720.0, 'inhalation': (2e-08, 1.6e-08, 1e-08, 6.8e-09, 5.8e-09, 4.8e-09), 'cloud': 1.87e-14, 'ground': 4.09e-16},
'Te-132': {'halflife': 281664.0, 'inhalation': (1.6e-08, 1.3e-08, 6.4e-09, 4e-09, 2.6e-09, 2e-09), 'cloud': 1.17e-13, 'ground': 2.47e-15},
'I-123': {'halflife': 47520.0, 'inhalation': (8.7e-10, 7.9e-10, 3.8e-10, 1.8e-10, 1.1e-10, 7.4e-11), 'cloud': 6.49e-15, 'ground': 1.53e-16},
'I-125': {'halflife': 5192640.0, 'inhalation': (2e-08, 2.3e-08, 1.5e-08, 1.1e-08, 7.2e-09, 5.1e-09), 'cloud': 3.73e-16, 'ground': 3.14e-17},
'I-129': {'halflife': 4.951152e+14, 'inhalation': (7.2e-08, 8.6e-08, 6.1e-08, 6.7e-08, 4.6e-08, 3.6e-08), 'cloud': 2.81e-16, 'ground': 1.95e-17},
'I-131': {'halflife': 694656.0, 'inhalation': (7.2e-08, 7.2e-08, 3.7e-08, 1.9e-08, 1.1e-08, 7.4e-09), 'cloud': 1.69e-14, 'ground': 3.64e-16},
#entry for gaseous iodine identical to I-131 entry
'I-131g': {'halflife': 694656.0, 'inhalation': (7.2e-08, 7.2e-08, 3.7e-08, 1.9e-08, 1.1e-08, 7.4e-09), 'cloud': 1.69e-14, 'ground': 3.64e-16},
'I-132': {'halflife': 8280.0, 'inhalation': (1.1e-09, 9.6e-10, 4.5e-10, 2.2e-10, 1.3e-10, 9.4e-11), 'cloud': 1.05e-13, 'ground': 2.2e-15},
'I-133': {'halflife': 74880.0, 'inhalation': (1.9e-08, 1.8e-08, 8.3e-09, 3.8e-09, 2.2e-09, 1.5e-09), 'cloud': 2.76e-14, 'ground': 6.17e-16},
'I-134': {'halflife': 3153.6, 'inhalation': (4.6e-10, 3.7e-10, 1.8e-10, 9.7e-11, 5.9e-11, 4.5e-11), 'cloud': 1.22e-13, 'ground': 2.53e-15},
'I-135': {'halflife': 23796.0, 'inhalation': (4.1e-09, 3.7e-09, 1.7e-09, 7.9e-10, 4.8e-10, 3.2e-10), 'cloud': 7.54e-14, 'ground': 1.47e-15},
'Cs-134': {'halflife': 64964160.0, 'inhalation': (1.1e-08, 7.3e-09, 5.2e-09, 5.3e-09, 6.3e-09, 6.6e-09), 'cloud': 7.06e-14, 'ground': 1.48e-15},
'Cs-135': {'halflife': 7.25328e+13, 'inhalation': (1.7e-09, 9.9e-10, 6.2e-10, 6.1e-10, 6.8e-10, 6.9e-10), 'cloud': 9.5e-18, 'ground': 2.69e-20},
'Cs-136': {'halflife': 1131840.0, 'inhalation': (7.3e-09, 5.2e-09, 2.9e-09, 2e-09, 1.4e-09, 1.2e-09), 'cloud': 9.94e-14, 'ground': 2.03e-15},
'Cs-137': {'halflife': 946080000.0, 'inhalation': (8.8e-09, 5.4e-09, 3.6e-09, 3.7e-09, 4.4e-09, 4.6e-09), 'cloud': 2.55e-14, 'ground': 5.51e-16},
'Ba-140': {'halflife': 1097280.0, 'inhalation': (2.7e-08, 2e-08, 1.1e-08, 7.6e-09, 6.2e-09, 5.1e-09), 'cloud': 8.07e-15, 'ground': 1.9e-16},
'La-140': {'halflife': 145152.0, 'inhalation': (8.8e-09, 6.3e-09, 3.1e-09, 2e-09, 1.3e-09, 1.1e-09), 'cloud': 1.11e-13, 'ground': 2.16e-15},
'Ce-141': {'halflife': 2808000.0, 'inhalation': (1.4e-08, 1.1e-08, 6.3e-09, 4.6e-09, 4.1e-09, 3.2e-09), 'cloud': 3.1e-15, 'ground': 6.93e-17},
'Ce-144': {'halflife': 24537600.0, 'inhalation': (1.9e-07, 1.6e-07, 8.8e-08, 5.5e-08, 4.1e-08, 3.6e-08), 'cloud': 3.42e-15, 'ground': 1.82e-16},
'Pm-147': {'halflife': 82624320.0, 'inhalation': (2.1e-08, 1.8e-08, 1.1e-08, 7e-09, 5.7e-09, 5e-09), 'cloud': 8.67e-18, 'ground': 2.8e-20},
'Eu-152': {'halflife': 419428800.0, 'inhalation': (1.1e-07, 1e-07, 7e-08, 4.9e-08, 4.3e-08, 4.2e-08), 'cloud': 5.28e-14, 'ground': 1.08e-15},
'Eu-154': {'halflife': 277516800.0, 'inhalation': (1.6e-07, 1.5e-07, 9.7e-08, 6.5e-08, 5.6e-08, 5.3e-08), 'cloud': 5.75e-14, 'ground': 1.17e-15},
'Hg-203': {'halflife': 4026240.0, 'inhalation': (1e-08, 7.9e-09, 4.7e-09, 3.4e-09, 3e-09, 2.4e-09), 'cloud': 1.04e-14, 'ground': 2.22e-16},
'U-234': {'halflife': 7.694784e+12, 'inhalation': (1.5e-05, 1.1e-05, 7e-06, 4.8e-06, 4.2e-06, 3.5e-06), 'cloud': 6.11e-18, 'ground': 5.86e-19},
'U-235': {'halflife': 2.2201344e+16, 'inhalation': (1.3e-05, 1e-05, 6.3e-06, 4.3e-06, 3.7e-06, 3.1e-06), 'cloud': 6.46e-15, 'ground': 1.4e-16},
'U-238': {'halflife': 1.4096592e+17, 'inhalation': (1.2e-05, 9.4e-06, 5.9e-06, 4e-06, 3.4e-06, 2.9e-06), 'cloud': 2.5e-18, 'ground': 4.23e-19},
'Np-237': {'halflife': 6.748704e+13, 'inhalation': (4.4e-05, 4e-05, 2.8e-05, 2.2e-05, 2.2e-05, 2.3e-05), 'cloud': 8.87e-16, 'ground': 2.52e-17},
'Np-239': {'halflife': 203904.0, 'inhalation': (5.9e-09, 4.2e-09, 2e-09, 1.4e-09, 1.2e-09, 9.3e-10), 'cloud': 6.95e-15, 'ground': 1.54e-16},
'Pu-238': {'halflife': 2765707200.0, 'inhalation': (7.8e-05, 7.4e-05, 5.6e-05, 4.4e-05, 4.3e-05, 4.6e-05), 'cloud': 3.5e-18, 'ground': 6.26e-19},
'Pu-239': {'halflife': 7.600176e+11, 'inhalation': (8e-05, 7.7e-05, 6e-05, 4.8e-05, 4.7e-05, 5e-05), 'cloud': 3.48e-18, 'ground': 2.84e-19},
'Pu-240': {'halflife': 2.0624544e+11, 'inhalation': (8e-05, 7.7e-05, 6e-05, 4.8e-05, 4.7e-05, 5e-05), 'cloud': 3.42e-18, 'ground': 6.01e-19},
'Pu-241': {'halflife': 454118400.0, 'inhalation': (9.1e-07, 9.7e-07, 9.2e-07, 8.3e-07, 8.6e-07, 9e-07), 'cloud': 6.33e-20, 'ground': 1.72e-21},
'Pu-242': {'halflife': 1.1857536e+13, 'inhalation': (7.6e-05, 7.3e-05, 5.7e-05, 4.5e-05, 4.5e-05, 4.8e-05), 'cloud': 2.9e-18, 'ground': 4.98e-19},
'Pu-244': {'halflife': 2.6048736e+15, 'inhalation': (7.4e-05, 7.2e-05, 5.6e-05, 4.5e-05, 4.4e-05, 4.7e-05), 'cloud': 2.08e-18, 'ground': 4.16e-19},
'Am-241': {'halflife': 13623552000.0, 'inhalation': (7.3e-05, 6.9e-05, 5.1e-05, 4e-05, 4e-05, 4.2e-05), 'cloud': 6.74e-16, 'ground': 2.33e-17},
'Am-243': {'halflife': 2.3273568e+11, 'inhalation': (7.2e-05, 6.8e-05, 5e-05, 4e-05, 4e-05, 4.1e-05), 'cloud': 1.85e-15, 'ground': 4.79e-17},
'Cm-242': {'halflife': 14083200.0, 'inhalation': (2.2e-05, 1.8e-05, 1.1e-05, 7.3e-06, 6.4e-06, 5.2e-06), 'cloud': 4.02e-18, 'ground': 7.02e-19},
'Cm-244': {'halflife': 570801600.0, 'inhalation': (6.2e-05, 5.7e-05, 3.7e-05, 2.7e-05, 2.6e-05, 2.7e-05), 'cloud': 3.4e-18, 'ground': 6.44e-19},
'Cm-247': {'halflife': 4.919616e+14, 'inhalation': (6.7e-05, 6.3e-05, 4.7e-05, 3.7e-05, 3.7e-05, 3.9e-05), 'cloud': 1.38e-14, 'ground': 2.99e-16},
#noble gasses
'Ar-37': {'halflife': 3024000.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 4.75e-20, 'ground': -999},
'Ar-39': {'halflife': 8483184000.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 1.27e-16, 'ground': -999},
'Ar-41': {'halflife': 6588.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 6.13e-14, 'ground': -999},
'Kr-74': {'halflife': 690.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 5.21e-14, 'ground': -999},
'Kr-76': {'halflife': 53280.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 1.85e-14, 'ground': -999},
'Kr-77': {'halflife': 4482.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 4.51e-14, 'ground': -999},
'Kr-79': {'halflife': 126144.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 1.12e-14, 'ground': -999},
'Kr-81': {'halflife': 6.62256e+12, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 2.43e-16, 'ground': -999},
'Kr-83m': {'halflife': 6588.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 2.43e-18, 'ground': -999},
'Kr-85': {'halflife': 337435200.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 2.55e-16, 'ground': -999},
'Kr-85m': {'halflife': 16128.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 6.83e-15, 'ground': -999},
'Kr-87': {'halflife': 4572.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 3.94e-14, 'ground': -999},
'Kr-88': {'halflife': 10224.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 9.72e-14, 'ground': -999},
'Xe-120': {'halflife': 2400.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 1.74e-14, 'ground': -999},
'Xe-121': {'halflife': 2406.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 8.68e-14, 'ground': -999},
'Xe-122': {'halflife': 72360.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 2.2e-15, 'ground': -999},
'Xe-123': {'halflife': 7488.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 2.78e-14, 'ground': -999},
'Xe-125': {'halflife': 61200.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 1.08e-14, 'ground': -999},
'Xe-127': {'halflife': 3144960.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 1.12e-14, 'ground': -999},
'Xe-129m': {'halflife': 691200.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 9.38e-16, 'ground': -999},
'Xe-131m': {'halflife': 1028160.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 3.7e-16, 'ground': -999},
'Xe-133m': {'halflife': 189216.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 1.27e-15, 'ground': -999},
'Xe-133': {'halflife': 452736.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 1.39e-15, 'ground': -999},
'Xe-135m': {'halflife': 918.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 1.85e-14, 'ground': -999},
'Xe-135': {'halflife': 32760.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 1.11e-14, 'ground': -999},
'Xe-138': {'halflife': 852.0, 'inhalation': (-999, -999, -999, -999, -999, -999), 'cloud': 5.44e-14, 'ground': -999}
}