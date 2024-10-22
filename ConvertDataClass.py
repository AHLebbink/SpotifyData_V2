import os
import pandas as pd


class ConvertData:

    def __init__(self, username, start_year, end_year):
        self.username = username
        self.save_dir_name = 'clean_data'
        self.save_dir = self.save_dir_name + '_' + self.username
        self.range_year = list(range(start_year, end_year+1))

    def create_save_dir(self):
        # make save folders
        if not os.path.isdir(self.save_dir):
            os.mkdir(self.save_dir)

    def convert_data(self, path_rawdata):
        """ Convert raw data (json) to data by year (csv) """

        # Create folder to save the cleaned data in
        self.create_save_dir()

        # Get all JSON file names as a list
        json_file_names = [filename for filename in os.listdir(path_rawdata) if filename.endswith('.json')]

        # Remove video data
        json_file_names = [item for item in json_file_names if 'Video' not in item]

        raw_data = {}
        # Read raw json files
        for json_file_name in json_file_names:
            df = pd.read_json(os.path.join(path_rawdata, json_file_name))
            df = df.fillna('')
            raw_data[json_file_name] = df  # dict = {filename : file content as df}

        # Make df for every year
        for year in self.range_year:
            split_years = []
            for filename, df in raw_data.items():
                # Split date columns
                df[['date', 'time']] = df['ts'].str.split("T", expand=True)
                df[['year', 'month', 'day']] = df['date'].str.split("-", expand=True)

                # Get index of year
                index_year = df.index[df['year'] == str(year)].tolist()
                year_data = df.iloc[index_year]
                split_years.append(year_data)

            # Join split year data into one dataframe (one year gets its own dataframe)
            combined_year_data = pd.concat(split_years, ignore_index=True)
            # combined_year_data.replace(float('nan'), '', inplace=True)

            # Split time into hour minute and seconds
            combined_year_data['time'] = combined_year_data['time'].str.replace('Z', '')
            combined_year_data[['hour', 'minute', 'second']] = combined_year_data['time'].str.split(':', expand=True)

            # Remove track/episode if played for 0 ms
            combined_year_data = combined_year_data.loc[combined_year_data['ms_played'] >= 10000]

            new_filename = 'Streaming_History_Audio_' + str(year) + '.csv'
            combined_year_data.to_csv(os.path.join(self.save_dir, new_filename))

            print('New Data files saved in ' + os.path.join(self.save_dir, new_filename))

        print('end')

    def load_data(self):
        """ Load csv of years as dataframe
        :returns Dictionary = { year : dataframe per year }"""

        csv_filenames = [filename for filename in os.listdir(self.save_dir) if filename.endswith('.csv')]

        data_per_year = {}

        for csv_filename in csv_filenames:
            year = csv_filename.split('_')[-1].split('.')[0]
            if int(year) in self.range_year:
                df = pd.read_csv(self.save_dir + '/' + csv_filename, index_col=0, na_filter=False)
                data_per_year[year] = df

        return data_per_year

    """ Save DataFrame as excel file, with multiple sheets"""

    def dict_df_to_excel(self, d, name):
        path_to_data = 'analysed_data_' + self.username + '/'
        if not os.path.isdir(path_to_data):
            os.mkdir(path_to_data)
        path_to_file = path_to_data + name + '.xlsx'

        with pd.ExcelWriter(path_to_file) as writer:
            for key, df in d.items():
                df.to_excel(writer, sheet_name=str(key), index=False)

        print(name + ' saved in: ' + path_to_data)

    """ Save DataFrame as excel file, with one sheet """

    def df_to_excel(self, df, name):
        path_to_data = 'analysed_data_' + self.username + '/'
        if not os.path.isdir(path_to_data):
            os.mkdir(path_to_data)

        path_to_file = path_to_data + name + '.xlsx'
        df.to_excel(path_to_file, sheet_name=str(name), index=False)
        print(name + ' saved in ' + path_to_data)

    def plt_to_jpg(self, plt, name):
        path_to_data = 'analysed_data_' + self.username + '/'
        if not os.path.isdir(path_to_data):
            os.mkdir(path_to_data)

        path_to_file = path_to_data + name + '.jpg'
        plt.savefig(path_to_file)
        print(name + ' saved in ' + path_to_data)
