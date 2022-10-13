import pandas as pd
import numpy as np

xlsx_data = {
    'Vehicles': [],
    'Petitions': [],
    'Flexiblity': [],
    'Energy': [],
    'Petitions Satisfied': [],
    'Vehicle Factor': [],
    'SEC': [],
    'Mode': [],
    'Individual Trip Distance': [],
    'Ride-share Distance': []
}

change_params = {
    'Mode': ['START', 'SPREAD'],
    'Vehicle Factor': ['1.0', '1.5', '2.0'],
    'SEC': ['1', '4', '16'],
    'Petitions': ['300', '1000', '10000'],
    'Flexiblity': ['2', '10', '25', '50'],
    'Energy': ['0.5', '1.0', '2.0', '4.0', '5.0', '6.0'],
}

# Filter data based on a specific value
def filter_data(value, parsed_data):
    # Here we store the values that are going to be changed while keeping one of the params constant
    filename = './constraint_analysis/'+value+'_analysis.xlsx'
    # These are the values we are going to keep constant as we change values from 'change_params'
    column_names = ('Mode', 'Vehicle Factor', 'SEC', 'Petitions',
                    'Flexiblity', 'Energy')
    index = column_names.index(value)
    column_names = column_names[:index] + column_names[index+1:]

    # Filtration by iterating over the change_params
    data = pd.DataFrame()
    for param_one in change_params[column_names[0]]:
        for param_two in change_params[column_names[1]]:
            for param_three in change_params[column_names[2]]:
                for param_four in change_params[column_names[3]]:
                    for param_five in change_params[column_names[4]]:
                        data = pd.concat([data, parsed_data[(parsed_data[column_names[0]] == param_one) &
                                                        (parsed_data[column_names[1]] == param_two) &
                                                        (parsed_data[column_names[2]] == param_three) &
                                                        (parsed_data[column_names[3]] == param_four) &
                                                       (parsed_data[column_names[4]] == param_five)]], join='outer')
    data.to_excel(filename, index=False)


if __name__ == '__main__':
    analysis_file = 'output/solution.csv'

    # Reading the Evaluation file into a pandas frame
    analysis_data = pd.read_csv(analysis_file, delimiter=';', lineterminator='\n')
    analysis_data = analysis_data.reset_index()

    # We are extracting the params we are interested from the evaluation file and preparing them for filtration
    for index, row in analysis_data.iterrows():
        path = row['File'].split('/')[3:]
        analysis_file = pd.read_excel('./output_analysis/'+path[0]+'.xlsx')
        analysis_file.rename(columns={'Individual Coverage': 'Ride-share Distances', 'Ride-share Distance':'Individual Coverages'}, inplace=True)

        individual_distance = 0
        ride_share_distance = 0
        for index, dist in analysis_file.iterrows():
            individual_distance += float(dist['Individual Coverages'])
            ride_share_distance += float(dist['Ride-share Distances'])
        analysis_file.to_excel('./output_analysis/'+path[0] + '.xlsx')
        file = path[0].split('_')
        xlsx_data['Mode'].append(file[0])
        xlsx_data['Vehicles'].append(file[7])
        xlsx_data['Flexiblity'].append(file[9])
        xlsx_data['SEC'].append(file[1])
        xlsx_data['Energy'].append(file[3])
        xlsx_data['Petitions Satisfied'].append(row['Trips_Satisfied'])
        xlsx_data['Petitions'].append(file[11])
        xlsx_data['Vehicle Factor'].append(file[5])
        xlsx_data['Individual Trip Distance'].append(individual_distance)
        xlsx_data['Ride-share Distance'].append(ride_share_distance)


    # After extracting the data we convert it back into a pandas dataframe to start filtration based on our change params and change_against keys
    parsed_data = pd.DataFrame(data=xlsx_data, columns=('Mode', 'Vehicles','Vehicle Factor','SEC','Petitions',
                                                        'Petitions Satisfied','Flexiblity','Energy',
                                                        'Ride-share Distance', 'Individual Trip Distance'))

    # These are the values we are going to keep constant as we change values from 'change_params'
    column_names = ('Mode', 'Vehicle Factor', 'SEC', 'Petitions',
                    'Flexiblity', 'Energy')
    # Values that are remain constant while we change other params
    for column in column_names:
        filter_data(column, parsed_data)





