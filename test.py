import pandas as pd

if __name__ == '__main__':
    file = './SPREAD_1_SEC_0.5_ENERGY_1.0_EV-FACTOR_11_EV_2_FLEX_300_TPS.txt.xlsx'
    data = pd.read_excel(file)
    data.at[len(data)-1, 'Mode'] = 0.0
    data.to_excel(file, index=False)

    print(data.loc[len(data)-1, 'Mode'])