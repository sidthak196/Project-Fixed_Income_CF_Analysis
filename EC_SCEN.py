import pandas as pd

class Interest_Rates:

    def __init__(self):
        self.input_rates = pd.DataFrame
        self.par_rates = [0] * 361 

    # read rates just ZCB for now
    def ReadRates(self, Scenario_File):
        self.input_rates = pd.read_csv(Scenario_File, index_col='Term')  
        print(self.input_rates.dtypes)  
    
    # store rates
    def InitializeRates(self):
        for i in self.input_rates.index:
            self.par_rates[i] = self.input_rates.loc[i][0]
    
    # interpolate rates 
    def InterpolateRates(self):
        tenures = list(self.input_rates.index)
        high_index = 1
        for i in range(1,len(self.par_rates)):
            if self.par_rates[i]!=0:
                continue
            #set the high index
            while True:
                if tenures[high_index]<i:
                    high_index +=1
                else:
                    break
            self.par_rates[i] = self.par_rates[tenures[high_index-1]] + (((i-tenures[high_index-1])*(self.par_rates[tenures[high_index]]-self.par_rates[tenures[high_index-1]]))/(tenures[high_index]-tenures[high_index-1]))
            self.par_rates[i] = round(self.par_rates[i],3)
    
    #Bootstrapping
    def BootstrapRates(self):
        




Interest_Rates_object = Interest_Rates()
Interest_Rates_object.ReadRates("INPUTS\Interest_rates.csv")
Interest_Rates_object.InitializeRates()
Interest_Rates_object.InterpolateRates()
print(Interest_Rates_object.rates)

#print(Interest_Rates_object.rates)

