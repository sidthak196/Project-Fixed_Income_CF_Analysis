import pandas as pd
from pandas.core.indexing import check_bool_indexer

class Interest_Rates:

    def __init__(self):
        self.input_rates = pd.DataFrame
        self.par_rates = [0] * 361 
        self.spot_rates = [0] * 361
        self.zcb_prices = [0] * 361

    # read rates just ZCB for now
    def ReadRates(self, Scenario_File):
        self.input_rates = pd.read_csv(Scenario_File, index_col='Term')  
        print(self.input_rates.dtypes)  
    
    # store rates
    def InitializeRates(self):
        for i in self.input_rates.index:
            self.par_rates[i] = self.input_rates.loc[i][0]
    
    # interpolate rates 
    def InterpolateRates(self, tenures, target_rates, step):
        high_index = 1
        for i in range(0,len(target_rates), step):
            if target_rates[i]!=0 or i == 0:
                continue
            #set the high index
            while True:
                if tenures[high_index]<i:
                    high_index +=1
                else:
                    break
            target_rates[i] = target_rates[tenures[high_index-1]] + (((i-tenures[high_index-1])*(target_rates[tenures[high_index]]-target_rates[tenures[high_index-1]]))/(tenures[high_index]-tenures[high_index-1]))
            target_rates[i] = round(target_rates[i],3)
    
    #Bootstrapping
    def PartoSpotandZCB(self, step):
        ann_factor = 0
        for i in range(0,len(self.par_rates),step):
            if i <= 6:
                self.spot_rates[i] = self.par_rates[i]
                self.zcb_prices[i] = (1/(1+self.spot_rates[i]))**(i/12)
                ann_factor = ann_factor + self.zcb_prices[i]
                continue
            self.zcb_prices[i] = round((1 - ((self.par_rates[i]/(100*12/step))*ann_factor))/(1+(self.par_rates[i]/(100*12/step))),5)
            self.spot_rates[i] = round(((1/ self.zcb_prices[i])**(12/i) - 1)*100,3)
            ann_factor = ann_factor + self.zcb_prices[i]
        for i in range(0,6):
            self.spot_rates[i] = self.par_rates[i]
            self.zcb_prices[i] = (1/(1+self.spot_rates[i]))**(i/12)
    
    def getTenures(self, rates):
        tenures = []
        i = 0
        for val in rates:
            if val != 0:
                tenures.append(i)
            i= i+1 
        return tenures

Interest_Rates_object = Interest_Rates()
Interest_Rates_object.ReadRates("INPUTS\Interest_rates.csv")
Interest_Rates_object.InitializeRates()
Interest_Rates_object.InterpolateRates(Interest_Rates_object.input_rates.index, Interest_Rates_object.par_rates,6)
Interest_Rates_object.PartoSpotandZCB(6)
tenure = Interest_Rates_object.getTenures(Interest_Rates_object.par_rates)

Interest_Rates_object.InterpolateRates(Interest_Rates_object.input_rates.index, Interest_Rates_object.par_rates,1)
Interest_Rates_object.InterpolateRates(Interest_Rates_object.input_rates.index, Interest_Rates_object.spot_rates,1)
Interest_Rates_object.InterpolateRates(Interest_Rates_object.input_rates.index, Interest_Rates_object.zcb_prices,1)


