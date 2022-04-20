# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 21:36:03 2022

@author: wb584620
"""
import pandas as pd

class clsTaxRevenueDashboard:

    """
    Function to read Country Metadata.
    It returns dataframe with country metadata from file.
    """
    def readCountryMetadata (self) -> pd.DataFrame:
        dfCntryMetadata = None
        try:
            dfCntryMetadata = pd.read_excel(self.strCntryFile)
        except Exception as e:
            print("TaxRevenueDashboard.readCountryMetadata: Unable to read country metadata")
            print("TaxRevenueDashboard.readCountryMetadata: Exception details")
            print(type(e))
            print(e.args)
            print(e)
        else:
            return dfCntryMetadata

    """
    Function to read CSV data provided by Sebastian.
    It returns dataframe with data from file.
    """
    def readData (self) -> pd.DataFrame:
        dfData = None
        try:
            dfData = pd.read_csv(self.strSrcFileName)
            dfData.fillna('')
        except Exception as e:
            print("TaxRevenueDashboard.readData: Unable to read data from CSV")
            print("TaxRevenueDashboard.readData: Exception details")
            print(type(e))
            print(e.args)
            print(e)
        else:
            return dfData

    """
    Constructor to initialize Tax Revenue Dashboard objects. It accepts
        paramStrCntryFile: Country Metadata File Name along with Full Path.
        paramStrDestFileName: Final Output File Name along with Full Path.
        paramIntFromYear: Starting Year to extract data.
        paramIntToYear: Ending Year to extract data.
    """
    def __init__(self, paramStrCntryFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\country_code_updated.xls", \
                       paramStrSrcFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\tax_revenue_27_sept_2021.csv", \
                       paramStrDestFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\High_Frequency_Indicators\\output\\Countries.xlsx", \
                       paramIntFromYear=2019, paramIntToYear=2021):
        self.strCntryFile = paramStrCntryFile
        self.strSrcFileName = paramStrSrcFileName
        self.dfData = self.readData()
        self.dfCountryMetaData = self.readCountryMetadata()
        self.strDestFileName = paramStrDestFileName
        self.intStartYear = paramIntFromYear
        self.intEndYear = paramIntToYear
        self.dictIndicators = {
            "Total_Revenue_incl_SC":{"name":"Total Revenue", "unit":"% of GDP", "code":"tRevenue", "multiplier":1},
            "Tax_Revenue":{"name":"Tax Revenue", "unit":"% of GDP", "code":"tTaxes", "multiplier":1},
            "Income_Taxes":{"name":"Income Taxes", "unit":"% of GDP", "code":"tIT", "multiplier":1},
            "PIT":{"name":"PIT", "unit":"% of GDP", "code":"tPIT", "multiplier":1},
            "CIT":{"name":"CIT", "unit":"% of GDP", "code":"tCIT", "multiplier":1},
            "Tax_on_Goods_and_Services":{"name":"Taxes on Goods and Services", "unit":"% of GDP", "code":"tG&S", "multiplier":1},
            "Value_Added_Tax":{"name":"VAT", "unit":"% of GDP", "code":"tVAT", "multiplier":1},
            "Excise_Taxes":{"name":"Excise Taxes", "unit":"% of GDP", "code":"tExcise", "multiplier":1},
            "Trade_Taxes":{"name":"Trade Taxes", "unit":"% of GDP", "code":"tTrade", "multiplier":1},
            "Social_Contributions":{"name":"Social Contributions", "unit":"% of GDP", "code":"tSC", "multiplier":1},
            "Property_Tax":{"name":"Property Taxes", "unit":"% of GDP", "code":"tProperty", "multiplier":1},
            "Other_Taxes":{"name":"Other Taxes", "unit":"% of GDP", "code":"tOther", "multiplier":1},
            "Direct_Taxes":{"name":"Direct Taxes", "unit":"% of GDP", "code":"tDirect", "multiplier":1},
            "Indirect_Taxes":{"name":"Indirect Taxes", "unit":"% of GDP", "code":"tIndirect", "multiplier":1},
            "Total_Non_Tax_Revenue":{"name":"Total Non-Tax Revenue", "unit":"% of GDP", "code":"tNon-TaxRevenue", "multiplier":1},
            "GDP_PC_Constant_USD":{"name":"GDP per Capita Constant USD", "unit":"USD", "code":"tGDPPCUSD", "multiplier":1},
            "ln_GDP_PC_Constant_USD":{"name":"Lognormal GDP per Capita", "unit":"", "code":"lGDPPCUSD", "multiplier":1},
            "GDP_Current_LCU":{"name":"GDP Current LCU", "unit":"LCU", "code":"GDPLCU", "multiplier":1},
            "GDP_Constant_USD":{"name":"GDP Constant USD", "unit":"USD", "code":"GDPUSD", "multiplier":1},
            "Trade":{"name":"Trade", "unit":"", "code":"Trade", "multiplier":1},
            "GDP_Current_LCU_lag":{"name":"GDP Current LCU lag", "unit":"", "code":"GDPLCUClag", "multiplier":1},
            "GDP_Current_LCU_gr":{"name":"GDP Current LCU growth", "unit":"", "code":"GDPLCUCgr", "multiplier":1},
            "Tax_Revenue_buoyancy":{"name":"Tax Revenue Buoyancy", "unit":"", "code":"bTaxes", "multiplier":1},
            "Income_Taxes_buoyancy":{"name":"Income Taxes Buoyancy", "unit":"", "code":"bIT", "multiplier":1},
            "PIT_buoyancy":{"name":"PIT Buoyancy", "unit":"", "code":"bPIT", "multiplier":1},
            "CIT_buoyancy":{"name":"CIT Buoyancy", "unit":"", "code":"bCIT", "multiplier":1},
            "Value_Added_Tax_buoyancy":{"name":"VAT Buoyancy", "unit":"", "code":"bVAT", "multiplier":1},
            "Excise_Taxes_buoyancy":{"name":"Excise Taxes Buoyancy", "unit":"", "code":"bExcise", "multiplier":1},
            "Trade_Taxes_buoyancy":{"name":"Trade Taxes Buoyancy", "unit":"", "code":"bTrade", "multiplier":1},
            "Social_Contributions_buoyancy":{"name":"Social Contributions Buoyancy", "unit":"", "code":"bSC", "multiplier":1},
            "Property_Tax_buoyancy":{"name":"Property Taxes Buoyancy", "unit":"", "code":"bProperty", "multiplier":1},
            "Tax_Revenue_real_USD":{"name":"Tax Revenue USD", "unit":"USD", "code":"TaxUSD", "multiplier":1},
            "Tax_Revenue_current_LCU":{"name":"Tax Revenue LCU", "unit":"LCU", "code":"TaxLCU", "multiplier":1},
            "gr_Tax_Revenue":{"name":"Tax Revenue Growth", "unit":"in %", "code":"TaxGrowth", "multiplier":1},
            "Tax_Capacity_Tax_Revenue":{"name":"Tax Capacity - Tax Revenue", "unit":"% of GDP", "code":"tcTaxes", "multiplier":1},
            "Tax_Capacity_Income_Taxes":{"name":"Tax Capacity - Income Taxes", "unit":"% of GDP", "code":"tcIT", "multiplier":1},
            "Tax_Capacity_PIT":{"name":"Tax Capacity - PIT", "unit":"% of GDP", "code":"tcPIT", "multiplier":1},
            "Tax_Capacity_CIT":{"name":"Tax Capacity - CIT", "unit":"% of GDP", "code":"tcCIT", "multiplier":1},
            "Tax_Capacity_Tax_on_Goods_and_Services":{"name":"Tax Capacity - Taxes on Goods and Services", "unit":"% of GDP", "code":"tcG&S", "multiplier":1},
            "Tax_Capacity_Value_Added_Tax":{"name":"Tax Capacity - VAT", "unit":"% of GDP", "code":"tcVAT", "multiplier":1},
            "Tax_Capacity_Excise_Taxes":{"name":"Tax Capacity - Excise Taxes", "unit":"% of GDP", "code":"tcExcises", "multiplier":1},
            "Tax_Capacity_Trade_Taxes":{"name":"Tax Capacity - Trade Taxes", "unit":"% of GDP", "code":"tcTrade", "multiplier":1},
            "Tax_Capacity_Social_Contributions":{"name":"Tax Capacity - Social_Contributions", "unit":"% of GDP", "code":"tcSC", "multiplier":1},
            "Tax_Capacity_Property_Tax":{"name":"Tax Capacity - Property Taxes", "unit":"% of GDP", "code":"tcProperty", "multiplier":1},
            "Tax_Gap_Tax_Revenue":{"name":"Tax Gap - Tax Revenue", "unit":"% of GDP", "code":"tgTaxes", "multiplier":1},
            "Tax_Gap_Income_Taxes":{"name":"Tax Gap - Income Taxes", "unit":"% of GDP", "code":"tgIT", "multiplier":1},
            "Tax_Gap_PIT":{"name":"Tax Gap - PIT", "unit":"% of GDP", "code":"tgPIT", "multiplier":1},
            "Tax_Gap_CIT":{"name":"Tax Gap - CIT", "unit":"% of GDP", "code":"tgCIT", "multiplier":1},
            "Tax_Gap_Tax_on_Goods_and_Services":{"name":"Tax Gap - Taxes on Goods and Services", "unit":"% of GDP", "code":"tgG&S", "multiplier":1},
            "Tax_Gap_Value_Added_Tax":{"name":"Tax Gap - VAT", "unit":"", "code":"tgVAT", "multiplier":1},
            "Tax_Gap_Excise_Taxes":{"name":"Tax Gap - Excise Taxes", "unit":"", "code":"tgExcises", "multiplier":1},
            "Tax_Gap_Trade_Taxes":{"name":"Tax Gap - Trade Taxes", "unit":"", "code":"tgTrade", "multiplier":1},
            "Tax_Gap_Social_Contributions":{"name":"Tax Gap - Social Contributions", "unit":"", "code":"tgSC", "multiplier":1},
            "Tax_Gap_Property_Tax":{"name":"Tax Gap - Property Taxes", "unit":"", "code":"tgProperty", "multiplier":1},
            "ln_GDP_PC_bin":{"name":"Lognormal GDP per Capita Bin", "unit":"", "code":"lGDPPCBin", "multiplier":1},
            "max_Tax_Revenue":{"name":"Maximum Tax Revenue", "unit":"% of GDP", "code":"mTaxes", "multiplier":1},
            "max_Income_Taxes":{"name":"Maximum Income Taxes", "unit":"% of GDP", "code":"mIT", "multiplier":1},
            "max_PIT":{"name":"Maximum PIT", "unit":"% of GDP", "code":"mPIT", "multiplier":1},
            "max_CIT":{"name":"Maximum CIT", "unit":"% of GDP", "code":"mCIT", "multiplier":1},
            "max_Tax_on_Goods_and_Services":{"name":"Maximum Taxes on Goods and Services", "unit":"% of GDP", "code":"mG&S", "multiplier":1},
            "max_Value_Added_Tax":{"name":"Maximum VAT", "unit":"% of GDP", "code":"mVAT", "multiplier":1},
            "max_Excise_Taxes":{"name":"Maximum Excise Taxes", "unit":"% of GDP", "code":"mExcise", "multiplier":1},
            "max_Trade_Taxes":{"name":"Maximum Trade Taxes", "unit":"% of GDP", "code":"mTrade", "multiplier":1},
            "max_Social_Contributions":{"name":"Maximum Social Contributions", "unit":"% of GDP", "code":"mSC", "multiplier":1},
            "max_Property_Tax":{"name":"Maximum Property Taxes", "unit":"% of GDP", "code":"mProperty", "multiplier":1},
            "outlier":{"name":"Outlier", "unit":"", "code":"Outlier", "multiplier":1},
            "pit_rate":{"name":"PIT Rate", "unit":"", "code":"rPIT", "multiplier":1},
            "cit_rate":{"name":"CIT Rate", "unit":"", "code":"rCIT", "multiplier":1},
            "indirect_tax_rate":{"name":"Indirect Tax Rate", "unit":"", "code":"rIndTax", "multiplier":1},
            "soc_contri_employer_rate":{"name":"Social Contributions - Employer Rate", "unit":"", "code":"rSCER", "multiplier":1},
            "soc_contri_employee_rate":{"name":"Social Contributions - Employee Rate", "unit":"", "code":"rSCEE", "multiplier":1},
            "labor_tax":{"name":"PIT + Employee Rate", "unit":"", "code":"rLabor", "multiplier":1},
            "labor_tax_all":{"name":"PIT + Employee Rate + Employer Rate", "unit":"", "code":"rLaborAll", "multiplier":1},
        }
    
    """
    Function to create long format with a unique row for each combination of Country, Year, Indicator from CSV file (with Frontier data) provided 
    by Sebastian.
    The original file has a unique row for each combination of Country, and Year with each indicator as column
    """
    def longFormat03Mar2022(self):
        flgProceed = True
        if ((self.dfCountryMetaData is None) and (flgProceed==True)):
            print("TaxRevenueDashboard.longFormat03Mar2022: Unable to read Country Metadata from File={}".format(self.paramStrCntryFile))
            flgProceed = False
            return None
        elif ((self.dfData is None) and (flgProceed==True)):
            print("TaxRevenueDashboard.longFormat03Mar2022: Unable to read Tax Revenue Data from File={}".format(self.strSrcFileName))
            flgProceed = False
            return None
        
        if flgProceed==True:
                    #return NonefData = pd.read_csv(self.strSrcFileName)
            strCntryColName = "Country_Code"
            lstDataDict = []
            lstCountries = list(self.dfData[strCntryColName].unique())
            lstColNames = list(self.dfData)
            lstCountries.sort()
            
            for c in lstCountries:
                lstFilter = self.dfCountryMetaData[self.dfCountryMetaData["Country_Code"]==c].to_dict("records")
                for j in range(self.intStartYear, self.intEndYear+1):
                    lstRow = self.dfData[(self.dfData[strCntryColName]==c) & (self.dfData["year"]==j)].to_dict("records")
                    for k in self.dictIndicators.keys():
                        if (k in lstColNames) and (len(lstRow)>0):
                            dictRow = {}
                            dictRow["country_name"] = lstFilter[0]["Country_Name"]
                            dictRow["year"] = j
                            dictRow["indicator name"] = self.dictIndicators[k]["name"]
                            dictRow["indicator unit"] = self.dictIndicators[k]["unit"]
                            dictRow["indicator code"] = self.dictIndicators[k]["code"]
                            dictRow["country_code"] = c
                            dictRow["iso3_code"] = c
                            dictRow["iso2_code"] = lstFilter[0]["Country_Code2"]
                            dictRow["resource_rich"] = lstFilter[0]["Resource_Rich"]
                            dictRow["oil_gas_rich"] = lstFilter[0]["Oil_Gas_Rich"]
                            dictRow["region_code"] = lstFilter[0]["Region_Code"]
                            dictRow["region_desc"] = lstFilter[0]["Region_Desc"]
                            dictRow["ida"] = lstFilter[0]["IDA"]
                            dictRow["income_group"] = lstFilter[0]["Income Group"]
                            dictRow["small_states"] = lstFilter[0]["Small_States"]
                            dictRow["ida_ibrd"] = lstFilter[0]["IDA_IBRD"]
                            dictRow["small_island_state"] = lstFilter[0]["Small_Island_State"]
                            if lstRow[0][k] != "":
                                if (("buoyancy" in self.dictIndicators[k]["name"].lower()) and ((lstRow[0][k]>3) or (lstRow[0][k]<-3))):
                                        dictRow["value"] = ""
                                else:
                                    dictRow["value"] = lstRow[0][k]*self.dictIndicators[k]["multiplier"]
                            else:
                                dictRow["value"] = ""
                            
                            lstDataDict.append(dictRow)
                print(len(lstDataDict))
        
            #print(dictRow)
            dfFinal = pd.DataFrame(lstDataDict)
            
            dfFinal.to_csv(self.strDestFileName, sep=',', encoding='utf-8',index=False)
    
def main():
    obj = clsTaxRevenueDashboard(paramStrCntryFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\country_code_updated.xls", \
                        paramStrSrcFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\tax_revenue_4_mar_2022.csv", \
                        paramStrDestFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\rev_tax_data2.csv", \
                        paramIntFromYear=1980, paramIntToYear=2021)
    obj.longFormat03Mar2022()


if __name__ == "__main__":
    main()