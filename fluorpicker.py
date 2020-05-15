import csv

try:
    csvfluors = open('fluors.csv', newline='')
except OSError as error:
    print(error)
else:
    fluor_reader = csv.DictReader(csvfluors, skipinitialspace=True)
    fitting_cubes = []

    for fluor in fluor_reader:
        with open('cubes.csv', newline='') as csvcubes:
            cube_reader = csv.DictReader(csvcubes, skipinitialspace=True)
            for cube in cube_reader:
                cube_exc_range = cube['Excitation range values']
                cube_sup_range = cube['Suppression range values']

                exmin, exmax = 0, 0
                if cube_exc_range.count('/'):
                    expeak, exbandwidth = cube_exc_range.split('/')
                    exmin, exmax = int(expeak) - int(exbandwidth) / 2, int(expeak) + int(exbandwidth) / 2
                elif cube_exc_range.count('-'):
                    exmin, exmax = cube_exc_range.split('-')
                    exmin, exmax = float(exmin), float(exmax)

                supmin, supmax = 0, 0
                if cube['Suppression filter mode'] == 'bp':
                    suppeak, supbandwidth = cube_sup_range.split('/')
                    supmin, supmax = int(suppeak) - int(supbandwidth) / 2, int(suppeak) + int(supbandwidth) / 2
                elif cube['Suppression filter mode'] == 'lp':
                    supmin = int(cube_sup_range)

                # if

                if (exmin <= float(fluor['Excitation wavelength']) <= exmax
                        and float(fluor['Excitation wavelength']) < float(cube['Dichromatic mirror']) < float(
                            fluor['Emission wavelength'])
                        and (supmin <= float(fluor['Emission wavelength']) <= supmax or supmin <= float(
                            fluor['Emission wavelength']))):
                    fitting_cubes.append(cube)

    print('Fitting cubes:')
    for cube in fitting_cubes:
        print('{}, {}, {}, {}, {}, {}, {}'.format(*cube.values()))
