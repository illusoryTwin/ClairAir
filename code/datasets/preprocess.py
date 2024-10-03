# code/datasets/preprocess.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder


class Preprocessor:
    def __init__(self):
        self.label_encoder_make = LabelEncoder()
        self.label_encoder_model = LabelEncoder()
        self.label_encoder_vehicle_class = LabelEncoder()
        self.label_encoder_transmission = LabelEncoder()

    def num2cat_transform(self, data: pd.DataFrame):
        data['Make'] = self.label_encoder_make.fit_transform(data['Make'])
        data['Model'] = self.label_encoder_model.fit_transform(data['Model'])
        data['Vehicle_Class'] = self.label_encoder_vehicle_class.fit_transform(data['Vehicle_Class'])
        data['Transmission'] = self.label_encoder_transmission.fit_transform(data['Transmission'])
        return data

    def preprocess_input(self, input_data: pd.DataFrame) -> pd.DataFrame:
        input_data = input_data.copy()  # Create a copy to avoid SettingWithCopyWarning

        # Check if CO2_Emissions exists in the DataFrame
        if 'CO2_Emissions' in input_data.columns:
            co2_emissions_column_exists = True
        else:
            co2_emissions_column_exists = False

        # Rename columns
        input_data.rename(columns={
            'Fuel_Consumption_in_City(L/100 km)': 'Fuel_Consumption_in_City',
            'Fuel_Consumption_in_City_Hwy(L/100 km)': 'Fuel_Consumption_in_City_Hwy',
            'Fuel_Consumption_in_City_comb(L/100 km)': 'Fuel_Consumption_comb'
        }, inplace=True)

        # Select relevant columns, keeping CO2_Emissions if it exists
        relevant_columns = ['Make', 'Model', 'Vehicle_Class', 'Engine_Size', 'Transmission',
                            'Fuel_Consumption_in_City', 'Smog_Level']

        if co2_emissions_column_exists:
            relevant_columns.append('CO2_Emissions')

        input_data = input_data[relevant_columns]

        # Transform categorical variables
        input_data = self.num2cat_transform(input_data)

        return input_data


# class Preprocessor:
#     def __init__(self):
#         self.label_encoder_make = LabelEncoder()
#         self.label_encoder_model = LabelEncoder()
#         self.label_encoder_vehicle_class = LabelEncoder()
#         self.label_encoder_transmission = LabelEncoder()
#
#     def num2cat_transform(self, data: pd.DataFrame):
#         data['Make'] = self.label_encoder_make.fit_transform(data['Make'])
#         data['Model'] = self.label_encoder_model.fit_transform(data['Model'])
#         data['Vehicle_Class'] = self.label_encoder_vehicle_class.fit_transform(data['Vehicle_Class'])
#         data['Transmission'] = self.label_encoder_transmission.fit_transform(data['Transmission'])
#         return data
#
#     def preprocess_input(self, input_data: pd.DataFrame) -> pd.DataFrame:
#         input_data.rename(columns={
#             'Fuel_Consumption_in_City(L/100 km)': 'Fuel_Consumption_in_City',
#             'Fuel_Consumption_in_City_Hwy(L/100 km)': 'Fuel_Consumption_in_City_Hwy',
#             'Fuel_Consumption_in_City_comb(L/100 km)': 'Fuel_Consumption_comb'
#         }, inplace=True)
#
#         input_data = input_data[['Make', 'Model', 'Vehicle_Class', 'Engine_Size',
#                                   'Transmission', 'Fuel_Consumption_in_City', 'Smog_Level']]
#
#         input_data = self.num2cat_transform(input_data)
#
#         return input_data
