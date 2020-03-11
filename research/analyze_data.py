#
# variables to keep:
#    current_precip_rate

import csv
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def twod_plots(data, target):
    for idx, sub_data in enumerate(data.columns):
        plt.subplot(3, 4, idx+1)
        plt.title(sub_data)
        plt.scatter(data[sub_data], target, label=sub_data)
    plt.show()

def main():
    file = "weather_annotated.csv"
    df = pd.read_csv(file, sep=',', header=0, names=["last_4_dewpt_avg","last_4_temp_avg","last_4_solar_radiation_high","last_4_humidity_avg","current_solar_radiation","current_humidity","current_temp","current_dewpt","current_precip_rate","previous_day_percip_total","is_greenbelt_dry"])
    target = df["is_greenbelt_dry"]
    data = df.drop(columns="is_greenbelt_dry")



if __name__ == '__main__':
    main()
