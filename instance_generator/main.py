import sys
import random as r
import modal
import distributions
import codecs
import tkinter as tk
from tkinter import filedialog
import seaborn
import pandas as pd
import datetime
import math
import os
import shutil

# Constraints for spread mode
# constraints = {
#     'evs': [100, 100, 400, 1000, 100, 400, 1000, 200, 150, 150, 200],
#     'tps': [300, 10000, 10000, 10000, 50000, 50000,
#             50000, 4000, 4000, 10000, 10000],
#     'flexiblity': [50, 30, 25, 15,  10, 5, 2],
#     'energy': [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
# }

# Constraints for dynamic EVs
# constraints= {
#     'secs': [1, 2, 4, 8],
#     'energy': [0.5, 1.0, 2.0, 6.0],
#     'tps': [300, 1000],
#     'ev_factor': [1.0, 2.0]
# }
constraints = {
    secs: [1, 4, 16],
    tps: [300, 1000, 10000],
    evs: [1.0, 1.5, 2.0],
    sys_energy: [0.5, 1.0, 2.0, 4.0, 5.0, 6.0],
    flexiblity: [2, 10, 25, 50],
    dispatch: ['start', 'spread']
}
raw_petitions = []

def writeToFile(time_horizon, grid_size, secs, evs, passengers, petitions, file_type, file_num, energy_required,
                flexiblity, sys_energy):
    # outfile ="./instances/"+file_type+"/"+str(file_num)+".txt"
    # output_folder = './instances/evaluation_spread_mode/'+str(flexiblity)+'_FLEX_'+str(sys_energy)+'_SYS_ENERGY/'
    output_folder = './instances/evaluation_dynamic_ev/'+str(len(secs))+'_SEC_'+str(sys_energy)+'_ENERGY/'
    outfile = output_folder + str(constraints['ev_factor'][file_num])+'_'+str(len(evs))+\
              "_EV_"+str(len(petitions))+"_TPS.txt"
    outstream = codecs.open(outfile, "w", encoding="utf-8")
    outstream.write(str(grid_size)+" "+str(grid_size)+" "+str(time_horizon)+"\n")
    outstream.write(str(len(secs))+"\n")
    energy_produced = 0
    for sec in secs:
        sec_str = str(sec.sec_id)+" "+str(sec.x_start)+" "+str(sec.y_start)+"\n"
        energy_produced += sec.total_energy
        outstream.write(sec_str)
    # outstream.write(str(energy_produced[0])+"\n")
    outstream.write(str(len(evs))+"\n")
    for ev in evs:
        ev_str = str(ev.ev_id)+" "+str(ev.sec_id)+" "+\
                 str(ev.release_time)+" "+str(ev.battery_capacity)+" "+\
                 str(ev.num_passengers)+"\n"+str(0)+"\n"
        outstream.write(ev_str)

    # outstream.write(str(len(passengers))+"\n")
    # for per in passengers:
    #     per_str = str(per.p_id)+" "+str(per.sec_id)+"\n"
    #     outstream.write(per_str)

    outstream.write(str(len(petitions))+"\n")
    for petition in petitions:
        sec_id = 0
        for per in passengers:
            if per.p_id == petition.passenger_id:
                sec_id = per.sec_id
        allocation_status = -1
        p_str = str(petition.petition_id)+" "+str(sec_id)+" "+str(allocation_status)+"\n"+str(int(petition.time))+" "+\
                str(petition.pickup_x)+" "+str(petition.pickup_y)+" "+ \
                str(petition.drop_x) + " " +str(petition.drop_y)+" "+str(petition.early_start)+" "+ \
                str(petition.late_start) + " " +str(petition.early_finish)+" "+str(petition.late_finish)+"\n"
        outstream.write(p_str)


def calculateManhattanDistance(pickup_x, pickup_y, drop_x, drop_y):
    return (abs(pickup_x - drop_x) + abs(pickup_y - drop_y))


def assignRealWorldConstraints(time_horizon, grid_size, num_sec, num_ev,
                      trip_rate, num_passengers, file_type,
                      file_num, sys_energy, flexiblity, block_size, distances):
    print('Writing in '+str(num_sec)+'_SEC_'+str(sys_energy)+'_ENERGY')
    print(str(constraints['ev_factor'][file_num])+"_EV_"+\
              str(num_passengers)+"_TPS.txt")
    secs = []
    evs = []
    passengers = []
    petitions = []
    total_ev = 0
    total_petitions = num_passengers
    time_per_block = 1
    energy_required = 0
    pick_up_x, pick_up_y, drop_x, drop_y = 0, 0, 0, 0
    time = 0
    for i in range(num_passengers):
        p_id = i
        sec_id = r.randint(0, num_sec-1)
        petition_id = i+1
        time =  int(trip_rate[i])
        pick_up = r.randint(0, (grid_size * grid_size) - 1)
        pickup_x = pick_up // grid_size
        pickup_y = pick_up % grid_size
        distance = int(distances[i])
        tmp_x =  r.randint(0, distance)
        drop_x =  pickup_x + tmp_x
        if drop_x >= grid_size:
            drop_x = pickup_x - tmp_x
        tmp_y =  r.randint(0, (distance-tmp_x))
        drop_y = pickup_y + tmp_y
        if drop_y > grid_size:
            drop_y = pickup_y - tmp_y
        travel_time = distance * time_per_block
        energy_required += travel_time
        early_start = time + int((flexiblity/100) * trip_rate[num_passengers-1])
        early_finish = early_start + travel_time
        late_start = early_start + int((flexiblity/100) * trip_rate[num_passengers-1])
        late_finish = late_start + travel_time
        if late_finish > time_horizon:
            time_horizon = late_finish
        passengers.append(modal.Passenger(p_id, sec_id))
        petitions.append(modal.Trip_petition(petition_id, p_id, time,
                                             pickup_x, pickup_y, drop_x,
                                             drop_y, early_start,
                                             early_finish, late_start,
                                             late_finish, travel_time))
    energy_gen_time = time
    for i in range(num_sec):
        sec_id = i
        x_start = r.randint(0, grid_size-1)
        y_start = r.randint(0, grid_size-1)
        x_end = x_start
        y_end = y_start
        charge = 0
        charge_generation = r.randint(1,3)
        energy_dis = []
        if charge_generation == 1:
            energy_dis = distributions.generateWeibullDis(energy_gen_time, sys_energy, energy_required, num_sec)
        elif charge_generation == 2:
            energy_dis = distributions.generateNormalDis(energy_gen_time, sys_energy, energy_required, num_sec)
        else:
            energy_dis = distributions.generatePoissonDis(energy_gen_time, sys_energy, energy_required, num_sec)
        total_energy_produced = 0
        for item in energy_dis:
            total_energy_produced += item
        secs.append(modal.Sec(sec_id, charge_generation, x_start, y_start,
                              x_end, y_end, charge, total_energy_produced))
        for j in range(num_ev[i]):
            battery_capacity = grid_size
            ev_id = total_ev
            capacity = 6
            # Energy requirement for trip petitions is calculated using the metric
            charge_per_block = 1
            # Computing release time
            total_energy = 0
            is_released = False
            for i in range(len(energy_dis)):
                if energy_dis[i] != -1:
                    total_energy += energy_dis[i]
                    energy_dis[i] = -1
                if total_energy > battery_capacity:
                    release_time = i+1
                    is_released = True
                    break

            if is_released is False:
                release_time = -1
            evs.append(modal.Ev(sec_id, battery_capacity, ev_id,
                                capacity, charge_per_block, release_time))
            total_ev += 1
    writeToFile(time_horizon, grid_size, secs, evs, passengers, petitions, file_type, file_num, energy_required,
                flexiblity, sys_energy)


def parseRealData(mode):
    valid_file = False
    data = []
    ny_zone_data = {}
    with open("taxi_zones_ny.txt") as f:
        for line in f:
            (k, v) = line.split(':')
            ny_zone_data[int(k)] = v
    # print(ny_zone_data)
    # YYYY/DD/MM Time is the date-time format
    # Reading raw data from file input
    while not valid_file:
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(initialdir="./real_world_dataset", title="Input Data set",
                                              filetypes=[("Excel files","*.xlsx"), ("CSV files", "*.csv")])
        file = filename.split("/")[-1].split(".")[0]
        file_type = filename.split("/")[-1].split(".")[1]
        if file_type == "csv":
            data = pd.read_csv(filename, delimiter=';', lineterminator='\n')
            valid_file = True
            break
        else:
            print("Invalid File Type. Supported file type is .csv ")
    # print(data['lpep_pickup_datetime'])
    keys = ['VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'trip_distance']
    data = data.filter(items=keys)
    data['pickup'] = pd.to_datetime(data['lpep_pickup_datetime'], format='%m/%d/%Y   %H:%M:%S %p')
    data = data.drop(['lpep_pickup_datetime'], axis=1)
    data = data.set_index(pd.DatetimeIndex(data['pickup']), drop=True)
    # data = data.drop(data['pickup'], axis=1)
    # Dropping rows with duplicate index
    data = data[~data.index.duplicated()]
    data = data.dropna()
    # print(data)
    index_date = pd.date_range('2018-01-01', periods=len(data.index), freq="1S")
    parsed_data = pd.DataFrame(data, index=index_date)
    parsed_data = parsed_data.dropna()
    # print(parsed_data)
    # Creating Real-world instance constraints
    # n_hours = float(input("Simulation time in hours: "))
    # print("Extracting trips from ", start_time.time()," to ", end_time.time())
    # raw_petitions = data.between_time(str(start_time.time()), str(end_time.time()))

    n_hours = 3
    start_time = datetime.datetime.strptime(input('specify time in HHMM format: '), "%H%M")
    end_time = start_time + datetime.timedelta(hours = n_hours)
    block_size = 1
    if mode == 'Spread':
        for energy in constraints['energy']:
            sys_energy = energy
            for flex in constraints['flexiblity']:
                for inst in range(len(constraints['evs'])):
                    # Forming grid
                    grid_size = 100
                    raw_petitions = parsed_data.head(constraints['tps'][inst])
                    raw_petitions = raw_petitions.reset_index(drop=False)
                    # Forming SECs
                    num_sec = 10
                    ev_rate = constraints['evs'][inst]/num_sec
                    num_passengers = len(raw_petitions.index)
                    evs = {}
                    for i in range(num_sec):
                        evs[i] = int(ev_rate)

                    trip_rate = []
                    distances = []
                    for i, row in raw_petitions.iterrows():
                        diff = datetime.datetime.combine(datetime.date.today(), row['pickup'].time()) - \
                               datetime.datetime.combine(datetime.date.today(), start_time.time())
                        trip_rate.append(diff.total_seconds() - 3600)
                        if row['trip_distance'] == 0:
                            distances.append(1)
                        else:
                            distances.append(math.ceil(row['trip_distance']))
                    time_horizon = int(trip_rate[num_passengers-1])
                    assignRealWorldConstraints(time_horizon, grid_size, num_sec, evs, trip_rate,
                                               num_passengers, file_type, inst, sys_energy, flex, block_size, distances)
    else:
        for s in constraints['secs']:
            for energy in constraints['energy']:
                sys_energy = energy
                for inst in range(len(constraints['ev_factor'])):
                    for tp in constraints['tps']:
                        grid_size = 100
                        raw_petitions = parsed_data.head(tp)
                        raw_petitions = raw_petitions.reset_index(drop=False)
                        # Forming SECs
                        num_sec = s
                        num_passengers = len(raw_petitions.index)
                        total_distance = 0
                        trip_rate = []
                        distances = []
                        for i, row in raw_petitions.iterrows():
                            diff = datetime.datetime.combine(datetime.date.today(), row['pickup'].time()) - \
                                   datetime.datetime.combine(datetime.date.today(), start_time.time())
                            trip_rate.append(diff.total_seconds() - 3600)
                            if row['trip_distance'] == 0:
                                distances.append(1)
                                total_distance += 1
                            else:
                                distances.append(math.ceil(row['trip_distance']))
                                total_distance += math.ceil(row['trip_distance'])
                        time_horizon = int(trip_rate[num_passengers-1])
                        total_charge_rate = total_distance * (inst+1)
                        battery_capacity = grid_size
                        num_ev = int(total_charge_rate/battery_capacity)
                        ev_rate = int(num_ev/num_sec)
                        evs = {}
                        for i in range(num_sec):
                            evs[i] = ev_rate
                        flex = 15
                        assignRealWorldConstraints(time_horizon, grid_size, num_sec, evs, trip_rate,
                                                   num_passengers, file_type, inst, sys_energy, flex, block_size, distances)








def assignConstraints(time_horizon, grid_size, num_sec, num_ev,
                      trip_rate, num_passengers, file_type,
                      file_num, sys_energy, flexiblity):
    print("Generating file "+str(file_num)+".txt")
    secs = []
    evs = []
    passengers = []
    petitions = []
    total_ev = 0
    total_petitions = num_passengers
    track_time = trip_rate
    time_per_block = 0.5
    energy_required = 0
    pick_up_x, pick_up_y, drop_x, drop_y = 0, 0, 0, 0
    time_horizon = int(time_horizon)
    time = 0
    for i in range(num_passengers):
        p_id = i
        sec_id = r.randint(0, num_sec-1)
        petition_id = i+1
        time += track_time
        pick_up = r.randint(0, (grid_size * grid_size) - 1)
        drop = r.randint(0, (grid_size * grid_size) - 1)
        pickup_x = pick_up // grid_size
        pickup_y = pick_up % grid_size
        drop_x = drop // grid_size
        drop_y = drop % grid_size
        while pick_up_x == drop_x and drop_y == pick_up_y:
            pick_up = r.randint(0, (grid_size*grid_size)-1)
            drop = r.randint(0, (grid_size*grid_size)-1)
            pickup_x = pick_up // grid_size
            pickup_y = pick_up % grid_size
            drop_x = drop // grid_size
            drop_y = drop % grid_size
        travel_time = int(calculateManhattanDistance(pickup_x, pickup_y, drop_x, drop_y) * time_per_block)
        energy_required += travel_time
        early_start = time + flexiblity
        early_finish = early_start + travel_time
        late_start = early_start + trip_rate
        late_finish = late_start + travel_time
        if late_finish > time_horizon:
            time_horizon = late_finish
        passengers.append(modal.Passenger(p_id, sec_id))
        petitions.append(modal.Trip_petition(petition_id, p_id, time,
                                             pickup_x, pickup_y, drop_x,
                                             drop_y, early_start,
                                             early_finish, late_start,
                                             late_finish, travel_time))
        track_time = time

    time_horizon = int(time_horizon)
    for i in range(track_time, time_horizon, trip_rate):
        petition_id = len(petitions)+1
        p_id = r.randint(0, num_passengers-1)
        last_petition = None
        for i in range(len(petitions)):
            if petitions[i].passenger_id == p_id:
                last_petition = petitions[i]
        time = last_petition.time + trip_rate
        pickup_x = last_petition.drop_x
        pickup_y = last_petition.drop_y
        drop = r.randint(0, (grid_size * grid_size) - 1)
        drop_x = drop // grid_size
        drop_y = drop % grid_size
        while pick_up_x == drop_x and drop_y == pick_up_y:
            pickup_x = last_petition.drop_x
            pickup_y = last_petition.drop_y
            drop = r.randint(0, (grid_size * grid_size) - 1)
            drop_x = drop // grid_size
            drop_y = drop % grid_size
        travel_time = int(calculateManhattanDistance(pickup_x, pickup_y, drop_x, drop_y) * time_per_block)
        energy_required += travel_time
        early_start = time
        early_finish = early_start + travel_time
        late_start = early_start + flexiblity
        late_finish = late_start + travel_time
        if late_finish > time_horizon:
            time_horizon = late_finish
        petitions.append(modal.Trip_petition(petition_id, p_id, time,
                                             pickup_x, pickup_y, drop_x,
                                             drop_y, early_start,
                                             early_finish, late_start,
                                             late_finish, travel_time))
    for i in range(num_sec):
        sec_id = i
        x_start = r.randint(0, grid_size-1)
        y_start = r.randint(0, grid_size-1)
        x_end = x_start
        y_end = y_start
        charge = 0
        charge_generation = r.randint(1,3)
        energy_dis = []
        if charge_generation == 1:
            energy_dis = distributions.generateWeibullDis(time_horizon, sys_energy, energy_required, num_sec)
        elif charge_generation == 2:
            energy_dis = distributions.generateNormalDis(time_horizon, sys_energy, energy_required, num_sec)
        else:
            energy_dis = distributions.generatePoissonDis(time_horizon, sys_energy, energy_required, num_sec)
        total_energy_produced = 0
        for item in energy_dis:
            total_energy_produced += item
        secs.append(modal.Sec(sec_id, charge_generation, x_start, y_start,
                              x_end, y_end, charge, total_energy_produced))
        for j in range(num_ev[i]):
            battery_capacity = int(grid_size/2)
            ev_id = total_ev
            capacity = 6
            # Energy requirement for trip petitions is calculated using the metric
            charge_per_block = 1
            # Computing release time
            total_energy = 0
            is_released = False
            for i in range(len(energy_dis)):
                if energy_dis[i] != -1:
                    total_energy += energy_dis[i]
                    energy_dis[i] = -1
                if total_energy > battery_capacity:
                    release_time = i+1
                    is_released = True
                    break

            if is_released is False:
                release_time = -1
            evs.append(modal.Ev(sec_id, battery_capacity, ev_id,
                                capacity, charge_per_block, release_time))
            total_ev += 1
    writeToFile(time_horizon, grid_size, secs, evs, passengers, petitions, file_type, file_num, energy_required)


def generateLargeDataset(file_type, num_inst, sys_energy, flexiblity):
    print("Generating Large dataset")
    for file_num in range(1, num_inst+1):
        time_horizon = r.randint(50, 100)
        grid_size = 100
        num_sec = r.randint(4, 6)
        evs = {}
        for i in range(num_sec):
            evs[i] = r.randint(5, 8)
        trip_rate = int((flexiblity/100) * time_horizon)
        if trip_rate == 0:
            trip_rate = 1
        num_passengers = r.randint(10, 15)
        flexibility = int((flexiblity / 100) * time_horizon)
        assignConstraints(time_horizon, grid_size, num_sec, evs, trip_rate,
                          num_passengers, file_type, file_num, sys_energy, flexiblity)


def generateMediumDataset(file_type, num_inst, sys_energy, flexiblity):
    print("Generating Medium dataset")
    for file_num in range(1, num_inst+1):
        time_horizon = r.randint(50, 100)
        grid_size = 100
        num_sec = r.randint(2, 4)
        evs = {}
        for i in range(num_sec):
            evs[i] = r.randint(5, 10)
        trip_rate = int((flexiblity/100) * time_horizon)
        if trip_rate == 0:
            trip_rate = 1
        num_passengers = r.randint(5, 10)
        flexibility = int((flexiblity / 100) * time_horizon)
        assignConstraints(time_horizon, grid_size, num_sec, evs, trip_rate,
                          num_passengers, file_type, file_num, sys_energy, flexiblity)


def generateSmallDataset(file_type, num_inst, sys_energy, flexiblity):
    print("Generating small dataset")
    for file_num in range(1, num_inst+1):
        time_horizon = r.randint(50,100)
        grid_size = 100
        num_sec = 2
        evs = {}
        for i in range(num_sec):
            evs[i] = r.randint(5, 10)
        trip_rate = int((flexiblity/100) * time_horizon)
        if trip_rate == 0:
            trip_rate = 1
        num_passengers = r.randint(3, 5)
        flexibility = int((flexiblity / 100) * time_horizon)
        assignConstraints(time_horizon, grid_size, num_sec, evs, trip_rate,
                          num_passengers, file_type, file_num, sys_energy, flexiblity)


def main(file_type, num_inst, sys_energy, flexiblity):
    if file_type == 'small':
        generateSmallDataset(file_type, num_inst, sys_energy, flexiblity)
    elif file_type == 'medium':
        generateMediumDataset(file_type, num_inst, sys_energy, flexiblity)
    elif file_type == 'large':
        generateLargeDataset(file_type, num_inst, sys_energy, flexiblity)
    elif file_type == 'v_large':
        generateVLargeDataset(file_type, num_inst, sys_energy, flexiblity)
    else:
        mode = ['start', 'spread']

        parseRealData(mode)


if __name__ == '__main__':
    # types = ['small', 'medium', 'large']
    types = ['real_world']
    num_inst = 5
    sys_energy = 2.0
    flexiblity =  10
    for file_type in types:
        main(file_type, num_inst, sys_energy, flexiblity)
