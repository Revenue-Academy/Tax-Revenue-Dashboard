# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 21:36:03 2022

@author: wb584620
"""
import traceback
import pandas as pd
import math
import sys

sys.path.insert(0, "c:\\users\\wb584620\\OneDrive - WBG\\Desktop\\work\\common\\code\\")
from clsLibraryFunctions import clsLibraryFunctions


class clsTaxRevenueDashboard:

    """
    Function to read Country Metadata.
    It returns dataframe with country metadata from file.
    """
    def readCountryMetadata (self, strCntryMetadataSheet) -> pd.DataFrame:
        dfCntryMetadata = None
        try:
            dictRet = self.objLF._readExcelData(self.strCntryFile, strCntryMetadataSheet)
            if dictRet.get("exception", "")=="":
                dfCntryMetadata = dictRet.get("data", None)
            else:
                self.__addErrors(dictRet.get("exception", "").replace("<classDet>:", "TaxRevenueDashboard.readCountryMetadata:"))
        except Exception as e:
            self.__addErrors("TaxRevenueDashboard.readCountryMetadata: Error - Unable to read country metadata\nTaxRevenueDashboard.readCountryMetadata: Exception details\n{}\n{}\n{}\n{}\n".format(type(e), e.args, e, traceback.format_exc()))
        finally:
            return dfCntryMetadata

    """
    Function to display errors encoutnered during processing.
    It displays the errors on screen
    """
    def __addErrors (self, strErrorMessage, strCountryName="Generic", strYear=""):
        lstErrors = self.__dictErrors.get("{}-{}".format(strCountryName, strYear), [])
        lstErrors.append(strErrorMessage)
        self.__dictErrors["{}-{}".format(strCountryName, strYear)] = list(set(lstErrors))

    """
    Function to display errors encoutnered during processing.
    It displays the errors on screen
    """
    def displayErrors (self, blnDisplayOnlyErrors=True):
        lstK = list(self.__dictErrors.keys())
        lstK.sort()
        for k in lstK:
            if blnDisplayOnlyErrors==False:
                print("\n".join(self.__dictErrors[k]))
            else:
                for s in list(self.__dictErrors[k]):
                    if "Error - " in s:
                        print(s,end="\n")

    """
    Function to read CSV data provided by Sebastian.
    It returns dataframe with data from file.
    """
    def readData (self) -> pd.DataFrame:
        dfData = None
        try:
            dfData = pd.read_csv(self.strSrcFileName, dtype={"year": int, "Total_Non_Tax_Revenue": float, "country_number":float})
            dfData.fillna('')
        except Exception as e:
            self.__addErrors("TaxRevenueDashboard.readData: Error - Unable to read country metadata\nTaxRevenueDashboard.readData: Exception details\n{}\n{}\n{}\n{}\n".format(type(e), e.args, e, traceback.format_exc()))
        finally:
            return dfData

    """
    Function to transform Revenue Forgone dataframe.
    It accepts following parameters:
        dfData (DataFrame) - DataFrame containing Revenue Forgone data
    It returns transformed dataframe.
    """
    def __transformRevForgoneDF (self, dfData) -> pd.DataFrame:
        try:
            if dfData.shape[0]>0:
                lstCols = list(dfData.columns)
                lstCols = list(map(lambda st: str.replace(st, " - Revenue Forgone (% of GDP)", ""), lstCols))
                dfData.columns = lstCols
                dfData = dfData.melt(id_vars=list(dfData.columns)[0])
                dfData.columns=["Year", "Country Name", "RevForgone_Value"]
                # validatecountries needs to be fixed
                dictRet = self.__validateCountries(list(dfData["Country Name"].unique()), self.strWBCountriesMappingFileName)
                if dictRet.get("exception", "")!="":
                    self.__addErrors(dictRet.get("exception", "").replace("<classDet>:", "TaxRevenueDashboard.transformRevForgoneDF-validateCountries:"))
                else:
                    if dictRet.get("errors")!="":
                        self.__addErrors(dictRet.get("errors", "").replace("<classDet>:", "TaxRevenueDashboard.transformRevForgoneDF-validateCountries:"))
                    dictCountries = dictRet.get("data",{})
                    for c in dictCountries.keys():
                        if dictCountries.get(c, "")=="":
                            dfData.loc[dfData["Country Name"]==c, "Cntry_Name"] = ""
                        else:
                            dfData.loc[dfData["Country Name"]==c, "Cntry_Name"] = dictCountries[c]
            else:
                self.__addErrors("TaxRevenueDashboard.transformRevForgoneDF: Error - No Revenue Forgone data\n")
        except Exception as e:
            self.__addErrors("TaxRevenueDashboard.transformRevForgoneDF: Error - Unable to transofrm Revenue Forgone data\nTaxRevenueDashboard.transformRevForgoneDF: Exception details\n{}\n{}\n{}\n{}\n".format(type(e), e.args, e, traceback.format_exc()))
            #traceback.print_exc()
        finally:
            return dfData

    """
    Function to read data from Fiscal Space file. It accepts
        paramStrFiscalSpaceFile: Fiscal Space File name along with complete path
        paramStrDataSheet: Data sheet name
    This funtction will return a data frame containing the data requested.
    """
    def __readFiscalSpaceData(self, paramStrFiscalSpaceFile, paramStrDataSheet, paramStrFunctionName) -> pd.DataFrame:
        try:
            dfData = None
            dictRet = {}
            dictRet = self.objLF._readExcelData(paramStrFiscalSpaceFile, paramStrDataSheet)
            if dictRet.get("exception", "")=="":
                dfData = dictRet.get("data", None)
                dfData = dfData.melt(id_vars=["Country Code", "IMF Country Code", "Country", "Country group",
                       "Geographical region", "Income group, as of July 1, 2022",
                       "Indicator Type", "Series Name"])
                dfData.columns = ["Country Code", "IMF Country Code", "Country", "Country group",
                       "Geographical region", "Income group, as of July 1, 2022",
                       "Indicator Type", "Series Name", "year", "{}_Value".format(paramStrFunctionName.replace(" ", "_"))]
                dictRet = {}
                dictRet = self.objLF._validateCountries(list(dfData["Country"].unique()), self.strWBCountriesMappingFileName)
                if dictRet.get("exception", "")!="":
                    self.__addErrors(dictRet.get("exception", "").replace("<classDet>:", "TaxRevenueDashboard.readFiscalSpaceData-{}-validateCountries:".format(paramStrFunctionName)))
                else:
                    if dictRet.get("errors")!="":
                        self.__addErrors(dictRet.get("errors", "").replace("<classDet>:", "TaxRevenueDashboard.readFiscalSpaceData-{}-validateCountries:".format(paramStrFunctionName)))
                dictCountries = dictRet.get("data",{})
                for c in dictCountries.keys():
                    if dictCountries.get(c, "")=="":
                        dfData.loc[dfData["Country"]==c, "Country_Code"] = ""
                    else:
                        dfData.loc[dfData["Country"]==c, "Country_Code"] = self.__dfCountryMetaData.loc[self.__dfCountryMetaData["Country_Name"]==dictCountries[c], "Country_Code"].iloc[0]
                dfData.drop(["Country Code", "IMF Country Code", "Country", "Country group",
                       "Geographical region", "Income group, as of July 1, 2022",
                       "Indicator Type", "Series Name"], axis=1, inplace=True)
                dfData["year"] = pd.to_numeric(dfData["year"])
            else:
                self.__addErrors(dictRet.get("exception", "").replace("<classDet>:", "TaxRevenueDashboard.readFiscalSpaceData-{}:".format(paramStrFunctionName)))
        except Exception as e:
            self.__addErrors("TaxRevenueDashboard.readFiscalSpaceData-{}: Error - Error while reading and transforming {} data\nTaxRevenueDashboard.readFiscalSpaceData-{}: Exception details\n{}\n{}\n{}\n{}\n".format(paramStrFunctionName, paramStrFunctionName, paramStrFunctionName, type(e), e.args, e, traceback.format_exc()))
            #traceback.print_exc()
        finally:
            return dfData

    """
    Function to read data from WDI files. It accepts
        paramStrWDIFile: WDI File name along with complete path
        paramStrDataSheet: Data sheet name
    This funtction will return a data frame containing the data requested.
    """
    def __readWDIData(self, paramStrWDIFile, paramStrDataSheet, paramStrFunctionName) -> pd.DataFrame:
        dfData = None
        dictRet = {}
        try:
            dictRet = self.objLF._readExcelData(paramStrWDIFile, paramStrDataSheet)
            if dictRet.get("exception", "")=="":
                dfData = dictRet.get("data", None)
                dfData = dfData.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"])
                dfData.columns = ["Country", "Country Code", "Indicator Name", "Indicator Code", "year", "{}_Value".format(paramStrFunctionName.replace(" ", "_"))]
                dictRet = {}
                dictRet = self.objLF._validateCountries(list(dfData["Country"].unique()), self.strWBCountriesMappingFileName)
                if dictRet.get("exception", "")!="":
                    self.__addErrors(dictRet.get("exception", "").replace("<classDet>:", "TaxRevenueDashboard.readWDIData-{}-validateCountries:".format(paramStrFunctionName)))
                else:
                    if dictRet.get("errors")!="":
                        self.__addErrors(dictRet.get("errors", "").replace("<classDet>:", "TaxRevenueDashboard.readWDIData-{}-validateCountries:".format(paramStrFunctionName)))
                dictCountries = dictRet.get("data",{})
                for c in dictCountries.keys():
                    if dictCountries.get(c, "")=="":
                        dfData.loc[dfData["Country"]==c, "Country_Code"] = ""
                    else:
                        dfData.loc[dfData["Country"]==c, "Country_Code"] = self.__dfCountryMetaData.loc[self.__dfCountryMetaData["Country_Name"]==dictCountries[c], "Country_Code"].iloc[0]
                dfData.drop(["Country", "Country Code", "Indicator Name", "Indicator Code"], axis=1, inplace=True)
                dfData["year"] = pd.to_numeric(dfData["year"])
            else:
                self.__addErrors(dictRet.get("exception", "").replace("<classDet>:", "TaxRevenueDashboard.readWDIData-{}:".format(paramStrFunctionName)))
        except Exception as e:
            self.__addErrors("TaxRevenueDashboard.readWDIData-{}: Error - Error while reading and transforming {} data\nTaxRevenueDashboard.readWDIData-{}: Exception details\n{}\n{}\n{}\n{}\n".format(paramStrFunctionName, paramStrFunctionName, paramStrFunctionName, type(e), e.args, e, traceback.format_exc()))
            #traceback.print_exc()
        finally:
            return dfData

    """
    Constructor to initialize Tax Revenue Dashboard objects. It accepts
        paramStrCntryFile: Country Metadata File Name along with Full Path.
        paramStrDestFileName: Final Output File Name along with Full Path.
        paramIntFromYear: Starting Year to extract data.
        paramIntToYear: Ending Year to extract data.
    """
    def __init__(self, paramStrCntryFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\country_code_updated.xls", 
                       paramStrSrcFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Revenue_Dashboard_v1\\tax_revenue_27_sept_2021.csv", 
                       paramStrDestFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\High_Frequency_Indicators\\output\\Countries.xlsx", 
                       paramStrRevForgoneFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\work\\RevExp-2Pager\\data\\GTED.xlsx",
                       paramStrExpensesFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\work\\RevExp-2Pager\\data\\WDI_Expenses.xlsx",
                       paramStrDebtFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\work\\RevExp-2Pager\\data\\GlobalDebtDatabase.xlsx",
                       paramStrWBCountriesMapping="c:\\users\\wb584620\\OneDrive - WBG\\Desktop\\work\\common\\data\\wb_countries_mapping.json", 
                       paramStrFiscalSpaceFile="c:\\users\\wb584620\\OneDrive - WBG\\Desktop\\work\\common\\data\\Fiscal-space-data.xlsx", 
                       paramStrGDPComponentsFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Work\\Revenue_Dashboard_v1\\data\\GDP_Components.xlsx", 
                       paramStrCntryMetadataSheet="country_code", 
                       paramStrRevForgoneSheet="Rev", 
                       paramStrExpensesSheet="Data", 
                       paramStrDebtSheet="wb_data", 
                       paramStrGGDebtSheet="ggdy", 
                       paramStrExternalDebtSheet="xtdebty", 
                       paramStrFiscalBalanceSheet="fby", 
                       paramStrPrivateSectorConsumptionExpenditureSheet="C", 
                       paramStrGGConsumptionExpenditureSheet="G", 
                       paramStrInvestmentSheet="I", 
                       paramStrExportsSheet="X", 
                       paramStrImportsSheet="M", 
                       paramIntFromYear=2019, paramIntToYear=2021):
        self.objLF=clsLibraryFunctions()
        self.__dictErrors = {}
        self.strCntryFile = paramStrCntryFile
        self.strSrcFileName = paramStrSrcFileName
        self.__dfData = self.readData()
        self.__dfCountryMetaData = self.readCountryMetadata(paramStrCntryMetadataSheet)
        self.strDestFileName = paramStrDestFileName
        self.strWBCountriesMappingFileName = paramStrWBCountriesMapping
        self.intStartYear = paramIntFromYear
        self.intEndYear = paramIntToYear
        self.strTaxRevInd = "Tax_Revenue"

        self.__dfGGDebt = None
        self.__dfFB = None
        self.__dfExtDebt = None
        self.__dfExpenses = None
        self.__dfC = None
        self.__dfG = None
        self.__dfI = None
        self.__dfX = None
        self.__dfM = None

        self.__dfGGDebt = self.__readFiscalSpaceData(paramStrFiscalSpaceFile, paramStrGGDebtSheet, "General Government Gross Debt")
        self.__dfFB = self.__readFiscalSpaceData(paramStrFiscalSpaceFile, paramStrFiscalBalanceSheet, "Fiscal Balance")
        self.__dfExtDebt = self.__readFiscalSpaceData(paramStrFiscalSpaceFile, paramStrExternalDebtSheet, "External Debt")
        #WDI Expenses (GC.XPN.TOTL.GD.ZS)
        self.__dfExpenses = self.__readWDIData(paramStrExpensesFile, paramStrExpensesSheet, "Expenses")
        #self.__dfExpenses = self.objLF._readWBGData("GC.XPN.TOTL.GD.ZS")["data"]
        #WDI Households and NPISHs final consumption expenditure (% of GDP) (NE.CON.PRVT.ZS)
        self.__dfC = self.__readWDIData(paramStrGDPComponentsFile, paramStrPrivateSectorConsumptionExpenditureSheet+"_USD", "Private Sector Consumption Expenditure")
        #self.__dfC = self.objLF._readWBGData("NE.CON.PRVT.ZS")["data"]
        #WDI General government final consumption expenditure (% of GDP) (NE.CON.GOVT.ZS)
        self.__dfG = self.__readWDIData(paramStrGDPComponentsFile, paramStrGGConsumptionExpenditureSheet+"_USD", "General Government Consumption Expenditure")
        #self.__dfG = self.objLF._readWBGData("NE.CON.GOVT.ZS")["data"]
        #WDI Net investment in nonfinancial assets (% of GDP) (GC.NFN.TOTL.GD.ZS)
        self.__dfI = self.__readWDIData(paramStrGDPComponentsFile, paramStrInvestmentSheet+"_USD", "Investments")
        #self.__dfI = self.objLF._readWBGData("GC.NFN.TOTL.GD.ZS")["data"]
        #WDI Exports of goods and services (% of GDP) (NE.EXP.GNFS.ZS)
        self.__dfX = self.__readWDIData(paramStrGDPComponentsFile, paramStrExportsSheet+"_USD", "Exports")
        #self.__dfX = self.objLF._readWBGData("NE.EXP.GNFS.ZS")["data"]
        #WDI Imports of goods and services (% of GDP) (NE.IMP.GNFS.ZS)
        self.__dfM = self.__readWDIData(paramStrGDPComponentsFile, paramStrImportsSheet+"_USD", "Imports")
        #self.__dfM = self.objLF._readWBGData("NE.IMP.GNFS.ZS")["data"]
        

        self.__dictIndicatorsBefore09NOV2022 = {
            "Total_Revenue_incl_SC":{"name":"Total Revenue", "unit":"% of GDP", "code":"tRevenue", "multiplier":1},
            "Tax_Revenue":{"name":"Tax Revenue", "unit":"% of GDP", "code":"tTaxes", "multiplier":1},
            "Income_Taxes":{"name":"Income Taxes", "unit":"% of GDP", "code":"tIT", "multiplier":1},
            "PIT":{"name":"PIT", "unit":"% of GDP", "code":"tPIT", "multiplier":1},
            "CIT":{"name":"CIT", "unit":"% of GDP", "code":"tCIT", "multiplier":1},
            "Value_Added_Tax":{"name":"VAT", "unit":"% of GDP", "code":"tVAT", "multiplier":1},
            "Excise_Taxes":{"name":"Excise Taxes", "unit":"% of GDP", "code":"tExcise", "multiplier":1},
            "Trade_Taxes":{"name":"Trade Taxes", "unit":"% of GDP", "code":"tTrade", "multiplier":1},
            "Property_Tax":{"name":"Property Taxes", "unit":"% of GDP", "code":"tProperty", "multiplier":1},
            "Social_Contributions":{"name":"Social Contributions", "unit":"% of GDP", "code":"tSC", "multiplier":1},
            "Other_Taxes":{"name":"Other Taxes", "unit":"% of GDP", "code":"tOther", "multiplier":1},
            "Tax_on_G_and_S":{"name":"Taxes on Goods and Services", "unit":"% of GDP", "code":"tG&S", "multiplier":1},
            "Total_Non_Tax_Revenue":{"name":"Total Non-Tax Revenue", "unit":"% of GDP", "code":"tNon-TaxRevenue", "multiplier":1},
            "Direct_Taxes":{"name":"Direct Taxes", "unit":"% of GDP", "code":"tDirect", "multiplier":1},
            "Indirect_Taxes":{"name":"Indirect Taxes", "unit":"% of GDP", "code":"tIndirect", "multiplier":1},
            "Income_Taxes_TR":{"name":"Income Taxes", "unit":"% of Tax Revenue", "code":"tITTR", "multiplier":1},
            "PIT_TR":{"name":"PIT", "unit":"% of Tax Revenue", "code":"tPITTR", "multiplier":1},
            "CIT_TR":{"name":"CIT", "unit":"% of Tax Revenue", "code":"tCITTR", "multiplier":1},
            "Value_Added_Tax_TR":{"name":"VAT", "unit":"% of Tax Revenue", "code":"tVATTR", "multiplier":1},
            "Excise_Taxes_TR":{"name":"Excise Taxes", "unit":"% of Tax Revenue", "code":"tExciseTR", "multiplier":1},
            "Trade_Taxes_TR":{"name":"Trade Taxes", "unit":"% of Tax Revenue", "code":"tTradeTR", "multiplier":1},
            "Property_Tax_TR":{"name":"Property Taxes", "unit":"% of Tax Revenue", "code":"tPropertyTR", "multiplier":1},
            "Other_Taxes_TR":{"name":"Other Taxes", "unit":"% of Tax Revenue", "code":"tOtherTR", "multiplier":1},
            "Tax_on_G_and_S_TR":{"name":"Taxes on Goods and Services", "unit":"% of Tax Revenue", "code":"tG&STR", "multiplier":1},
            "Tax_Revenue_buoyancy":{"name":"Tax Revenue Buoyancy", "unit":"", "code":"bTaxes", "multiplier":1},
            "Income_Taxes_buoyancy":{"name":"Income Taxes Buoyancy", "unit":"", "code":"bIT", "multiplier":1},
            "PIT_buoyancy":{"name":"PIT Buoyancy", "unit":"", "code":"bPIT", "multiplier":1},
            "CIT_buoyancy":{"name":"CIT Buoyancy", "unit":"", "code":"bCIT", "multiplier":1},
            "Value_Added_Tax_buoyancy":{"name":"VAT Buoyancy", "unit":"", "code":"bVAT", "multiplier":1},
            "Excise_Taxes_buoyancy":{"name":"Excise Taxes Buoyancy", "unit":"", "code":"bExcise", "multiplier":1},
            "Trade_Taxes_buoyancy":{"name":"Trade Taxes Buoyancy", "unit":"", "code":"bTrade", "multiplier":1},
            "Property_Tax_buoyancy":{"name":"Property Taxes Buoyancy", "unit":"", "code":"bProperty", "multiplier":1},
            "Social_Contributions_buoyancy":{"name":"Social Contributions Buoyancy", "unit":"", "code":"bSC", "multiplier":1},
            "Tax_Capacity_Tax_Revenue":{"name":"Tax Capacity - Tax Revenue", "unit":"% of GDP", "code":"tcTaxes", "multiplier":1},
            "Tax_Capacity_Income_Taxes":{"name":"Tax Capacity - Income Taxes", "unit":"% of GDP", "code":"tcIT", "multiplier":1},
            "Tax_Capacity_PIT":{"name":"Tax Capacity - PIT", "unit":"% of GDP", "code":"tcPIT", "multiplier":1},
            "Tax_Capacity_CIT":{"name":"Tax Capacity - CIT", "unit":"% of GDP", "code":"tcCIT", "multiplier":1},
            "Tax_Capacity_Value_Added_Tax":{"name":"Tax Capacity - VAT", "unit":"% of GDP", "code":"tcVAT", "multiplier":1},
            "Tax_Capacity_Excise_Taxes":{"name":"Tax Capacity - Excise Taxes", "unit":"% of GDP", "code":"tcExcises", "multiplier":1},
            "Tax_Capacity_Trade_Taxes":{"name":"Tax Capacity - Trade Taxes", "unit":"% of GDP", "code":"tcTrade", "multiplier":1},
            "Tax_Capacity_Property_Tax":{"name":"Tax Capacity - Property Taxes", "unit":"% of GDP", "code":"tcProperty", "multiplier":1},
            "Tax_Capacity_Social_Contributions":{"name":"Tax Capacity - Social_Contributions", "unit":"% of GDP", "code":"tcSC", "multiplier":1},
            "Tax_Capacity_Tax_on_Goods_and_Services":{"name":"Tax Capacity - Taxes on Goods and Services", "unit":"% of GDP", "code":"tcG&S", "multiplier":1},
            "Tax_Gap_Tax_Revenue":{"name":"Tax Gap - Tax Revenue", "unit":"% of GDP", "code":"tgTaxes", "multiplier":1},
            "Tax_Gap_Income_Taxes":{"name":"Tax Gap - Income Taxes", "unit":"% of GDP", "code":"tgIT", "multiplier":1},
            "Tax_Gap_PIT":{"name":"Tax Gap - PIT", "unit":"% of GDP", "code":"tgPIT", "multiplier":1},
            "Tax_Gap_CIT":{"name":"Tax Gap - CIT", "unit":"% of GDP", "code":"tgCIT", "multiplier":1},
            "Tax_Gap_Value_Added_Tax":{"name":"Tax Gap - VAT", "unit":"% of GDP", "code":"tgVAT", "multiplier":1},
            "Tax_Gap_Excise_Taxes":{"name":"Tax Gap - Excise Taxes", "unit":"% of GDP", "code":"tgExcises", "multiplier":1},
            "Tax_Gap_Trade_Taxes":{"name":"Tax Gap - Trade Taxes", "unit":"% of GDP", "code":"tgTrade", "multiplier":1},
            "Tax_Gap_Property_Tax":{"name":"Tax Gap - Property Taxes", "unit":"% of GDP", "code":"tgProperty", "multiplier":1},
            "Tax_Gap_Social_Contributions":{"name":"Tax Gap - Social Contributions", "unit":"% of GDP", "code":"tgSC", "multiplier":1},
            "Tax_Gap_Tax_on_Goods_and_Services":{"name":"Tax Gap - Taxes on Goods and Services", "unit":"% of GDP", "code":"tgG&S", "multiplier":1},
            "GDP_PC_Constant_USD":{"name":"GDP per Capita Constant USD", "unit":"USD", "code":"tGDPPCUSD", "multiplier":1},
            "ln_GDP_PC_Constant_USD":{"name":"Lognormal GDP per Capita", "unit":"", "code":"lGDPPCUSD", "multiplier":1},
            "GDP_Current_LCU":{"name":"GDP Current LCU", "unit":"LCU", "code":"GDPLCU", "multiplier":1},
            "GDP_Constant_USD":{"name":"GDP Constant USD", "unit":"USD", "code":"GDPUSD", "multiplier":1},
            "Trade":{"name":"Trade", "unit":"", "code":"Trade", "multiplier":1},
            "GDP_Current_LCU_lag":{"name":"GDP Current LCU lag", "unit":"", "code":"GDPLCUClag", "multiplier":1},
            "GDP_Current_LCU_gr":{"name":"GDP Current LCU growth", "unit":"", "code":"GDPLCUCgr", "multiplier":1},
            "Tax_Revenue_real_USD":{"name":"Tax Revenue USD", "unit":"USD", "code":"TaxUSD", "multiplier":1},
            "Tax_Revenue_current_LCU":{"name":"Tax Revenue LCU", "unit":"LCU", "code":"TaxLCU", "multiplier":1},
            "gr_Tax_Revenue":{"name":"Tax Revenue Growth", "unit":"in %", "code":"TaxGrowth", "multiplier":1},
            "ln_GDP_PC_bin":{"name":"Lognormal GDP per Capita Bin", "unit":"", "code":"lGDPPCBin", "multiplier":1},
            "max_Tax_Revenue":{"name":"Maximum Tax Revenue", "unit":"% of GDP", "code":"mTaxes", "multiplier":1},
            "max_Income_Taxes":{"name":"Maximum Income Taxes", "unit":"% of GDP", "code":"mIT", "multiplier":1},
            "max_PIT":{"name":"Maximum PIT", "unit":"% of GDP", "code":"mPIT", "multiplier":1},
            "max_CIT":{"name":"Maximum CIT", "unit":"% of GDP", "code":"mCIT", "multiplier":1},
            "max_Tax_on_Goods_and_Services":{"name":"Maximum Taxes on Goods and Services", "unit":"% of GDP", "code":"mG&S", "multiplier":1},
            "max_Value_Added_Tax":{"name":"Maximum VAT", "unit":"% of GDP", "code":"mVAT", "multiplier":1},
            "max_Excise_Taxes":{"name":"Maximum Excise Taxes", "unit":"% of GDP", "code":"mExcise", "multiplier":1},
            "max_Trade_Taxes":{"name":"Maximum Trade Taxes", "unit":"% of GDP", "code":"mTrade", "multiplier":1},
            "max_Property_Tax":{"name":"Maximum Property Taxes", "unit":"% of GDP", "code":"mProperty", "multiplier":1},
            "max_Social_Contributions":{"name":"Maximum Social Contributions", "unit":"% of GDP", "code":"mSC", "multiplier":1},
            "outlier":{"name":"Outlier", "unit":"", "code":"Outlier", "multiplier":1},
            "pit_rate":{"name":"PIT Rate", "unit":"", "code":"rPIT", "multiplier":1},
            "cit_rate":{"name":"CIT Rate", "unit":"", "code":"rCIT", "multiplier":1},
            "indirect_tax_rate":{"name":"Indirect Tax Rate", "unit":"", "code":"rIndTax", "multiplier":1},
            "soc_contri_employer_rate":{"name":"Social Contributions - Employer Rate", "unit":"", "code":"rSCER", "multiplier":1},
            "soc_contri_employee_rate":{"name":"Social Contributions - Employee Rate", "unit":"", "code":"rSCEE", "multiplier":1},
            "labor_tax_rate":{"name":"PIT + Employee Rate", "unit":"in %", "code":"rLabor", "multiplier":1},
            "labor_tax_all_rate":{"name":"PIT + Employee Rate + Employer Rate", "unit":"in %", "code":"rLaborAll", "multiplier":1},
        }

        self.__dictIndicators = {
            "Total_Revenue_incl_SC":{"name":"Total Revenue", "unit":"% of GDP", "code":"tRevenue", "multiplier":1, "df":"dfData"},
            "Tax_Revenue":{"name":"Tax Revenue", "unit":"% of GDP", "code":"tTaxes", "multiplier":1, "Buoyancy":"Tax_Revenue_buoyancy", "Capacity":"Tax_Capacity_Tax_Revenue", "Gap":"Tax_Gap_Tax_Revenue", "df":"dfData"},
            "Income_Taxes":{"name":"Income Taxes", "unit":"% of GDP", "code":"tIT", "multiplier":1, "Buoyancy":"Income_Taxes_buoyancy", "Capacity":"Tax_Capacity_Income_Taxes", "Gap":"Tax_Gap_Income_Taxes", "Tax Revenue Percent":"Income_Taxes_TR", "df":"dfData"},
            "PIT":{"name":"PIT", "unit":"% of GDP", "code":"tPIT", "multiplier":1, "Buoyancy":"PIT_buoyancy", "Capacity":"Tax_Capacity_PIT", "Gap":"Tax_Gap_PIT", "Tax Revenue Percent":"PIT_TR", "df":"dfData"},
            "CIT":{"name":"CIT", "unit":"% of GDP", "code":"tCIT", "multiplier":1, "Buoyancy":"CIT_buoyancy", "Capacity":"Tax_Capacity_CIT", "Gap":"Tax_Gap_CIT", "Tax Revenue Percent":"CIT_TR", "df":"dfData"},
            "Value_Added_Tax":{"name":"VAT", "unit":"% of GDP", "code":"tVAT", "multiplier":1, "Buoyancy":"Value_Added_Tax_buoyancy", "Capacity":"Tax_Capacity_Value_Added_Tax", "Gap":"Tax_Gap_Value_Added_Tax", "Tax Revenue Percent":"Value_Added_Tax_TR", "df":"dfData"},
            "Excise_Taxes":{"name":"Excise Taxes", "unit":"% of GDP", "code":"tExcise", "multiplier":1, "Buoyancy":"Excise_Taxes_buoyancy", "Capacity":"Tax_Capacity_Excise_Taxes", "Gap":"Tax_Gap_Excise_Taxes", "Tax Revenue Percent":"Excise_Taxes_TR", "df":"dfData"},
            "Trade_Taxes":{"name":"Trade Taxes", "unit":"% of GDP", "code":"tTrade", "multiplier":1, "Buoyancy":"Trade_Taxes_buoyancy", "Capacity":"Tax_Capacity_Trade_Taxes", "Gap":"Tax_Gap_Trade_Taxes", "Tax Revenue Percent":"Trade_Taxes_TR", "df":"dfData"},
            "Property_Tax":{"name":"Property Taxes", "unit":"% of GDP", "code":"tProperty", "multiplier":1, "Buoyancy":"Property_Tax_buoyancy", "Capacity":"Tax_Capacity_Property_Tax", "Gap":"Tax_Gap_Property_Tax", "Tax Revenue Percent":"Property_Tax_TR", "df":"dfData"},
            "Social_Contributions":{"name":"Social Contributions", "unit":"% of GDP", "code":"tSC", "multiplier":1, "Buoyancy":"Social_Contributions_buoyancy", "Capacity":"Tax_Capacity_Social_Contributions", "Gap":"Tax_Gap_Social_Contributions", "df":"dfData"},
            "Other_Taxes":{"name":"Other Taxes", "unit":"% of GDP", "code":"tOther", "multiplier":1, "Tax Revenue Percent":"Other_Taxes_TR", "df":"dfData"},
            "General_Government_Gross_Debt_Value":{"name":"General Government Gross Debt", "unit":"% of GDP", "code":"tGGDebt", "multiplier":1, "df":"dfGGDebt"},
            "External_Debt_Value":{"name":"External Debt", "unit":"% of GDP", "code":"tExtDebt", "multiplier":1, "df":"dfExtDebt"},
            "Internal_Debt_Value":{"name":"Internal Debt", "unit":"% of GDP", "code":"tIntDebt", "multiplier":1},
            "Fiscal_Balance_Value":{"name":"Fiscal Balance", "unit":"% of GDP", "code":"tFB", "multiplier":1, "df":"dfFB"},
            "Expenses_Value":{"name":"Expenses", "unit":"% of GDP", "code":"tExpenses", "multiplier":1, "df":"dfExpenses"},
            "Private_Sector_Consumption_Expenditure_Value":{"name":"Private Sector Consumption Expenditure (C)", "unit":"Constant USD", "code":"tGDP_C", "multiplier":1, "df":"dfC"},
            "General_Government_Consumption_Expenditure_Value":{"name":"General Government Consumption Expenditure (G)", "unit":"Constant USD", "code":"tGDP_G", "multiplier":1, "df":"dfG"},
            "Investments_Value":{"name":"Investments (I)", "unit":"Constant USD", "code":"tGDP_I", "multiplier":1, "df":"dfI"},
            "Exports_Value":{"name":"Exports (X)", "unit":"Constant USD", "code":"tGDP_X", "multiplier":1, "df":"dfX"},
            "Imports_Value":{"name":"Imports (M)", "unit":"Constant USD", "code":"tGDP_M", "multiplier":1, "df":"dfM"},
            "Tax_on_G_and_S":{"name":"Taxes on Goods and Services", "unit":"% of GDP", "code":"tG&S", "multiplier":1, "Buoyancy":"Tax_on_G_and_S_buoyancy",  "Capacity":"Tax_Capacity_Tax_on_G_and_S", "Gap":"Tax_Gap_Tax_on_G_and_S", "Tax Revenue Percent":"Tax_Gap_Tax_on_G_and_S_TR", "df":"dfData"},
            "Total_Non_Tax_Revenue":{"name":"Total Non-Tax Revenue", "unit":"% of GDP", "code":"tNon-TaxRevenue", "multiplier":1, "df":"dfData"},
            "Direct_Taxes":{"name":"Direct Taxes", "unit":"% of GDP", "code":"tDirect", "multiplier":1, "df":"dfData"},
            "Indirect_Taxes":{"name":"Indirect Taxes", "unit":"% of GDP", "code":"tIndirect", "multiplier":1, "df":"dfData"},
            "GDP_PC_Constant_USD":{"name":"GDP per Capita Constant USD", "unit":"USD", "code":"tGDPPCUSD", "multiplier":1, "df":"dfData"},
            "ln_GDP_PC_Constant_USD":{"name":"Lognormal GDP per Capita", "unit":"", "code":"lGDPPCUSD", "multiplier":1, "df":"dfData"},
            "GDP_Current_LCU":{"name":"GDP Current LCU", "unit":"LCU", "code":"GDPLCU", "multiplier":1, "df":"dfData"},
            "GDP_Constant_USD":{"name":"GDP Constant USD", "unit":"USD", "code":"GDPUSD", "multiplier":1, "df":"dfData"},
            "Trade":{"name":"Trade", "unit":"", "code":"Trade", "multiplier":1, "df":"dfData"},
            "GDP_Current_LCU_lag":{"name":"GDP Current LCU lag", "unit":"", "code":"GDPLCUClag", "multiplier":1, "df":"dfData"},
            "GDP_Current_LCU_gr":{"name":"GDP Current LCU growth", "unit":"", "code":"GDPLCUCgr", "multiplier":1, "df":"dfData"},
            "Tax_Revenue_real_USD":{"name":"Tax Revenue USD", "unit":"USD", "code":"TaxUSD", "multiplier":1, "df":"dfData"},
            "Tax_Revenue_current_LCU":{"name":"Tax Revenue LCU", "unit":"LCU", "code":"TaxLCU", "multiplier":1, "df":"dfData"},
            "gr_Tax_Revenue":{"name":"Tax Revenue Growth", "unit":"in %", "code":"TaxGrowth", "multiplier":1, "df":"dfData"},
            "ln_GDP_PC_bin":{"name":"Lognormal GDP per Capita Bin", "unit":"", "code":"lGDPPCBin", "multiplier":1, "df":"dfData"},
            "max_Tax_Revenue":{"name":"Maximum Tax Revenue", "unit":"% of GDP", "code":"mTaxes", "multiplier":1, "df":"dfData"},
            "max_Income_Taxes":{"name":"Maximum Income Taxes", "unit":"% of GDP", "code":"mIT", "multiplier":1, "df":"dfData"},
            "max_PIT":{"name":"Maximum PIT", "unit":"% of GDP", "code":"mPIT", "multiplier":1, "df":"dfData"},
            "max_CIT":{"name":"Maximum CIT", "unit":"% of GDP", "code":"mCIT", "multiplier":1, "df":"dfData"},
            "max_Tax_on_Goods_and_Services":{"name":"Maximum Taxes on Goods and Services", "unit":"% of GDP", "code":"mG&S", "multiplier":1, "df":"dfData"},
            "max_Value_Added_Tax":{"name":"Maximum VAT", "unit":"% of GDP", "code":"mVAT", "multiplier":1, "df":"dfData"},
            "max_Excise_Taxes":{"name":"Maximum Excise Taxes", "unit":"% of GDP", "code":"mExcise", "multiplier":1, "df":"dfData"},
            "max_Trade_Taxes":{"name":"Maximum Trade Taxes", "unit":"% of GDP", "code":"mTrade", "multiplier":1, "df":"dfData"},
            "max_Property_Tax":{"name":"Maximum Property Taxes", "unit":"% of GDP", "code":"mProperty", "multiplier":1, "df":"dfData"},
            "max_Social_Contributions":{"name":"Maximum Social Contributions", "unit":"% of GDP", "code":"mSC", "multiplier":1, "df":"dfData"},
            "outlier":{"name":"Outlier", "unit":"", "code":"Outlier", "multiplier":1, "df":"dfData"},
            "pit_rate":{"name":"PIT Rate", "unit":"", "code":"rPIT", "multiplier":1, "df":"dfData"},
            "cit_rate":{"name":"CIT Rate", "unit":"", "code":"rCIT", "multiplier":1, "df":"dfData"},
            "indirect_tax_rate":{"name":"Indirect Tax Rate", "unit":"", "code":"rIndTax", "multiplier":1, "df":"dfData"},
            "soc_contri_employer_rate":{"name":"Social Contributions - Employer Rate", "unit":"", "code":"rSCER", "multiplier":1, "df":"dfData"},
            "soc_contri_employee_rate":{"name":"Social Contributions - Employee Rate", "unit":"", "code":"rSCEE", "multiplier":1, "df":"dfData"},
            "labor_tax_rate":{"name":"PIT + Employee Rate", "unit":"in %", "code":"rLabor", "multiplier":1, "df":"dfData"},
            "labor_tax_all_rate":{"name":"PIT + Employee Rate + Employer Rate", "unit":"in %", "code":"rLaborAll", "multiplier":1, "df":"dfData"},
        }

        """
        # read and transform Revenue Forgone data
        dictRet = {}
        dictRet = self.objLF._readExcelData(paramStrRevForgoneFile, paramStrRevForgoneSheet)
        if dictRet.get("exception", "")=="":
            self.__dfRevForgone = dictRet.get("data", None)
        else:
            self.__addErrors(dictRet.get("exception", "").replace("<classDet>:", "TaxRevenueDashboard.init-Revenue Forgone:"))
        self.__dfRevForgone = self.__transformRevForgoneDF(self.__dfRevForgone)
        """

    
    """
    Function to create long format with a unique row for each combination of Country, Year, Indicator from CSV file (with Frontier data) provided 
    by Sebastian.
    The original file has a unique row for each combination of Country, and Year with each indicator as column
    """
    def longFormat03Mar2022(self):
        flgProceed = True
        if ((self.__dfCountryMetaData is None) and (flgProceed==True)):
            print("TaxRevenueDashboard.longFormat03Mar2022: Unable to read Country Metadata from File={}".format(self.paramStrCntryFile))
            flgProceed = False
            return None
        elif ((self.__dfData is None) and (flgProceed==True)):
            print("TaxRevenueDashboard.longFormat03Mar2022: Unable to read Tax Revenue Data from File={}".format(self.strSrcFileName))
            flgProceed = False
            return None
        
        if flgProceed==True:
                    #return NonefData = pd.read_csv(self.strSrcFileName)
            strCntryColName = "Country_Code"
            lstDataDict = []
            lstCountries = list(self.__dfData[strCntryColName].unique())
            lstColNames = list(self.__dfData)
            #print(lstColNames)
            lstCountries.sort()
            
            for c in lstCountries:
                lstFilter = self.__dfCountryMetaData[self.__dfCountryMetaData["Country_Code"]==c].to_dict("records")
                print("{} started".format(lstFilter[0]["Country_Name"]))
                for j in range(self.intStartYear, self.intEndYear+1):
                    lstRow = self.__dfData[(self.__dfData[strCntryColName]==c) & (self.__dfData["year"]==j)].to_dict("records")
                    #print(lstRow)
                    dblPITRate = ""
                    dblEmployerRate = ""
                    dblEmployeeRate = ""
                    for k in self.__dictIndicators.keys():
                        dictRow = {}
                        dictRow["country_name"] = lstFilter[0]["Country_Name"]
                        dictRow["year2"] = j
                        dictRow["indicator name"] = self.__dictIndicators[k]["name"]
                        dictRow["indicator unit"] = self.__dictIndicators[k]["unit"]
                        dictRow["indicator code"] = self.__dictIndicators[k]["code"]
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
                        #print("k1:{}".format(k))

                        if len(lstRow)>0:
                            if self.__dictIndicators[k]["unit"] == "% of Tax Revenue":
                                #print("k2:{}, len(lstRow):{}".format(k, len(lstRow)))
                                if (lstRow[0][k.replace("_TR", "")] != "") and (lstRow[0][self.strTaxRevInd] != "") and (lstRow[0][self.strTaxRevInd] != 0):
                                    dictRow["value"] = (lstRow[0][k.replace("_TR", "")] / lstRow[0][self.strTaxRevInd]) * 100
                                    #lstDataDict.append(dictRow)
                                else:
                                    dictRow["value"] = ""
                            elif (k in lstColNames):
                                if lstRow[0][k] != "":
                                    #print("{}-{}-{}\n{}".format(c,j,self.__dictIndicators[k]["name"],lstRow[0][k]))
                                    if ("buoyancy" in self.__dictIndicators[k]["name"].lower()):
                                        if lstRow[0][k]!="":
                                            if ((float(lstRow[0][k])>3) or (float(lstRow[0][k])<(-3))):
                                                dictRow["value"] = ""
                                            else:
                                                dictRow["value"] = lstRow[0][k]*self.__dictIndicators[k]["multiplier"]
                                                #lstDataDict.append(dictRow)
                                        else:
                                            dictRow["value"] = ""
                                    else:
                                        dictRow["value"] = lstRow[0][k]*self.__dictIndicators[k]["multiplier"]
                                        #lstDataDict.append(dictRow)
                                else:
                                    dictRow["value"] = ""

                                if self.__dictIndicators[k]["name"]=="PIT Rate":
                                    dblPITRate = lstRow[0][k]
                                elif self.__dictIndicators[k]["name"]=="Social Contributions - Employer Rate":
                                    dblEmployerRate = lstRow[0][k]
                                elif self.__dictIndicators[k]["name"]=="Social Contributions - Employer Rate":
                                    dblEmployeeRate = lstRow[0][k]

                                if ((dictRow["indicator name"]=="PIT + Employee Rate + Employer Rate") or (dictRow["indicator name"]=="PIT + Employee Rate")):
                                    #print("inside1")
                                    if lstRow[0][k]=="":
                                        if ((dictRow["indicator name"]=="PIT + Employee Rate + Employer Rate") and (dblPITRate!="") and (dblEmployeeRate!="") and (dblEmployerRate!="")):
                                            dictRow["value"] = float(dblPITRate) + float(dblEmployeeRate) + float(dblEmployerRate)
                                        elif ((dictRow["indicator name"]=="PIT + Employee Rate") and (dblPITRate!="") and (dblEmployeeRate!="")):
                                            dictRow["value"] = float(dblPITRate) + float(dblEmployeeRate)
                                
                        else:
                            dictRow["value"] = ""

                        #print(dictRow)
                        if str(dictRow.get("value","")).strip()!="":
                            if type(dictRow["value"])==int or type(dictRow["value"])==float:
                                lstDataDict.append(dictRow)

                print("{} completed\nTotal {} rows completed\n\n".format(lstFilter[0]["Country_Name"], len(lstDataDict)))
        
            #print(dictRow)
            dfFinal = pd.DataFrame(lstDataDict)
            
            dfFinal.to_csv(self.strDestFileName, sep=',', encoding='utf-8',index=False)
        
    """
    Function to create long format with a unique row for each combination of Country, Year, Indicator from CSV file (with Frontier data) provided 
    by Sebastian.
    The original file has a unique row for each combination of Country, and Year with each indicator as column
    """
    def longFormat11Oct2022(self):
        flgProceed = True
        if ((self.__dfCountryMetaData is None) and (flgProceed==True)):
            print("TaxRevenueDashboard.longFormat11Oct2022: Unable to read Country Metadata from File={}".format(self.strCntryFile))
            flgProceed = False
            return None
        elif ((self.__dfData is None) and (flgProceed==True)):
            print("TaxRevenueDashboard.longFormat11Oct2022: Unable to read Tax Revenue Data from File={}".format(self.strSrcFileName))
            flgProceed = False
            return None
        
        if flgProceed==True:
                    #return NonefData = pd.read_csv(self.strSrcFileName)
            strCntryColName = "Country_Code"
            lstDataDict = []
            lstCountries = list(self.__dfData[strCntryColName].unique())
            lstColNames = list(self.__dfData)
            #print(lstColNames)
            lstCountries.sort()
            
            for c in lstCountries:
                lstFilter = self.__dfCountryMetaData[self.__dfCountryMetaData["Country_Code"]==c].to_dict("records")
                print("{} started".format(lstFilter[0]["Country_Name"]))
                for j in range(self.intStartYear, self.intEndYear+1):
                    lstRow = self.__dfData[(self.__dfData[strCntryColName]==c) & (self.__dfData["year"]==j)].to_dict("records")
                    #print(lstRow)
                    dblPITRate = ""
                    dblEmployerRate = ""
                    dblEmployeeRate = ""
                    intTotalRevenue = None
                    intTaxRevenue = None
                    intTotalNonTaxRevenue = None
                    int
                    for k in self.__dictIndicators.keys():
                        dictRow = {}
                        dictRow["year2"] = j
                        dictRow["indicator name"] = self.__dictIndicators[k]["name"]
                        dictRow["indicator unit"] = self.__dictIndicators[k]["unit"]
                        dictRow["indicator code"] = self.__dictIndicators[k]["code"]
                        dictRow["iso3_code"] = c

                        if len(lstRow)>0:
                            if self.__dictIndicators[k]["unit"] == "% of Tax Revenue":
                                #print("k2:{}, len(lstRow):{}".format(k, len(lstRow)))
                                if (lstRow[0][k.replace("_TR", "")] != "") and (lstRow[0][self.strTaxRevInd] != "") and (lstRow[0][self.strTaxRevInd] != 0):
                                    dictRow["value"] = (lstRow[0][k.replace("_TR", "")] / lstRow[0][self.strTaxRevInd]) * 100
                                    #lstDataDict.append(dictRow)
                                else:
                                    dictRow["value"] = math.nan
                            elif (k in lstColNames):
                                if lstRow[0][k] != "":
                                    #print("{}-{}-{}\n{}".format(c,j,self.__dictIndicators[k]["name"],lstRow[0][k]))
                                    if ("buoyancy" in self.__dictIndicators[k]["name"].lower()):
                                        if lstRow[0][k]!="":
                                            if ((float(lstRow[0][k])>3) or (float(lstRow[0][k])<(-3))):
                                                dictRow["value"] = math.nan
                                            else:
                                                dictRow["value"] = lstRow[0][k]*self.__dictIndicators[k]["multiplier"]
                                                #lstDataDict.append(dictRow)
                                        else:
                                            dictRow["value"] = math.nan
                                    else:
                                        dictRow["value"] = lstRow[0][k]*self.__dictIndicators[k]["multiplier"]
                                        #lstDataDict.append(dictRow)
                                else:
                                    dictRow["value"] = math.nan

                                if self.__dictIndicators[k]["name"]=="PIT Rate":
                                    dblPITRate = lstRow[0][k]
                                elif self.__dictIndicators[k]["name"]=="Social Contributions - Employer Rate":
                                    dblEmployerRate = lstRow[0][k]
                                elif self.__dictIndicators[k]["name"]=="Social Contributions - Employer Rate":
                                    dblEmployeeRate = lstRow[0][k]

                                if ((dictRow["indicator name"]=="PIT + Employee Rate + Employer Rate") or (dictRow["indicator name"]=="PIT + Employee Rate")):
                                    #print("inside1")
                                    if lstRow[0][k]=="":
                                        if ((dictRow["indicator name"]=="PIT + Employee Rate + Employer Rate") and (dblPITRate!="") and (dblEmployeeRate!="") and (dblEmployerRate!="")):
                                            dictRow["value"] = float(dblPITRate) + float(dblEmployeeRate) + float(dblEmployerRate)
                                        elif ((dictRow["indicator name"]=="PIT + Employee Rate") and (dblPITRate!="") and (dblEmployeeRate!="")):
                                            dictRow["value"] = float(dblPITRate) + float(dblEmployeeRate)
                                
                        else:
                            dictRow["value"] = math.nan

                        #print(dictRow)
                        if self.__dictIndicators[k]["name"]=="Total Revenue" and math.isnan(dictRow["value"]):
                            intTotalRevenue = len(lstDataDict)
                        elif self.__dictIndicators[k]["name"]=="Tax Revenue" and math.isnan(dictRow["value"])==False:
                            intTaxRevenue = len(lstDataDict)
                        elif self.__dictIndicators[k]["name"]=="Total Non-Tax Revenue" and math.isnan(dictRow["value"])==False:
                            intTotalNonTaxRevenue = len(lstDataDict)

                        if str(dictRow.get("value","")).strip()!="":
                            if type(dictRow["value"])==int or type(dictRow["value"])==float:
                                lstDataDict.append(dictRow)

                        if intTotalRevenue!=None and intTaxRevenue!=None and intTotalNonTaxRevenue!=None:
                            #print("Before: R={}, T={}, N={}".format(lstDataDict[intTotalRevenue]["value"], lstDataDict[intTaxRevenue]["value"], lstDataDict[intTotalNonTaxRevenue]["value"]))
                            lstDataDict[intTotalRevenue]["value"] = lstDataDict[intTaxRevenue]["value"] + lstDataDict[intTotalNonTaxRevenue]["value"]
                            #print("After: R={}, T={}, N={}".format(lstDataDict[intTotalRevenue]["value"], lstDataDict[intTaxRevenue]["value"], lstDataDict[intTotalNonTaxRevenue]["value"]))
                            intTotalRevenue = None
                            intTaxRevenue = None
                            intTotalNonTaxRevenue = None
                            

                print("{} completed\nTotal {} rows completed\n\n".format(lstFilter[0]["Country_Name"], len(lstDataDict)))
        
            #print(dictRow)
            dfFinal = pd.DataFrame(lstDataDict)
            
            dfFinal.to_csv(self.strDestFileName, sep=',', encoding='utf-8',index=False)
        
    """
    Function to create hybrid format with a unique row for each combination of Country, Year, Indicator from CSV file (with Frontier data) provided 
    by Sebastian.
    The original file has a unique row for each combination of Country, and Year with each indicator as column
    """
    def hybridFormat09Nov2022(self):
        flgProceed = True
        if ((self.__dfCountryMetaData is None) and (flgProceed==True)):
            print("TaxRevenueDashboard.hybridFormat09Nov2022: Unable to read Country Metadata from File={}".format(self.strCntryFile))
            flgProceed = False
            return None
        elif ((self.__dfData is None) and (flgProceed==True)):
            print("TaxRevenueDashboard.hybridFormat09Nov2022: Unable to read Tax Revenue Data from File={}".format(self.strSrcFileName))
            flgProceed = False
            return None
        
        if flgProceed==True:
                    #return NonefData = pd.read_csv(self.strSrcFileName)
            strCntryColName = "Country_Code"
            lstDataDict = []
            lstCountries = list(self.__dfData[strCntryColName].unique())
            #lstColNames = list(self.__dfData)
            #print(lstColNames)
            #print(lstCountries)
            lstCountries.sort()
            
            for c in lstCountries:
                lstFilter = self.__dfCountryMetaData[self.__dfCountryMetaData["Country_Code"]==c].to_dict("records")
                print("{} started".format(lstFilter[0]["Country_Name"]))
                for j in range(self.intStartYear, self.intEndYear+1):
                    #print("{}-{}".format(c,j))
                    lstRow = self.__dfData[(self.__dfData[strCntryColName]==c) & (self.__dfData["year"]==j)].to_dict("records")
                    #print(lstRow)
                    #print("{}:{} year:{}".format(strCntryColName, c, j))
                    #print(self.__dfGGDebt[(self.__dfGGDebt[strCntryColName]==c)].shape)
                    #print(self.__dfGGDebt[(self.__dfGGDebt[strCntryColName]==c)].dtypes)
                    #print(self.__dfGGDebt[(self.__dfGGDebt["year"]==j)].shape)
                    #print(self.__dfGGDebt[(self.__dfGGDebt[strCntryColName]==c) & (self.__dfGGDebt["year"]==j)].shape)
                    lstGGDebtRow = self.__dfGGDebt[(self.__dfGGDebt[strCntryColName]==c) & (self.__dfGGDebt["year"]==j)].to_dict("records")
                    lstFBRow = self.__dfFB[(self.__dfFB[strCntryColName]==c) & (self.__dfFB["year"]==j)].to_dict("records")
                    lstExtDebtRow = self.__dfExtDebt[(self.__dfExtDebt[strCntryColName]==c) & (self.__dfExtDebt["year"]==j)].to_dict("records")
                    lstExpensesRow = self.__dfExpenses[(self.__dfExpenses[strCntryColName]==c) & (self.__dfExpenses["year"]==j)].to_dict("records")
                    lstCRow = self.__dfC[(self.__dfC[strCntryColName]==c) & (self.__dfC["year"]==j)].to_dict("records")
                    lstGRow = self.__dfG[(self.__dfG[strCntryColName]==c) & (self.__dfG["year"]==j)].to_dict("records")
                    lstIRow = self.__dfI[(self.__dfI[strCntryColName]==c) & (self.__dfI["year"]==j)].to_dict("records")
                    lstXRow = self.__dfX[(self.__dfX[strCntryColName]==c) & (self.__dfX["year"]==j)].to_dict("records")
                    lstMRow = self.__dfM[(self.__dfM[strCntryColName]==c) & (self.__dfM["year"]==j)].to_dict("records")

                    #print(lstRow)
                    #print(lstGGDebtRow)
                    dblPITRate = ""
                    dblEmployerRate = ""
                    dblEmployeeRate = ""
                    dblExtDebt = ""
                    dblGGDebt = ""
                    intTotalRevenue = None
                    intTaxRevenue = None
                    intTotalNonTaxRevenue = None
                    for k in self.__dictIndicators.keys():
                        if self.__dictIndicators[k].get("df","")=="dfData" and len(lstRow)>0:
                            lstFinalRow = lstRow
                        elif self.__dictIndicators[k].get("df","")=="dfGGDebt" and len(lstGGDebtRow)>0:
                            lstFinalRow = lstGGDebtRow
                        elif self.__dictIndicators[k].get("df","")=="dfFB" and len(lstFBRow)>0:
                            lstFinalRow = lstFBRow
                        elif self.__dictIndicators[k].get("df","")=="dfExtDebt" and len(lstExtDebtRow)>0:
                            lstFinalRow = lstExtDebtRow
                        elif self.__dictIndicators[k].get("df","")=="dfExpenses" and len(lstExpensesRow)>0:
                            lstFinalRow = lstExpensesRow
                        elif self.__dictIndicators[k].get("df","")=="dfC" and len(lstCRow)>0:
                            lstFinalRow = lstCRow
                        elif self.__dictIndicators[k].get("df","")=="dfG" and len(lstGRow)>0:
                            lstFinalRow = lstGRow
                        elif self.__dictIndicators[k].get("df","")=="dfI" and len(lstIRow)>0:
                            lstFinalRow = lstIRow
                        elif self.__dictIndicators[k].get("df","")=="dfX" and len(lstXRow)>0:
                            lstFinalRow = lstXRow
                        elif self.__dictIndicators[k].get("df","")=="dfM" and len(lstMRow)>0:
                            lstFinalRow = lstMRow
                            #print(lstFinalRow)
                        else:
                            lstFinalRow = None
                        #print(k)
                        #print("{}:{}\n{}".format(k, self.__dictIndicators[k]["df"],lstFinalRow))
                        dictRow = {}
                        dictRow["Year2"] = j
                        dictRow["indicator name"] = self.__dictIndicators[k]["name"]
                        dictRow["indicator unit"] = self.__dictIndicators[k]["unit"]
                        dictRow["indicator code"] = self.__dictIndicators[k]["code"]
                        dictRow["iso3_code"] = c
                        intMultiplier = self.__dictIndicators[k].get("multiplier", 1)

                        if lstFinalRow!=None and len(lstFinalRow)>0:
                            dblIncomeTaxes = lstFinalRow[0].get("Income_Taxes", math.nan)
                            dblVAT = lstFinalRow[0].get("Value_Added_Tax", math.nan)
                            dblExciseTaxes = lstFinalRow[0].get("Excise_Taxes", math.nan)
                            dblTradeTaxes = lstFinalRow[0].get("Trade_Taxes", math.nan)
                            dblPropertyTaxes = lstFinalRow[0].get("Property_Tax", math.nan)
                            dblOtherTaxes = lstFinalRow[0].get("Other_Taxes", math.nan)
                            #if c=="ABW" and j==2007:
                                #print("{}:{}\n{}:{}\n{}:{}\n{}:{}\n{}:{}\n{}:{}\n".format(dblIncomeTaxes, math.isnan(dblIncomeTaxes), dblVAT, math.isnan(dblVAT), dblExciseTaxes, math.isnan(dblExciseTaxes), dblTradeTaxes, math.isnan(dblTradeTaxes), dblPropertyTaxes, math.isnan(dblPropertyTaxes), dblOtherTaxes, math.isnan(dblOtherTaxes)))
                                #exit(0)
                            if math.isnan(dblIncomeTaxes)==False and math.isnan(dblVAT)==False and math.isnan(dblExciseTaxes)==False and math.isnan(dblTradeTaxes)==False and math.isnan(dblPropertyTaxes)==False:
                                dblTaxRevenueCalc = dblIncomeTaxes + dblVAT + dblExciseTaxes + dblTradeTaxes + dblPropertyTaxes + dblOtherTaxes
                            else:
                                dblTaxRevenueCalc = math.nan
                        else:
                            dblTaxRevenueCalc = math.nan
                                
                        
                        if k=="Total_Revenue_incl_SC":
                            #print("inside indicator")
                            if lstFinalRow!=None and len(lstFinalRow)>0:
                                #print("inside final row")
                                dblTotalRevenue = lstFinalRow[0].get("Total_Revenue_incl_SC", math.nan)
                                dblTaxRevenue = lstFinalRow[0].get("Tax_Revenue", math.nan)
                                dblNonTaxRevenue = lstFinalRow[0].get("Total_Non_Tax_Revenue", math.nan)
                                
                                if math.isnan(dblTotalRevenue)==False:
                                    dblTotalRevenueCalc = dblTotalRevenue
                                    #print("THen 1")
                                elif math.isnan(dblTotalRevenue)==True and (math.isnan(dblTaxRevenue)==False or math.isnan(dblNonTaxRevenue)==False):
                                    if math.isnan(dblTaxRevenue)==False and math.isnan(dblNonTaxRevenue)==False:
                                        dblTotalRevenueCalc = dblTaxRevenue + dblNonTaxRevenue
                                        #print("Else 1 Then 1")
                                    elif math.isnan(dblTaxRevenue)==False and math.isnan(dblNonTaxRevenue)==True:
                                        dblTotalRevenueCalc = dblTaxRevenue
                                        #print("Else 1 Else 1")
                                    elif math.isnan(dblTaxRevenue)==True and math.isnan(dblNonTaxRevenue)==False:
                                        dblTotalRevenueCalc = dblNonTaxRevenue
                                        #print("Else 1 Else 2")
                                elif math.isnan(dblTotalRevenue)==True and math.isnan(dblTaxRevenue)==True and math.isnan(dblNonTaxRevenue)==True:
                                    dblTotalRevenueCalc = math.nan
                                    #print("Else 2")
                            else:
                                dblTotalRevenueCalc = math.nan
                            dblValue = dblTotalRevenueCalc
                        else:
                            if lstFinalRow!=None and len(lstFinalRow)>0:
                                dblValue = lstFinalRow[0].get(k,math.nan)
                            else:
                                dblValue = math.nan

                        if ((dblValue!="") and (dblValue!=math.nan)):
                            #print("{}-{}-{}\n{}".format(c,j,self.__dictIndicators[k]["name"],lstRow[0][k]))
                            dictRow["value"] = dblValue * intMultiplier
                            #lstDataDict.append(dictRow)
                        else:
                            dictRow["value"] = math.nan

                        if self.__dictIndicators[k]["name"]=="PIT Rate":
                            dblPITRate = dblValue
                        elif self.__dictIndicators[k]["name"]=="Social Contributions - Employer Rate":
                            dblEmployerRate = dblValue
                        elif self.__dictIndicators[k]["name"]=="Social Contributions - Employer Rate":
                            dblEmployeeRate = dblValue
                        elif self.__dictIndicators[k]["name"]=="External Debt":
                            dblExtDebt = dblValue
                        elif self.__dictIndicators[k]["name"]=="General Government Gross Debt":
                            dblGGDebt = dblValue

                        if ((dictRow["indicator name"]=="PIT + Employee Rate + Employer Rate") or (dictRow["indicator name"]=="PIT + Employee Rate") or (dictRow["indicator name"]=="PIT + Employee Rate") or (dictRow["indicator name"]=="Internal Debt")):
                            #print("inside1")
                            if ((dictRow["indicator name"]=="PIT + Employee Rate + Employer Rate") and (dblPITRate!="") and (dblEmployeeRate!="") and (dblEmployerRate!="")):
                                dictRow["value"] = float(dblPITRate) + float(dblEmployeeRate) + float(dblEmployerRate)
                            elif ((dictRow["indicator name"]=="PIT + Employee Rate") and (dblPITRate!="") and (dblEmployeeRate!="")):
                                dictRow["value"] = float(dblPITRate) + float(dblEmployeeRate)
                            elif ((dictRow["indicator name"]=="Internal Debt") and (math.isnan(dblGGDebt)==False) and (math.isnan(dblExtDebt)==False)):
                                dictRow["value"] = float(dblGGDebt) - float(dblExtDebt)
                            elif ((dictRow["indicator name"]=="Internal Debt") and (math.isnan(dblGGDebt)==False) and (math.isnan(dblExtDebt)==True)):
                                dictRow["value"] = float(dblGGDebt)

                        strBuoyancy = self.__dictIndicators[k].get("Buoyancy", "")
                        #print("inside {}".format(strBuoyancy))
                        if ((strBuoyancy != "") and (lstFinalRow!=None)):
                            if (lstFinalRow[0][strBuoyancy] != ""):
                                if lstFinalRow[0][strBuoyancy]!="":
                                    if ((float(lstRow[0][strBuoyancy])>3) or (float(lstRow[0][strBuoyancy])<(-3))):
                                        dictRow["Buoyancy"] = math.nan
                                    else:
                                        dictRow["Buoyancy"] = lstRow[0][strBuoyancy]
                                else:
                                    dictRow["Buoyancy"] = math.nan
                            else:
                                dictRow["Buoyancy"] = math.nan
                        else:
                            dictRow["Buoyancy"] = math.nan

                        strCapacity = self.__dictIndicators[k].get("Capacity", "")
                        #print("inside {}".format(strCapacity))
                        if ((strCapacity != "") and (lstFinalRow!=None)):
                            if (lstFinalRow[0][strCapacity] != ""):
                                if lstFinalRow[0][strCapacity]!="":
                                    dictRow["Capacity"] = lstRow[0][strCapacity]
                                else:
                                    dictRow["Capacity"] = math.nan
                            else:
                                dictRow["Capacity"] = math.nan
                        else:
                            dictRow["Capacity"] = math.nan

                        strGap = self.__dictIndicators[k].get("Gap", "")
                        #print("inside {}".format(strGap))
                        if ((strGap != "") and (lstFinalRow!=None)):
                            if (lstFinalRow[0][strGap] != ""):
                                if lstFinalRow[0][strGap]!="":
                                    dictRow["Gap"] = lstRow[0][strGap]
                                else:
                                    dictRow["Gap"] = math.nan
                            else:
                                dictRow["Gap"] = math.nan
                        else:
                            dictRow["Gap"] = math.nan

                        strTRP = self.__dictIndicators[k].get("Tax Revenue Percent", "")
                        #print("inside {}".format(strTRP))
                        if ((strTRP != "") and (lstFinalRow!=None)):
                            #print("k2:{}, len(lstRow):{}".format(k, len(lstRow)))
                            if (lstFinalRow[0][k] != "") and (dblTaxRevenueCalc != "") and (dblTaxRevenueCalc != 0) and (math.isnan(dblTaxRevenueCalc)==False):
                                dictRow["Tax Revenue Percent"] = (lstFinalRow[0][k] / dblTaxRevenueCalc) * 100
                            else:
                                dictRow["Tax Revenue Percent"] = math.nan
                        else:
                            dictRow["Tax Revenue Percent"] = math.nan

                        lstDataDict.append(dictRow)

                print("{} completed\nTotal {} rows completed\n\n".format(lstFilter[0]["Country_Name"], len(lstDataDict)))
        
            #print(dictRow)
            dfFinal = pd.DataFrame(lstDataDict)
            
            dfFinal.to_csv(self.strDestFileName, sep=',', encoding='utf-8',index=False)

    """
    Function to create hybrid format with a unique row for each combination of Country, Year, Indicator from CSV file (with Frontier data) provided 
    by Sebastian.
    The original file has a unique row for each combination of Country, and Year with each indicator as column
    """
    def hybridFormat05Jan2023(self):
        flgProceed = True
        if ((self.__dfCountryMetaData is None) and (flgProceed==True)):
            print("TaxRevenueDashboard.hybridFormat05Jan2023: Unable to read Country Metadata from File={}".format(self.strCntryFile))
            flgProceed = False
            return None
        elif ((self.__dfData is None) and (flgProceed==True)):
            print("TaxRevenueDashboard.hybridFormat05Jan2023: Unable to read Tax Revenue Data from File={}".format(self.strSrcFileName))
            flgProceed = False
            return None
        
        if flgProceed==True:
                    #return NonefData = pd.read_csv(self.strSrcFileName)
            strCntryColName = "Country_Code"
            lstDataDict = []
            lstCountries = list(self.__dfData[strCntryColName].unique())
            #lstColNames = list(self.__dfData)
            #print(lstColNames)
            #print(lstCountries)
            lstCountries.sort()
            
            for c in lstCountries:
                lstFilter = self.__dfCountryMetaData[self.__dfCountryMetaData["Country_Code"]==c].to_dict("records")
                print("{} started".format(lstFilter[0]["Country_Name"]))
                for j in range(self.intStartYear, self.intEndYear+1):
                    #print("{}-{}".format(c,j))
                    lstRow = self.__dfData[(self.__dfData[strCntryColName]==c) & (self.__dfData["year"]==j)].to_dict("records")
                    #print(lstRow)
                    #print("{}:{} year:{}".format(strCntryColName, c, j))
                    #print(self.__dfGGDebt[(self.__dfGGDebt[strCntryColName]==c)].shape)
                    #print(self.__dfGGDebt[(self.__dfGGDebt[strCntryColName]==c)].dtypes)
                    #print(self.__dfGGDebt[(self.__dfGGDebt["year"]==j)].shape)
                    #print(self.__dfGGDebt[(self.__dfGGDebt[strCntryColName]==c) & (self.__dfGGDebt["year"]==j)].shape)
                    lstGGDebtRow = self.__dfGGDebt[(self.__dfGGDebt[strCntryColName]==c) & (self.__dfGGDebt["year"]==j)].to_dict("records")
                    lstFBRow = self.__dfFB[(self.__dfFB[strCntryColName]==c) & (self.__dfFB["year"]==j)].to_dict("records")
                    lstExtDebtRow = self.__dfExtDebt[(self.__dfExtDebt[strCntryColName]==c) & (self.__dfExtDebt["year"]==j)].to_dict("records")
                    lstExpensesRow = self.__dfExpenses[(self.__dfExpenses[strCntryColName]==c) & (self.__dfExpenses["year"]==j)].to_dict("records")
                    lstCRow = self.__dfC[(self.__dfC[strCntryColName]==c) & (self.__dfC["year"]==j)].to_dict("records")
                    lstGRow = self.__dfG[(self.__dfG[strCntryColName]==c) & (self.__dfG["year"]==j)].to_dict("records")
                    lstIRow = self.__dfI[(self.__dfI[strCntryColName]==c) & (self.__dfI["year"]==j)].to_dict("records")
                    lstXRow = self.__dfX[(self.__dfX[strCntryColName]==c) & (self.__dfX["year"]==j)].to_dict("records")
                    lstMRow = self.__dfM[(self.__dfM[strCntryColName]==c) & (self.__dfM["year"]==j)].to_dict("records")

                    #print(lstRow)
                    #print(lstGGDebtRow)
                    dblPITRate = ""
                    dblEmployerRate = ""
                    dblEmployeeRate = ""
                    dblExtDebt = ""
                    dblGGDebt = ""
                    for k in self.__dictIndicators.keys():
                        if self.__dictIndicators[k].get("df","")=="dfData" and len(lstRow)>0:
                            lstFinalRow = lstRow
                        elif self.__dictIndicators[k].get("df","")=="dfGGDebt" and len(lstGGDebtRow)>0:
                            lstFinalRow = lstGGDebtRow
                        elif self.__dictIndicators[k].get("df","")=="dfFB" and len(lstFBRow)>0:
                            lstFinalRow = lstFBRow
                        elif self.__dictIndicators[k].get("df","")=="dfExtDebt" and len(lstExtDebtRow)>0:
                            lstFinalRow = lstExtDebtRow
                        elif self.__dictIndicators[k].get("df","")=="dfExpenses" and len(lstExpensesRow)>0:
                            lstFinalRow = lstExpensesRow
                        elif self.__dictIndicators[k].get("df","")=="dfC" and len(lstCRow)>0:
                            lstFinalRow = lstCRow
                        elif self.__dictIndicators[k].get("df","")=="dfG" and len(lstGRow)>0:
                            lstFinalRow = lstGRow
                        elif self.__dictIndicators[k].get("df","")=="dfI" and len(lstIRow)>0:
                            lstFinalRow = lstIRow
                        elif self.__dictIndicators[k].get("df","")=="dfX" and len(lstXRow)>0:
                            lstFinalRow = lstXRow
                        elif self.__dictIndicators[k].get("df","")=="dfM" and len(lstMRow)>0:
                            lstFinalRow = lstMRow
                            #print(lstFinalRow)
                        else:
                            lstFinalRow = None
                        #print(k)
                        #print("{}:{}\n{}".format(k, self.__dictIndicators[k]["df"],lstFinalRow))
                        dictRow = {}
                        dictRow["Year2"] = j
                        dictRow["indicator name"] = self.__dictIndicators[k]["name"]
                        dictRow["indicator unit"] = self.__dictIndicators[k]["unit"]
                        dictRow["indicator code"] = self.__dictIndicators[k]["code"]
                        dictRow["iso3_code"] = c
                        intMultiplier = self.__dictIndicators[k].get("multiplier", 1)

                        if lstFinalRow!=None and len(lstFinalRow)>0:
                            dblIncomeTaxes = lstFinalRow[0].get("Income_Taxes", math.nan)
                            dblVAT = lstFinalRow[0].get("Value_Added_Tax", math.nan)
                            dblExciseTaxes = lstFinalRow[0].get("Excise_Taxes", math.nan)
                            dblTradeTaxes = lstFinalRow[0].get("Trade_Taxes", math.nan)
                            dblPropertyTaxes = lstFinalRow[0].get("Property_Tax", math.nan)
                            dblOtherTaxes = lstFinalRow[0].get("Other_Taxes", math.nan)
                            #if c=="ABW" and j==2007:
                                #print("{}:{}\n{}:{}\n{}:{}\n{}:{}\n{}:{}\n{}:{}\n".format(dblIncomeTaxes, math.isnan(dblIncomeTaxes), dblVAT, math.isnan(dblVAT), dblExciseTaxes, math.isnan(dblExciseTaxes), dblTradeTaxes, math.isnan(dblTradeTaxes), dblPropertyTaxes, math.isnan(dblPropertyTaxes), dblOtherTaxes, math.isnan(dblOtherTaxes)))
                                #exit(0)
                            if math.isnan(dblIncomeTaxes)==False and math.isnan(dblVAT)==False and math.isnan(dblExciseTaxes)==False and math.isnan(dblTradeTaxes)==False and math.isnan(dblPropertyTaxes)==False:
                                dblTaxRevenueCalc = dblIncomeTaxes + dblVAT + dblExciseTaxes + dblTradeTaxes + dblPropertyTaxes + dblOtherTaxes
                            else:
                                dblTaxRevenueCalc = math.nan
                        else:
                            dblTaxRevenueCalc = math.nan
                                
                        
                        if k=="Total_Revenue_incl_SC":
                            #print("inside indicator")
                            if lstFinalRow!=None and len(lstFinalRow)>0:
                                #print("inside final row")
                                dblTotalRevenue = lstFinalRow[0].get("Total_Revenue_incl_SC", math.nan)
                                dblTaxRevenue = lstFinalRow[0].get("Tax_Revenue", math.nan)
                                dblNonTaxRevenue = lstFinalRow[0].get("Total_Non_Tax_Revenue", math.nan)
                                
                                if math.isnan(dblTotalRevenue)==False:
                                    dblTotalRevenueCalc = dblTotalRevenue
                                    #print("THen 1")
                                elif math.isnan(dblTotalRevenue)==True and (math.isnan(dblTaxRevenue)==False or math.isnan(dblNonTaxRevenue)==False):
                                    if math.isnan(dblTaxRevenue)==False and math.isnan(dblNonTaxRevenue)==False:
                                        dblTotalRevenueCalc = dblTaxRevenue + dblNonTaxRevenue
                                        #print("Else 1 Then 1")
                                    elif math.isnan(dblTaxRevenue)==False and math.isnan(dblNonTaxRevenue)==True:
                                        dblTotalRevenueCalc = dblTaxRevenue
                                        #print("Else 1 Else 1")
                                    elif math.isnan(dblTaxRevenue)==True and math.isnan(dblNonTaxRevenue)==False:
                                        dblTotalRevenueCalc = dblNonTaxRevenue
                                        #print("Else 1 Else 2")
                                elif math.isnan(dblTotalRevenue)==True and math.isnan(dblTaxRevenue)==True and math.isnan(dblNonTaxRevenue)==True:
                                    dblTotalRevenueCalc = math.nan
                                    #print("Else 2")
                            else:
                                dblTotalRevenueCalc = math.nan
                            dblValue = dblTotalRevenueCalc
                        else:
                            if lstFinalRow!=None and len(lstFinalRow)>0:
                                dblValue = lstFinalRow[0].get(k,math.nan)
                            else:
                                dblValue = math.nan

                        if ((dblValue!="") and (dblValue!=math.nan)):
                            #print("{}-{}-{}\n{}".format(c,j,self.__dictIndicators[k]["name"],lstRow[0][k]))
                            dictRow["value"] = dblValue * intMultiplier
                            #lstDataDict.append(dictRow)
                        else:
                            dictRow["value"] = math.nan

                        if self.__dictIndicators[k]["name"]=="PIT Rate":
                            dblPITRate = dblValue
                        elif self.__dictIndicators[k]["name"]=="Social Contributions - Employer Rate":
                            dblEmployerRate = dblValue
                        elif self.__dictIndicators[k]["name"]=="Social Contributions - Employer Rate":
                            dblEmployeeRate = dblValue
                        elif self.__dictIndicators[k]["name"]=="External Debt":
                            dblExtDebt = dblValue
                        elif self.__dictIndicators[k]["name"]=="General Government Gross Debt":
                            dblGGDebt = dblValue

                        if ((dictRow["indicator name"]=="PIT + Employee Rate + Employer Rate") or (dictRow["indicator name"]=="PIT + Employee Rate") or (dictRow["indicator name"]=="PIT + Employee Rate") or (dictRow["indicator name"]=="Internal Debt")):
                            #print("inside1")
                            if ((dictRow["indicator name"]=="PIT + Employee Rate + Employer Rate") and (dblPITRate!="") and (dblEmployeeRate!="") and (dblEmployerRate!="")):
                                dictRow["value"] = float(dblPITRate) + float(dblEmployeeRate) + float(dblEmployerRate)
                            elif ((dictRow["indicator name"]=="PIT + Employee Rate") and (dblPITRate!="") and (dblEmployeeRate!="")):
                                dictRow["value"] = float(dblPITRate) + float(dblEmployeeRate)
                            elif ((dictRow["indicator name"]=="Internal Debt") and (math.isnan(dblGGDebt)==False) and (math.isnan(dblExtDebt)==False)):
                                dictRow["value"] = float(dblGGDebt) - float(dblExtDebt)
                            elif ((dictRow["indicator name"]=="Internal Debt") and (math.isnan(dblGGDebt)==False) and (math.isnan(dblExtDebt)==True)):
                                dictRow["value"] = float(dblGGDebt)

                        strBuoyancy = self.__dictIndicators[k].get("Buoyancy", "")
                        #print("inside {}".format(strBuoyancy))
                        if ((strBuoyancy != "") and (lstFinalRow!=None)):
                            if (lstFinalRow[0][strBuoyancy] != ""):
                                if lstFinalRow[0][strBuoyancy]!="":
                                    if ((float(lstRow[0][strBuoyancy])>3) or (float(lstRow[0][strBuoyancy])<(-3))):
                                        dictRow["Buoyancy"] = math.nan
                                    else:
                                        dictRow["Buoyancy"] = lstRow[0][strBuoyancy]
                                else:
                                    dictRow["Buoyancy"] = math.nan
                            else:
                                dictRow["Buoyancy"] = math.nan
                        else:
                            dictRow["Buoyancy"] = math.nan

                        strCapacity = self.__dictIndicators[k].get("Capacity", "")
                        #print("inside {}".format(strCapacity))
                        if ((strCapacity != "") and (lstFinalRow!=None)):
                            if (lstFinalRow[0][strCapacity] != ""):
                                if lstFinalRow[0][strCapacity]!="":
                                    dictRow["Capacity"] = lstRow[0][strCapacity]
                                else:
                                    dictRow["Capacity"] = math.nan
                            else:
                                dictRow["Capacity"] = math.nan
                        else:
                            dictRow["Capacity"] = math.nan

                        strGap = self.__dictIndicators[k].get("Gap", "")
                        #print("inside {}".format(strGap))
                        if ((strGap != "") and (lstFinalRow!=None)):
                            if (lstFinalRow[0][strGap] != ""):
                                if lstFinalRow[0][strGap]!="":
                                    dictRow["Gap"] = lstRow[0][strGap]
                                else:
                                    dictRow["Gap"] = math.nan
                            else:
                                dictRow["Gap"] = math.nan
                        else:
                            dictRow["Gap"] = math.nan

                        strTRP = self.__dictIndicators[k].get("Tax Revenue Percent", "")
                        #print("inside {}".format(strTRP))
                        if ((strTRP != "") and (lstFinalRow!=None)):
                            #print("k2:{}, len(lstRow):{}".format(k, len(lstRow)))
                            if (lstFinalRow[0][k] != "") and (dblTaxRevenueCalc != "") and (dblTaxRevenueCalc != 0) and (math.isnan(dblTaxRevenueCalc)==False):
                                dictRow["Tax Revenue Percent"] = (lstFinalRow[0][k] / dblTaxRevenueCalc) * 100
                            else:
                                dictRow["Tax Revenue Percent"] = math.nan
                        else:
                            dictRow["Tax Revenue Percent"] = math.nan

                        lstDataDict.append(dictRow)

                print("{} completed\nTotal {} rows completed\n\n".format(lstFilter[0]["Country_Name"], len(lstDataDict)))
        
            #print(dictRow)
            dfFinal = pd.DataFrame(lstDataDict)
            
            dfFinal.to_csv(self.strDestFileName, sep=',', encoding='utf-8',index=False)

def main():
    try:
        obj = clsTaxRevenueDashboard(paramStrCntryFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Work\\Revenue_Dashboard_v1\\country_code_updated.xls", \
                            paramStrSrcFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Work\\Revenue_Dashboard_v1\\Tax Revenue Analysis STATA\\tax_revenue_14_February_2023.csv", \
                            paramStrDestFileName="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Work\\Revenue_Dashboard_v1\\test.csv", \
                            paramStrRevForgoneFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\work\\RevExp-2Pager\\data\\GTED.xlsx", \
                            paramStrExpensesFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\work\\RevExp-2Pager\\data\\WDI_Expenses.xlsx", \
                            paramStrDebtFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\work\\RevExp-2Pager\\data\\GlobalDebtDatabase.xlsx", \
                            paramStrWBCountriesMapping="c:\\users\\wb584620\\OneDrive - WBG\\Desktop\\work\\common\\data\\wb_countries_mapping.json", \
                            paramStrFiscalSpaceFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Work\\Revenue_Dashboard_v1\\data\\Fiscal-space-data.xlsx", \
                            paramStrGDPComponentsFile="C:\\Users\\wb584620\\OneDrive - WBG\\Desktop\\Work\\Revenue_Dashboard_v1\\data\\GDP_Components.xlsx", \
                            paramStrCntryMetadataSheet="country_code", \
                            paramStrRevForgoneSheet="Rev", \
                            paramStrExpensesSheet="Data", \
                            paramStrDebtSheet="wb_data", \
                            paramStrGGDebtSheet="ggdy", \
                            paramStrExternalDebtSheet="xtdebty", \
                            paramStrFiscalBalanceSheet="fby", \
                            paramStrPrivateSectorConsumptionExpenditureSheet="C", \
                            paramStrGGConsumptionExpenditureSheet="G", \
                            paramStrInvestmentSheet="I", \
                            paramStrExportsSheet="X", \
                            paramStrImportsSheet="M", \
                            paramIntFromYear=1980, paramIntToYear=2022)
        obj.hybridFormat05Jan2023()
    finally:
        obj.displayErrors()


if __name__ == "__main__":
    main()