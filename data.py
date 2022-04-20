# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

"""
Function to create wide format with a unique row for each combination of Country, Year with Indicators as columns
"""
def wideFormatIndicatorsAsColumns(strSrcFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\Dummy_Data.xlsx", \
                                  strCntryFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\country_code_updated.xls", \
                                  strDestFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\Dummy_Data.csv", \
                                  strCntryColName="Country Name", strIndicatorNameColumn="Indicator Name", \
                                  intFromYear=1980, intToYear=2021):
    dfData = pd.read_excel(strSrcFileName)
    dfCntry = pd.read_excel(strCntryFile)
    dfData = dfData.fillna('')
    
    lstDataDict = []
    
    for i in dfData.iterrows():
        lstFilter = list(dfCntry[dfCntry["Country_Name"]==i[1][strCntryColName]].iloc())
        for j in range(intToYear-intFromYear+1):
            dictRow = {}
            dictRow["country_name"] = i[1][strCntryColName]
            dictRow["year"] = j+intFromYear
            dictRow[i[1].get(strIndicatorNameColumn,"")] = i[1].get(j+intFromYear,"")
            dictRow["country_code"] = i[1]["Country Code"]
            dictRow["iso3_code"] = lstFilter[0][0]
            dictRow["iso2_code"] = lstFilter[0][9]
            dictRow["resource_rich"] = lstFilter[0][2]
            dictRow["oil_gas_rich"] = lstFilter[0][3]
            dictRow["region_desc"] = lstFilter[0][5]
            dictRow["ida"] = lstFilter[0][6]
            dictRow["income_group"] = lstFilter[0][8]
            dictRow["small_states"] = lstFilter[0][10]
            dictRow["ida_ibrd"] = lstFilter[0][11]
            dictRow["small_island_state"] = lstFilter[0][12]
            lstDataDict.append(dictRow)
    
    dfFinal = pd.DataFrame(lstDataDict)
    
    dfFinal.to_csv(strDestFileName, sep=',', encoding='utf-8',index=False)


"""
Function to create long format with a unique row for each combination of Country, Year, Indicator
"""
def longFormat1(strSrcFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\Dummy_Data.xlsx", \
                                  strCntryFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\country_code_updated.xls", \
                                  strDestFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\Dummy_Data.csv", \
                                  strCntryColName="Country Name", strIndicatorNameColumn="Indicator Name", \
                                  intFromYear=1980, intToYear=2021):
    dfData = pd.read_excel(strSrcFileName)
    dfCntry = pd.read_excel(strCntryFile)
    dfData = dfData.fillna('')
    
    lstDataDict = []
    
    for i in dfData.iterrows():
        lstFilter = list(dfCntry[dfCntry["Country_Name"]==i[1][strCntryColName]].iloc())
        for j in range(intToYear-intFromYear+1):
            dictRow = {}
            dictRow["country_name"] = i[1][strCntryColName]
            dictRow["year"] = j+intFromYear
            dictRow["indicator name"] = i[1].get(strIndicatorNameColumn,"")
            dictRow["value"] = i[1].get(j+intFromYear,"")
            dictRow["country_code"] = i[1]["Country Code"]
            dictRow["iso3_code"] = lstFilter[0][0]
            dictRow["iso2_code"] = lstFilter[0][9]
            dictRow["resource_rich"] = lstFilter[0][2]
            dictRow["oil_gas_rich"] = lstFilter[0][3]
            dictRow["region_desc"] = lstFilter[0][5]
            dictRow["ida"] = lstFilter[0][6]
            dictRow["income_group"] = lstFilter[0][8]
            dictRow["small_states"] = lstFilter[0][10]
            dictRow["ida_ibrd"] = lstFilter[0][11]
            dictRow["small_island_state"] = lstFilter[0][12]
            lstDataDict.append(dictRow)
    
    print(dictRow)
    dfFinal = pd.DataFrame(lstDataDict)
    
    dfFinal.to_csv(strDestFileName, sep=',', encoding='utf-8',index=False)

"""
Function to create long format with a unique row for each combination of Country, Year, Indicator from CSV file provided 
by Sebastian. The column headers were modified to replace "_" with " ". Similar changes were done in Country Metadata Excel file as well.
Units were added in paranthesis for each indicator.
The original file has a unique row for each combination of Country, and Year with each indicator as column
"""
def longFormat2(strSrcFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\tax_revenue_27_sept_2021.csv", \
                                  strCntryFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\country_code_updated.xls", \
                                  strDestFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\rev_tax_data.csv", \
                                  strCntryColName="Country_Code", intIndicatorStartColumn=3, intIndicatorEndColumn=23,\
                                  intFromYear=1980, intToYear=2021):
    dfData = pd.read_csv(strSrcFileName)
    lstColumns = list(dfData.columns)
    dfCntry = pd.read_excel(strCntryFile)
    dfData = dfData.fillna('')
    dictIndicatorCodes = {
        "Total Revenue (% of GDP)":"Revenue",
        "Tax Revenue (% of GDP)":"Taxes",
        "Income Taxes (% of GDP)":"IT",
        "PIT (% of GDP)":"PIT",
        "CIT (% of GDP)":"CIT",
        "Tax on Goods and Services (% of GDP)":"G&S",
        "Value Added Tax (% of GDP)":"VAT",
        "Excise Taxes (% of GDP)":"Excise",
        "Trade Taxes (% of GDP)":"Trade",
        "Social Contributions (% of GDP)":"SC",
        "Property Tax (% of GDP)":"Property",
        "Other Taxes (% of GDP)":"Others",
        "Direct Taxes (% of GDP)":"Direct",
        "Indirect Taxes (% of GDP)":"Indirect",
        "Total Non Tax Revenue (% of GDP)":"Non Tax Revenue",
        "GDP (Current LCU)":"GDP LCU",
        "GDP (Constant USD)":"GDP USD",
        "Tax Revenue (real USD)":"Tax USD",
        "Tax Revenue (current LCU)":"Tax LCU",
        "gr Tax Revenue (in %)":"Tax Growth",
        "outlier":"Outlier",
        }
    
    lstDataDict = []
    
    lstCountries = list(dfData[strCntryColName].unique())
    lstCountries.sort()
    
    for c in lstCountries:
        lstFilter = list(dfCntry[dfCntry["Country_Code"]==c].iloc())
        for j in range(intFromYear, intToYear+1):
            lstRow = list(dfData[(dfData[strCntryColName]==c) & (dfData["year"]==j)].iloc())
            for k in range(intIndicatorStartColumn-1, intIndicatorEndColumn):
                dictRow = {}
                dictRow["country_name"] = lstFilter[0][7]
                dictRow["year"] = j
                if lstColumns[k].rfind(" (") != -1:
                    dictRow["indicator name"] = lstColumns[k][:lstColumns[k].rfind(" (")]
                    dictRow["indicator unit"] = lstColumns[k][lstColumns[k].rfind(" (")+2:len(lstColumns[k])-1]
                else:
                    dictRow["indicator name"] = lstColumns[k]
                    dictRow["indicator unit"] = ""
                dictRow["indicator code"] = dictIndicatorCodes.get(lstColumns[k], "")
                dictRow["country_code"] = c
                dictRow["iso3_code"] = lstFilter[0][0]
                dictRow["iso2_code"] = lstFilter[0][9]
                dictRow["resource_rich"] = lstFilter[0][2]
                dictRow["oil_gas_rich"] = lstFilter[0][3]
                dictRow["region_code"] = lstFilter[0][4]
                dictRow["region_desc"] = lstFilter[0][5]
                dictRow["ida"] = lstFilter[0][6]
                dictRow["income_group"] = lstFilter[0][8]
                dictRow["small_states"] = lstFilter[0][10]
                dictRow["ida_ibrd"] = lstFilter[0][11]
                dictRow["small_island_state"] = lstFilter[0][12]
                if len(lstRow)>0:
                    if dictRow["indicator unit"]=="% of GDP":
                        dictRow["value"] = lstRow[0][k]*100
                    else:
                        dictRow["value"] = lstRow[0][k]
                else:
                    dictRow["value"] = ""
                lstDataDict.append(dictRow)
    
    #print(dictRow)
    dfFinal = pd.DataFrame(lstDataDict)
    
    dfFinal.to_csv(strDestFileName, sep=',', encoding='utf-8',index=False)

"""
Function to create long format with a unique row for each combination of Country, Year, Indicator from CSV file (with Frontier data) provided 
by Sebastian.
The original file has a unique row for each combination of Country, and Year with each indicator as column
"""
def longFormat3(strSrcFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\tax_revenue_2_nov_2021.csv", \
                                  strCntryFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\country_code_updated.xls", \
                                  strDestFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\rev_tax_data2.csv", \
                                  strCntryColName="Country_Code", intFromYear=1980, intToYear=2021):
    dfData = pd.read_csv(strSrcFileName)
    dfData = dfData.fillna('')
    dfCntry = pd.read_excel(strCntryFile)
    dictIndicators = {
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
    }

    lstDataDict = []
    
    lstCountries = list(dfData[strCntryColName].unique())
    lstCountries.sort()
    
    for c in lstCountries:
        lstFilter = dfCntry[dfCntry["Country_Code"]==c].to_dict("records")
        for j in range(intFromYear, intToYear+1):
            lstRow = dfData[(dfData[strCntryColName]==c) & (dfData["year"]==j)].to_dict("records")
            for k in dictIndicators.keys():
                if len(lstRow)>0:
                    dictRow = {}
                    dictRow["country_name"] = lstFilter[0]["Country_Name"]
                    dictRow["year"] = j
                    dictRow["indicator name"] = dictIndicators[k]["name"]
                    dictRow["indicator unit"] = dictIndicators[k]["unit"]
                    dictRow["indicator code"] = dictIndicators[k]["code"]
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
                        dictRow["value"] = lstRow[0][k]*dictIndicators[k]["multiplier"]
                    else:
                        dictRow["value"] = ""
                lstDataDict.append(dictRow)
        print(len(lstDataDict))
    
    #print(dictRow)
    dfFinal = pd.DataFrame(lstDataDict)
    
    dfFinal.to_csv(strDestFileName, sep=',', encoding='utf-8',index=False)

def main():
    longFormat2()


if __name__ == "__main__":
    main()