import csv


class Fluor:
    def __init__(self, name, ex, emi):
        self.name = name
        self.ex = ex
        self.emi = emi
        self.fitting_cubes = []

    def add_fitting_cube(self, c):
        self.fitting_cubes.append(c)

    def __repr__(self):
        return f'{self.name}, {self.ex}, {self.emi}'


class WrongFileTypeError(Exception):
    pass


cubes_file = 'cubes.csv'
fluors_file = 'fluors.csv'

fluors = []

try:
    with open(cubes_file, newline='') as csvcubes, open(fluors_file, newline='') as csvfluors:
        if not cubes_file.endswith('.csv') or not fluors_file.endswith('.csv'):
            raise WrongFileTypeError
        fluor_reader = csv.DictReader(csvfluors, skipinitialspace=True)
        cube_reader = csv.DictReader(csvcubes, skipinitialspace=True)
        for fluor in fluor_reader:
            fl = Fluor(*fluor.values())
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

                if (exmin <= float(fluor['Excitation wavelength']) <= exmax
                        and float(fluor['Excitation wavelength']) < float(cube['Dichromatic mirror']) < float(
                            fluor['Emission wavelength'])
                        and (supmin <= float(fluor['Emission wavelength']) <= supmax or supmin <= float(
                            fluor['Emission wavelength']))):
                    fl.add_fitting_cube(cube)
            fluors.append(fl)
except OSError as error:
    print(error)
except WrongFileTypeError:
    print('Error: one of the input files is not a CSV file')
else:
    print('Fitting cubes:')
    print('---------------------------------------')
    for fluor in fluors:
        print(f'For {fluor.name} [{fluor.ex}, {fluor.emi}]:')
        for cube in fluor.fitting_cubes:
            print(' - {}, {}, {}, {}, {}, {}, {}'.format(*cube.values()))
        print('---------------------------------------')
