import pandas as pd
import numpy as np
import datetime as dt
from EC_SCEN import Interest_Rates

#getter function to read values and store in dataframe
#main function to drive valuation
#helper functions to do independent calculations

class Bonds:
    
    # Class data
    Input_df = pd.DataFrame
    Interest_Rates_obj = object()

    def __init__(self, Int_rate_obj):
        self.Input_df = pd.DataFrame
        self.Interest_Rates_obj =  Int_rate_obj   

    def get_data(self, file_name):
        self.Input_df = pd.read_csv(file_name)
    
    def Get_MV(self):
        MV = []
        for row in self.Input_df.itertuples():
            Redemp_date = dt.datetime(row.Redemp_Year,row.Redemp_Month,row.Redemp_Day)
            today = dt.date.today()
            term = (Redemp_date.year - today.year)*12 + (Redemp_date.month - today.month)
            CFL_arr = self.Get_CFL(row.Redemp_Amount, row.Cpn_Percent, term, row.Cpn_Frequency)
            # get discount rates from ec_Scen
            disc_rate = np.array(self.Interest_Rates_obj.zcb_prices[0:term])
            temp_mv = sum(CFL_arr*disc_rate)
            MV.append(temp_mv)
        self.Input_df["MV"] = MV

    def Get_CFL(self, redemp_amt, cpn_per, term, freq):
        cfl_arr = np.zeros(term)
        for i in range(1,term+1,int(12/freq)):
            cfl_arr[i] = (redemp_amt * cpn_per) / (freq * 100)
        cfl_arr[term-1]=cfl_arr[term-1] + redemp_amt
        return cfl_arr

Interest_Rates_object = Interest_Rates()
Interest_Rates_object.ReadRates("INPUTS\Interest_rates.csv")
Interest_Rates_object.InitializeRates()
Interest_Rates_object.InterpolateRates(Interest_Rates_object.input_rates.index, Interest_Rates_object.par_rates,6)
Interest_Rates_object.PartoSpotandZCB(6)
tenure = Interest_Rates_object.getTenures(Interest_Rates_object.par_rates)
Interest_Rates_object.InterpolateRates(Interest_Rates_object.input_rates.index, Interest_Rates_object.par_rates,1)
Interest_Rates_object.InterpolateRates(Interest_Rates_object.input_rates.index, Interest_Rates_object.spot_rates,1)
Interest_Rates_object.InterpolateRates(Interest_Rates_object.input_rates.index, Interest_Rates_object.zcb_prices,1)

Bond_obj = Bonds(Interest_Rates_object)
Bond_obj.get_data('INPUTS\Assets_Bonds.csv')
Bond_obj.Input_df.info()
Bond_obj.Get_MV()
print(Bond_obj.Input_df)

test= pd.DataFrame([Interest_Rates_object.zcb_prices,Interest_Rates_object.par_rates,Interest_Rates_object.spot_rates])
test.to_csv("Test.csv")
