import pandas as pd
from statistics import mean, mode
import numpy as np
from quotelog.models import QuoteLogdb as qdb


class QLAnalytics:
    def __init__(self,user_office,ql_model_query):
        self.user_office = user_office
        self.all_ql_model = ql_model_query

    def model_df(self):
        """
            Get all values in db and convert into a dataframe
        """
        # convert to a dataframe
        df = pd.DataFrame.from_records(self.all_ql_model.values())
        return df

    def by_user_office(self):
        """
            # filter data frame by current user office.
        """
        df = self.model_df() # get the whole dateframe
        # print(df)
        if df.empty != True:
            df_by_office = df[ df['office']  == str(self.user_office) ] # filter by office
            # print(df_by_office)
            return df_by_office # return the dataframe by specific office
        elif df.empty == True:
            return df.empty
        else:
            return 'error'      
    
    def val_counts(self):
        # Quotation Status
        Q_S = ['SENT','WON','PENDING','LOST']

        v_counts = {}
        
        # get all data by user office
        df = self.by_user_office()
        if df.empty != True:
            # df['quotation_status'] = df['quotation_status'].str.replace(' ', '')
        
            current_df_qs = list(df["quotation_status"])
            # print(current_df_qs)
            for i in  current_df_qs:
                if i == 'WON':
                    df_won = df[df["quotation_status"] == i]
                    # print(df["quotation_status"])
                    v_counts['FreightModeWonQuotes'] = df_won['freight_mode'].value_counts().idxmax()
                    v_counts['BusinessTypeWonProfits'] = df_won['business_type'].value_counts().idxmax()
                    
                    df_new = df_won[['quarter','percentage_profit']]
                    df_new = df_new.groupby('quarter', as_index=False).sum()
                    v_counts['new_quaters'] = list(df_new['quarter'].values)
                    v_counts['new_profits'] = list(df_new['percentage_profit'].values)

                    dates_taken_to_reply = mode( (df['date_of_reply_to_client'] - df['date_of_reciept_of_request'] ) / np.timedelta64(1, 'D') )
                    v_counts['datesDiff'] = int(dates_taken_to_reply)
                else:
                    v_counts['NoData_won_counts'] = 0

            for i in Q_S:
                if i in current_df_qs:
                    # print(f"values include {i}\n")
                    v_counts[i] = int(df["quotation_status"].value_counts()[i])
                elif i in current_df_qs:
                    v_counts['NoData'] = 0

            return v_counts
        else:
            v_counts['NoData'] = 0

    def sum_office(self):
        df = self.by_user_office()
        # print(df)
        shape = 0
        # shape of data
        if type(df) == bool:
            if df == True:
                # print("is bool")
                return shape
        else:
            if type(df) != bool:
                # print(df)
                new_df = df
                # print(new_df.shape[0])

                _shape = int(new_df.shape[0] + 1)
                if _shape >= 0:
                    return _shape
                else:
                    _shape = 0
                    return _shape


    



       
if __name__ == '__main__':
    df = QLAnalytics('FIT NAIROBI',qdb)
    df.kenya_df()    
        
