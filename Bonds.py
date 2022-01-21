import pandas as pd
import numpy as np
import datetime as dt

#getter function to read values and store in dataframe
#main function to drive valuation
#helper functions to do independent calculations

class Bonds:
    
    # Class data
    Input_df = pd.DataFrame
    
    def __init__(self):
        self.Input_df = pd.DataFrame    

    def get_data(self, file_name):
        self.Input_df = pd.read_csv(file_name)
    
    def Get_MV(self):
        for row in self.Input_df.itertuples():
            Redemp_date = dt.datetime(row.Redemp_Year,row.Redemp_Month,row.Redemp_Day)
            today = dt.date.today()
            term = (Redemp_date.year - today.year)*12 + (Redemp_date.month - today.month)
            CFL_arr = self.Get_CFL(row.Redemp_Amount, row.Cpn_Percent, term, row.Cpn_Frequency)
            # get discount rates from ec_Scen

    def Get_CFL(self, redemp_amt, cpn_per, term, freq):
        cfl_arr = np.zeros(term)
        for i in range(1,term+1,int(12/freq)):
            cfl_arr[i] = (redemp_amt * cpn_per) / (freq * 100)
        return cfl_arr

obj = Bonds()
obj.get_data('INPUTS\Assets_Bonds.csv')
obj.Input_df.info()
obj.Get_MV()
