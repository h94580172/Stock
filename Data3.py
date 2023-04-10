import pandas as pd

def merge_excel_files(file1, file2, output_file):
    # Read in the two Excel files
    stock_data = pd.read_excel(file1, sheet_name=None)
    stock_data2 = pd.read_excel(file2, sheet_name=None)

    # Create a writer object to write to a single Excel file
    with pd.ExcelWriter(output_file) as writer:
        # Separate the dataframes by sheet
        for sheet_name, df in stock_data.items():
            # Merge the two dataframes on the 'date' and 'stock_id' columns
            merged_df = pd.merge(df, stock_data2[sheet_name], on=['date', 'stock_id'])

            # Add the 'value' columns together
            merged_df['value'] = merged_df['value_x'] + merged_df['value_y']

            # Drop the 'value_x' and 'value_y' columns
            merged_df.drop(['value_x', 'value_y'], axis=1, inplace=True)

            # Write the merged dataframe to the Excel writer object
            merged_df.to_excel(writer, sheet_name=sheet_name, index=False)

merge_excel_files('stock_data.xlsx', 'stock_buy_sell.xlsx', 'stock_merged_data.xlsx')

