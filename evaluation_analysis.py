import pandas as pd

# constraints_spread = {
#     'evs': [100, 100, 400, 1000, 100, 400, 1000, 200, 150, 150, 200],
#     'tps': [300, 10000, 10000, 10000, 50000, 50000,
#             50000, 4000, 4000, 10000, 10000],
#     'flexiblity': [50, 30, 25, 15,  10, 5, 2],
#     'energy': [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
# }
# xlsx_data = {
#     'Vehicles': [],
#     'Petitions': [],
#     'Flexiblity': [],
#     'Energy': [],
#     'Petitions Satisfied': [],
# }

# Constraints for dynamic EVs
constraints= {
    'secs': [1, 2, 4, 8],
    'energy': [0.5, 1.0, 2.0, 6.0],
    'tps': [300, 1000],
    'ev_factor': [1.0, 2.0]
}

xlsx_data = {
    'Vehicles': [],
    'Petitions': [],
    'Flexiblity': [],
    'Energy': [],
    'Petitions Satisfied': [],
    'Vehicle Factor': [],
    'SEC': []
}
if __name__ == '__main__':
    analysis_file = 'output/analysis_dynamic_ev/solution.csv'
    analysis_data = pd.read_csv(analysis_file, delimiter=';', lineterminator='\n')
    analysis_data = analysis_data.reset_index()
    for index, row in analysis_data.iterrows():
        path = row['File'].split('/')[4:]
        folder = path[0].split('_')
        file = path[1].split('_')
        xlsx_data['Vehicle Factor'].append(file[0])
        xlsx_data['Vehicles'].append(file[1])
        xlsx_data['Flexiblity'].append(15)
        xlsx_data['SEC'].append(folder[0])
        xlsx_data['Energy'].append(folder[2])
        xlsx_data['Petitions Satisfied'].append(row['Trips_Satisfied'])
        xlsx_data['Petitions'].append(file[3])

    for i in xlsx_data.keys():
        print(len(xlsx_data[i]))
    df = pd.DataFrame(data=xlsx_data, columns=('Vehicles','Vehicle Factor','SEC','Petitions','Petitions Satisfied','Flexiblity','Energy'))
    df.to_excel('./output/analysis_dynamic_ev/evaluation.xlsx')









# if __name__ == '__main__':
#     analysis_file = 'output/analysis_dynamic/solution.csv'
#     analysis_data = pd.read_csv(analysis_file, delimiter=';', lineterminator='\n')
#     analysis_data = analysis_data.reset_index()
#     json_data = {}
#     n_data_points = len(constraints['evs'])
#     for i in range(n_data_points):
#         file = str(constraints['evs'][i])+'_EV_'+str(constraints['tps'][i])+'_TPS.txt'
#         for flex in constraints['flexiblity']:
#             for energy in constraints['energy']:
#                 folder = str(flex)+'_FLEX_'+str(energy)+'_SYS_ENERGY'
#                 for index, row in analysis_data.iterrows():
#                     file_type = row['File'].split('/')[4:]
#                     if file_type[0] == folder and file_type[1] == file:
#                         xlsx_data['Vehicles'].append(constraints['evs'][i])
#                         xlsx_data['Petitions'].append(constraints['tps'][i])
#                         xlsx_data['Flexiblity'].append(flex)
#                         xlsx_data['Energy'].append(energy)
#                         xlsx_data['Petitions Satisfied'].append(row['Trips_Satisfied'])
#                         break
#
#     for i in xlsx_data.keys():
#         print(len(xlsx_data[i]))
#     df = pd.DataFrame(data=xlsx_data, columns=('Vehicles','Petitions','Petitions Satisfied','Flexiblity','Energy'))
#     df.to_excel('./output/evaluation.xlsx')





