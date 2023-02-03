import pandas as pd

from django.core.files import File

import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

file_path_ = "all_wrld_ports_aiports_.csv"
abs_file_path = os.path.join(script_dir, file_path_)


class Locodes:
    """_summary_
        ## LoCodes 
        - work to get the codes for ports and airports from country code 
        - these are filtered from an excel file containing country codes and UN locodes by that country
        
        0. Get country code from web req. 
        1. Create a dataframe of the file: load_data() 
        2. Filter the df by country only and return frame column values of locodes: by_country()        
    """
    def __init__(self,country):
        self.country = country
    
    def load_data(self):
        df = pd.read_csv(abs_file_path)
        return df 
    
    def by_country(self):
        df = self.load_data()
        new_df = df[df['country'] == self.country]

        return new_df['refcode'].values

# print( list(Locodes('US').by_country()) )
class Management:
    """ _summary_
        # Data for managemt
        # Get overview of all data from all country branches.
        
        1. Creates a dataframe of the whole db 
    """
    def __init__(self,designation,ql_model_query):
        self.designation = designation
        self.ql_model_query = ql_model_query
        
        # Constants to be used all accross the code.
        self.ofcs =  ['FIT NAIROBI','FIT UGANDA','FIT TANZANIA','FIT RWANDA','FIT ETHIOPIA','FIT SUDAN','FIT DJIBOUTI']
        self.Q_S = ['SENT','WON','PENDING','LOST']
        self.business_type = ['AGENT','NEW CUSTOMER','EXISTING CUSTOMER']
        self.products = []
        self.request_type = []

    def management_data(self):
        # if self.designation == 'MANAGEMENT':
        df = pd.DataFrame.from_records(self.ql_model_query.values())
        return df
    
    def basic_counts(self):
        """
            # WON LOST PENDING ...
        """
        df = self.management_data()
        # Get all offices
        offices = list(pd.unique(df['office'])) # offices from the db 9
        q_s = list(pd.unique(df['quotation_status']))
        
        basic_counts_by_office = {}
        current_df_qs = list(df["quotation_status"])
        
        for a in offices:
            if a in self.ofcs:
                new_df = df[df['office'] == a]
                basic_counts_by_office[a] = {
                    a:b for a,b in zip(self.Q_S, new_df["quotation_status"].value_counts()) 
                }
                
        return basic_counts_by_office
        
    def management_count(self):
        """
            # same basic counts but for all offices...
        """
        df = self.management_data()
        
        # Get all offices
        offices = list(pd.unique(df['office']))
        # Get all years
        freight_mode_counts = {}
        business_type_counts = {}
        quotation_status_counts = {}
        
        # Quotation Status        
        for i in offices:
            if i in self.ofcs:
                new_df = df[df['office'] == i]
                freight_mode_counts[i] = new_df['freight_mode'].value_counts().idxmax()
                business_type_counts[i] = new_df['business_type'].value_counts().idxmax()
            
        return freight_mode_counts,business_type_counts
    
    def yrs_products(self):
        df = self.management_data()
        # convert created_on to date
        count_val_all_quotes = df.shape[0]
        df['created_on'] = pd.to_datetime(df['created_on']).dt.year
        # Get all won quotes
        df = df[(df['quotation_status'] == 'WON')]
        # create new frame
        new_df = df[['created_on','freight_mode','request_type','business_type']]
        
        return new_df,count_val_all_quotes
    
    def sum_win_ratio_by_yrs(self):
        """
            # Get win ratios by:
                -   YEAR	% WIN RATIO
                    2019	 34%
                    2020	 35%
        """
        tot_wr = {
            'years':[],
            'ratios':[]
        } # total win ratio
        new_df,count_val_all_quotes = self.yrs_products()
        yrs = list(pd.unique(new_df['created_on']))
        # End result should look like: {"years":[2019,2020],"ratios":[10,35]}
        count_val_won_quotes = new_df.shape[0]
        # Quotation Status 
        tot_wr['years'] = list(pd.unique(new_df['created_on']))
        for i in tot_wr['years']:
            shape_ = new_df[new_df['created_on'] == i]
            ratio_new = round((shape_.shape[0] / count_val_all_quotes),2)
            tot_wr['ratios'] += [ratio_new]

        return tot_wr
                
    def product_wr_by_yrs(self):
        """
            # Get win ratios by:
                - PRODUCT	    2019	2020	2021
                    AIRFREIGHT	34%	    23%	    15%
                    SEAFREIGHT	11%	    34%	    61%
                    ROADFREIGHT	91%	    54%	    51%
                    WAREHOUSING ......
        """
        # new_df,count_val_all_quotes = self.yrs_products() # new dataframe and count of all quotes.
        # new_df = new_df[['created_on','freight_mode']]  
        # final product 
        # print(new_df)
    
    def business_type_wr_by_yrs(self):
        """
            # Get win ratios by:
                - BUSINESS TYPE	    2019	2020	2021
                    ExistingClient	34%	     23%	15%
                    New Client	    11%	     34%	61%
                    Agents	        11%	     54%	61%
        """
        # print(self.business_type)
        new_df,count_val_all_quotes = self.yrs_products()
        new_df = new_df[['created_on','business_type']]
        # For every value in business type
        btype_wr = {}

        yrz = sorted(list(pd.unique(new_df['created_on']))) 
        # print(yrz)
        new_df['business_type'] = new_df['business_type']
        for i in self.business_type:
            btype_wr[i] = {
                'year': [],
                'ratio':[]
            }
            for y in yrz:
                df_main = new_df[(new_df['business_type'] == i) & (new_df['created_on'] == y) ]
                yr = list(pd.unique(df_main['created_on'].astype("string")))
                ratio_new = str(round((df_main.shape[0] / count_val_all_quotes),2))
                
                btype_wr[i]['year'] += yr
                btype_wr[i]['ratio'] += [ratio_new]    
             
     
        return (btype_wr)

    
    def request_type_wr_by_yrs(self):
        """
            # Get win ratios by:
                -REQUEST TYPE	    2019	2020	2021
                    IMPORTS	         34%	23%	    15%
                    EXPORTS	         11%	34%	    61%
                    TRANSSHIPMENT	 11%	54%	    67%
                    WAREHOUSING	     11%	54%	    61%
                    LOCAL	         11%	54%	    61%
        """
        
        # df = self.management_data()
        # new_df = df[['created_on','absolute_profit','request_type']]
        
        pass
    
        