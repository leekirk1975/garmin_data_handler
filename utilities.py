


# Create a new df if it does not exist and thereafter append any new data
def df_create_append(df2, dict_data_append, name):
    df2.name = name
    if df2.name in dict_data_append.keys():
        dict_data_append[df2.name] = dict_data_append[df2.name].append(df2)
    elif df2.name not in dict_data_append.keys():
        dict_data_append[df2.name] = df2
    return dict_data_append


# write from a dataframe to CSV
def df_to_csv(directory, csv_df, csv_filename, file_label):  # create csv file

    # Save all data files to a sub directory to aviod cultering
    csvname = directory  + csv_filename + file_label
    csv_df.to_csv(csvname, index=False)