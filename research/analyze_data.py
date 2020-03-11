import csv
import pandas as pd

def main():
    file = "weather_annotated.csv"
    df = pd.read_csv(file, sep=',')


if __name__ == '__main__':
    main()
