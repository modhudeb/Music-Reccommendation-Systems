import numpy as np
import pandas as pd


class GetHand :
    
    """
    This class will help you to preprocess and manipulate your dataset
    """

    # custom function to clean artist column's data
    def cleanString(string : str):
        """
        Custom function to clean column's string data. Can be used in pd.DataFrame.apply()
        """
        string = string.strip("['']")
        string = string.split("'")
        for x in string :
            if ", " in string:
                string.remove(", ")
        return (',').join(string)
    

    # custom function to find a value
    def isExist(tdf:pd.DataFrame ,string:str, columns:list=['name', 'artists']) -> pd.DataFrame:
        """
        Custom function to find a value in a dataframe's column\n
        If the string exists in the dataset, then it will return a dataframe that corresponds the value.\n
        else it will return 'None'
        """
        string = string.lower()
        stringList = string.split(" by ")
        # print(stringList)

        if len(stringList) == 1:
            temp = tdf[tdf[columns[0]].str.startswith(stringList[0])]
            if len(temp)==0:
                return None
            else :
                return temp

        else : 
            x = tdf[columns[0]].str.startswith(stringList[0])
            y = tdf[columns[1]].str.contains(stringList[len(stringList)-1])
            temp = tdf[x & y]
            if len(temp)==0:
                return None
            else :
                return temp



    def firstValueOf(df:pd.DataFrame, column:str):
        val = df[column][0:1].ravel()[0]
        if type(val) == str:
            val = val.split(",")
            return val[0]
        else :
            return val