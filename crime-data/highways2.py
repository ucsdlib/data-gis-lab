import numpy as np
import pandas as pd
import os
import argparse
import re
ap = argparse.ArgumentParser()
ap.add_argument("--excel_file", required = True)
ap.add_argument("--new_name", required = True)
args = vars(ap.parse_args())
file = args['excel_file']
to_save = args['new_name']
data = pd.read_csv(file)
#if you figure out all state routes, can unhighlight the elif statemetns and remove the else statements for state routes
#so that not all random numbers are included as well
#add more numbers for the state list if possible
state = [125,163,52,54,56,94,905]
interstate = [5,8,15,805]
names = []
crosses = []
names_and_crosses = []
#need a try catch if block for cases with nan, messes up .isidigit() check
for i in range(0, len(data)):
    name = ""
    try:
        if(data["address_road_primary"][i].isdigit()):
            if(int(data["address_road_primary"][i]) in interstate):
                name = "INTERSTATE " + str(int(data["address_road_primary"][i]))
            #elif(int(data["address_road_primary"][i]) in state):
            #    name = "STATE ROUTE " + str(int(data["address_road_primary"][i]))
            else:
                name = "STATE ROUTE " + str(int(data["address_road_primary"][i]))
            if(data["address_sfx_primary"][i] is np.nan):
                if(data["address_dir_primary"][i] is not np.nan):
                    name = name + " " + data["address_dir_primary"][i]
            elif(data["address_sfx_primary"][i] is not np.nan):
                name = name + " " + data["address_sfx_primary"][i]
            else:
                print("name error in digit block primary for row" + str(i))
        else:
            name = data["address_road_primary"][i]
            if(data["address_sfx_primary"][i] is np.nan):
                pass
            elif(data["address_sfx_primary"][i] is not np.nan):
                name = name + " " + data["address_sfx_primary"][i]
            else:
                print("name error in non-digit block primary for row" + str(i))
    except AttributeError as error:
        name = ""
    names.append(name)
for i in range(0, len(data)):
    cross = ""
    try:
        if(data["address_road_intersecting"][i].isdigit()):
            if(int(data["address_road_intersecting"][i]) in interstate):
                cross = "INTERSTATE " + str(int(data["address_road_intersecting"][i]))
            #elif(int(data["address_road_primary"][i]) in state):
            #    name = "STATE ROUTE " + str(int(data["address_road_primary"][i]))
            else:
                cross = "STATE ROUTE " + str(int(data["address_road_intersecting"][i]))
            if(data["address_sfx_primary"][i] is np.nan):
                if(data["address_dir_primary"][i] is not np.nan):
                    cross = cross + " " + data["address_dir_primary"][i]
            elif(data["address_sfx_primary"][i] is not np.nan):
                cross = cross + " " + data["address_sfx_primary"][i]
            else:
                print("cross error in digit block primary for row" + str(i))
        else:
            cross = data["address_road_intersecting"][i]
            if(data["address_sfx_primary"][i] is np.nan):
                pass
            elif(data["address_sfx_primary"][i] is not np.nan):
                cross = cross + " " + data["address_sfx_primary"][i]
            else:
                print("cross error in non-digit block primary for row" + str(i))
    except AttributeError as error:
        cross = ""
    crosses.append(cross)
for i in range(0, len(data)):
    if(names[i] != "" and crosses[i] != ""):
        combined = names[i] + " & " + crosses[i]
        names_and_crosses.append(combined)
    else:
        number = int(data["address_number_primary"][i])
        if(number >= 100):
            number += 50
        if(str(data["address_road_primary"][i]).isdigit()):
            result = str(data["address_road_primary"][i]) + " " + str(data["address_sfx_primary"][i])
            names_and_crosses.append(result)
        #elif(bool(re.search(r'\d', str(data["address_road_primary"][i])))):
        #    result = str(data["address_road_primary"][i]) + " " + str(data["address_sfx_primary"][i])
        #    names_and_crosses.append(result)
        else:
            result = str(number) + " " + str(data["address_road_primary"][i]) + " " + str(data["address_sfx_primary"][i])
            names_and_crosses.append(result)
#append results to columns in the dataframe, save that dataframe as a separate copy
data['interstate'] = names
data['crossint'] = crosses
data['inter & cross'] = names_and_crosses
data.to_csv(to_save)