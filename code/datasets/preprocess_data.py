import pandas as pd
from sklearn.impute import SimpleImputer
from code.datasets.preprocess import Preprocessor
from sklearn.model_selection import train_test_split
import pandas as pd
# from sklearn.preprocessing import LabelEncoder

# INITIAL VERSION
# class Preprocessor:
#     def __init__(self):
#         self.label_encoder_make = LabelEncoder()
#         self.label_encoder_model = LabelEncoder()
#         self.label_encoder_vehicle_class = LabelEncoder()
#         self.label_encoder_transmission = LabelEncoder()

#     def num2cat_transform(self, data: pd.DataFrame):
#         data['Make'] = self.label_encoder_make.fit_transform(data['Make'])
#         data['Model'] = self.label_encoder_model.fit_transform(data['Model'])
#         data['Vehicle_Class'] = self.label_encoder_vehicle_class.fit_transform(data['Vehicle_Class'])
#         data['Transmission'] = self.label_encoder_transmission.fit_transform(data['Transmission'])
#         return data

#     def preprocess_input(self, input_data: pd.DataFrame) -> pd.DataFrame:
#         input_data = input_data.copy()  # Create a copy to avoid SettingWithCopyWarning
#         input_data.rename(columns={
#             'Fuel_Consumption_in_City(L/100 km)': 'Fuel_Consumption_in_City',
#             'Fuel_Consumption_in_City_Hwy(L/100 km)': 'Fuel_Consumption_in_City_Hwy',
#             'Fuel_Consumption_in_City_comb(L/100 km)': 'Fuel_Consumption_comb'
#         }, inplace=True)

#         input_data = input_data[['Make', 'Model', 'Vehicle_Class', 'Engine_Size',
#                                   'Transmission', 'Fuel_Consumption_in_City', 'Smog_Level']]

#         input_data = self.num2cat_transform(input_data)

#         return input_data


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
#         input_data = input_data.copy()  # Create a copy to avoid SettingWithCopyWarning
#
#         # Check if CO2_Emissions exists in the DataFrame
#         if 'CO2_Emissions' in input_data.columns:
#             co2_emissions_column_exists = True
#         else:
#             co2_emissions_column_exists = False
#
#         # Rename columns
#         input_data.rename(columns={
#             'Fuel_Consumption_in_City(L/100 km)': 'Fuel_Consumption_in_City',
#             'Fuel_Consumption_in_City_Hwy(L/100 km)': 'Fuel_Consumption_in_City_Hwy',
#             'Fuel_Consumption_in_City_comb(L/100 km)': 'Fuel_Consumption_comb'
#         }, inplace=True)
#
#         # Select relevant columns, keeping CO2_Emissions if it exists
#         relevant_columns = ['Make', 'Model', 'Vehicle_Class', 'Engine_Size', 'Transmission',
#                             'Fuel_Consumption_in_City', 'Smog_Level']
#
#         if co2_emissions_column_exists:
#             relevant_columns.append('CO2_Emissions')
#
#         input_data = input_data[relevant_columns]
#
#         # Transform categorical variables
#         input_data = self.num2cat_transform(input_data)
#
#         return input_data
#
    
def load_data(file_path):
    return pd.read_csv(file_path)


def clean_data(data):
    # Check some missing values in the dataset
    missing_values = data.isnull().sum()
    print("Missing values before imputation:\n", missing_values)

    # Separate numeric and categorical columns
    numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = data.select_dtypes(include=['object']).columns

    # Impute missing values for numeric columns
    numeric_imputer = SimpleImputer(strategy='mean')  # Use median if preferred
    data[numeric_cols] = numeric_imputer.fit_transform(data[numeric_cols])

    # Impute missing values for categorical columns
    categorical_imputer = SimpleImputer(strategy='most_frequent')
    data[categorical_cols] = categorical_imputer.fit_transform(data[categorical_cols])

    # Check again for missing values
    missing_values_after = data.isnull().sum()
    print("Missing values after imputation:\n", missing_values_after)
    
    
    # Remove the outliers (using Z-score)
    z_scores = (data[numeric_cols] - data[numeric_cols].mean()) / data[numeric_cols].std()
    print("Z-scores:\n", z_scores)

    outlier_mask = (z_scores > 3).any(axis=1)
    print("Number of outliers detected:", outlier_mask.sum())
    print("Number of rows before filtering:", len(data))

    # Filter the data to remove outliers
    data = data[~outlier_mask]
    print("Data after removing outliers:\n", data)

    return data

def preprocess_data(data):
    preprocessor = Preprocessor()
    preprocessed_data = preprocessor.preprocess_input(data)
    return preprocessed_data


def split_data(data, preprocessed_data_path):
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    train_data.to_csv(preprocessed_data_path + 'train_data.csv', index=False)
    test_data.to_csv(preprocessed_data_path + 'test_data.csv', index=False)


if __name__ == '__main__':
    data = load_data('data/raw/CO2_emission.csv')
    cleaned_data = clean_data(data)
    # cleaned_data
    preprocessed_data = preprocess_data(cleaned_data)  
    # print(preprocessed_data)
    preprocessed_data_path = 'data/preprocessed/'
    split_data(preprocessed_data, preprocessed_data_path)