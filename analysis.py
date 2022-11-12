import pandas as pd
from xlsxwriter import Workbook

if __name__ == '__main__':
    file = './constraint_analysis/Vehicle Factor_analysis.xlsx'
    xlsx = pd.ExcelFile(file)
    sheet_names = xlsx.sheet_names[1:]
    for sheet in sheet_names:
        data = pd.read_excel(file, sheet_name=sheet)
        # data = pd.read_excel(file, sheet_name='Start')
        break_down = {
            'Petitions': 0,
            'Petitions_satisfied': 0,
            'Petition_satisfied_percent': 0,
            'Ride_share_cars': 0,
            'Individual_cars': 0,
            'Taxi_cars': 0,
            'Car_reduction_to_indivi_trips': 0,
            'Car_reduction_to_taxi_trips': 0,
            'Ride_share_distance': 0,
            'Taxi_distance': 0,
            'Individual_distance': 0,
            'Distance_reduction_to_taxi_trips': 0
        }
        petitons = data['Petitions'][len(data['Petitions'])-1]
        break_down['Petitions'] = petitons
        petitons_satisfied = data['Petitions Satisfied'][len(data['Petitions Satisfied'])-1]
        break_down['Petitions_satisfied'] = petitons_satisfied
        ride_share_distance = data['Ride-share Distance'][len(data['Ride-share Distance'])-1]
        break_down['Ride_share_distance'] = ride_share_distance
        individual_trip_distance = data['Individual Trip Distance'][len(data['Individual Trip Distance'])-1]
        break_down['Individual_distance'] = individual_trip_distance
        taxi_trip_distance = data['Sequential Distance'][len(data['Sequential Distance'])-1]
        break_down['Taxi_distance'] = taxi_trip_distance
        individual_cars = data['Individual Trip Cars'][len(data['Individual Trip Cars'])-1]
        break_down['Individual_cars'] = individual_cars
        ride_share_cars = data['Ride-share Trip Cars'][len(data['Ride-share Trip Cars'])-1]
        break_down['Ride_share_cars'] = ride_share_cars
        taxi_cars = data['Sequential Trip Cars'][len(data['Sequential Trip Cars'])-1]
        break_down['Taxi_cars'] = taxi_cars
        break_down['Petition_satisfied_percent'] = petitons_satisfied/petitons*100
        break_down['Car_reduction_to_indivi_trips'] = 100 - (ride_share_cars/individual_cars*100)
        break_down['Car_reduction_to_taxi_trips'] = 100 - (ride_share_cars/taxi_cars*100)
        break_down['Distance_reduction_to_taxi_trips'] = 100 - (ride_share_distance/taxi_trip_distance*100)
        df = pd.DataFrame(data=break_down, index=[0])
        df = (df.T)
        df.to_excel('./evaluation_analysis/'+sheet+'.xlsx')

