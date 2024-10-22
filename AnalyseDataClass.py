import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ConvertDataClass import ConvertData

def _get_minutes(df, column):
    return round(df[column].sum() / 1000 / 60)


def calculate_time_statistics(data_per_year, uri):
    minutes = []
    hours = []
    days = []
    years = []

    for year, dpy in data_per_year.items():
        if uri:
            dpy = dpy.loc[dpy[uri] != '']
            # dpy = dpy.dropna(subset=[uri])
        ms = dpy['ms_played'].sum()
        minute = ms / 1000 / 60
        hour = minute / 60
        day = hour / 24

        minutes.append(round(minute))
        hours.append(round(hour))
        days.append(round(day))
        years.append(year)

    return pd.DataFrame(list(zip(years, minutes, hours, days)),
                        columns=['Year', 'Minutes', 'Hours', 'Days'])


class AnalyseData:
    def __init__(self, username, data_per_year, save, start_year, end_year):
        self.username = username
        self.data_per_year = data_per_year
        self.save = save

        self.cd = ConvertData(self.username, start_year, end_year)

    """ TRACK - ALBUM - ARTIST """

    def get_top_tracks_per_year(self):
        """ Get the tracks sorted by frequency of times listened per year """

        column = 'master_metadata_track_name'
        top = 'track'
        top_tracks_per_year = {}
        for year, dpy in self.data_per_year.items():
            dpy = dpy.loc[dpy[column] != '']
            df_freq = dpy.value_counts(column).to_frame().reset_index(names=top)
            minutes = [_get_minutes(dpy[dpy[column] == item], 'ms_played') for item in df_freq[top]]
            artist = [dpy['master_metadata_album_artist_name'][dpy.index[dpy[column] == item].tolist()[0]] for item in
                      df_freq[top]]
            albums = [dpy['master_metadata_album_album_name'][dpy.index[dpy[column] == item].tolist()[0]] for item in
                      df_freq[top]]

            df_freq['minutes'] = minutes
            df_freq['artist'] = artist
            df_freq['album'] = albums

            top_tracks_per_year[year] = df_freq

        if self.save:
            self.cd.dict_df_to_excel(d=top_tracks_per_year, name=f'top_{top}s_per_year')
        else:
            print(f'top_{top}_per_year' + ' generated without saving')

        return top_tracks_per_year

    def get_top_albums_per_year(self):
        """ Get the albums sorted by frequency of times listened per year """

        column = 'master_metadata_album_album_name'
        top = 'album'
        top_albums_per_year = {}

        for year, dpy in self.data_per_year.items():
            dpy = dpy.loc[dpy[column] != '']
            df_freq = dpy.value_counts(column).to_frame().reset_index(names=top)
            minutes = [_get_minutes(dpy[dpy[column] == item], 'ms_played') for item in df_freq[top]]
            artist = [dpy['master_metadata_album_artist_name'][dpy.index[dpy[column] == item].tolist()[0]] for item in
                      df_freq[top]]

            df_freq['minutes'] = minutes
            df_freq['artist'] = artist

            top_albums_per_year[year] = df_freq

        if self.save:
            self.cd.dict_df_to_excel(d=top_albums_per_year, name=f'top_{top}s_per_year')
        else:
            print(f'top_{top}_per_year' + ' generated without saving')

        return top_albums_per_year

    def get_top_artists_per_year(self):
        """ The artists sorted by frequency of times listened per year + number of unique songs per artist """
        column = 'master_metadata_album_artist_name'
        top = 'artist'
        top_artists_per_year = {}
        for year, dpy in self.data_per_year.items():
            dpy = dpy.loc[dpy[column] != '']
            freq = dpy.value_counts(column).to_frame().reset_index(names=top)
            minutes = [_get_minutes(dpy[dpy[column] == item], 'ms_played') for item in freq[top]]
            track = [len(dpy[dpy[column] == item]['master_metadata_track_name'].unique()) for item in freq[top]]

            freq['minutes'] = minutes
            freq['# songs'] = track

            top_artists_per_year[year] = freq

        if self.save:
            self.cd.dict_df_to_excel(d=top_artists_per_year, name=f'top_{top}s_per_year')
        else:
            print(f'top_{top}_per_year' + ' generated without saving')

        return top_artists_per_year

    """ EPISODE - PODCAST """

    def get_top_episodes_per_year(self):
        column = 'episode_name'
        top = 'episode'
        top_episodes_per_year = {}
        for year, dpy in self.data_per_year.items():
            dpy = dpy.loc[dpy[column] != '']
            freq = dpy.value_counts(column).to_frame().reset_index(names=top)
            minutes = [_get_minutes(dpy[dpy[column] == item], 'ms_played') for item in freq[top]]
            podcast = [dpy['episode_show_name'][dpy.index[dpy[column] == item].tolist()[0]] for item in freq[top]]

            freq['minutes'] = minutes
            freq['podcast'] = podcast

            top_episodes_per_year[year] = freq

        if self.save:
            self.cd.dict_df_to_excel(d=top_episodes_per_year, name=f'top_{top}s_per_year')
        else:
            print(f'top_{top}_per_year' + ' generated without saving')

        return top_episodes_per_year

    def get_top_podcasts_per_year(self):
        column = 'episode_show_name'
        top = 'podcast'
        top_podcasts_per_year = {}
        for year, dpy in self.data_per_year.items():
            dpy = dpy.loc[dpy[column] != '']
            freq = dpy.value_counts(column).to_frame().reset_index(names=top)
            minutes = [_get_minutes(dpy[dpy[column] == item], 'ms_played') for item in freq[top]]
            episodes = [len(dpy[dpy[column] == item]['episode_name'].unique()) for item in freq[top]]

            freq['minutes'] = minutes
            freq['# episodes'] = episodes

            top_podcasts_per_year[year] = freq

        if self.save:
            self.cd.dict_df_to_excel(d=top_podcasts_per_year, name=f'top_{top}s_per_year')
        else:
            print(f'top_{top}_per_year' + ' generated without saving')

        return top_podcasts_per_year

    """ UNIQUE PER YEAR """

    def _get_unique_items_per_year(self, column, top):
        unique_items = []
        total_unique_items = []
        years = []

        for year, dpy in self.data_per_year.items():
            items = dpy[column].unique()
            total_unique_items.append(items)
            unique_items.append(len(items))
            years.append(year)

        unique_items_per_year = pd.DataFrame(list(zip(years, unique_items)), columns=['Year', f'# {top}s'])
        total_number_unique_items = len(pd.Series(np.concatenate(total_unique_items)).unique())
        unique_items_per_year.loc[len(unique_items_per_year)] = ['Total', total_number_unique_items]

        if self.save:
            self.cd.df_to_excel(unique_items_per_year, f'unique_{top}s_per_year')
        else:
            print(f'unique_{top}s_per_year' + ' generated without saving')

        return unique_items_per_year, total_number_unique_items

    """ Unique Songs - Artists """

    def get_unique_songs_per_year(self):
        return self._get_unique_items_per_year('master_metadata_track_name', 'Song')

    def get_unique_artists_per_year(self):
        return self._get_unique_items_per_year('master_metadata_album_artist_name', 'Artist')

    """ Unique Episodes - Podcasts """

    def get_unique_episodes_per_year(self):
        return self._get_unique_items_per_year('episode_name', 'Episode')

    def get_unique_podcasts_per_year(self):
        return self._get_unique_items_per_year('episode_show_name', 'Podcast')

    """ MINUTES PER YEAR """

    def get_minutes_per_year(self):
        # Combine episode, track, and total data
        minutes_per_year = {'Total': calculate_time_statistics(self.data_per_year, None),
                            'Tracks': calculate_time_statistics(self.data_per_year, 'spotify_track_uri'),
                            'Episodes': calculate_time_statistics(self.data_per_year, 'spotify_episode_uri')}

        if self.save:
            self.cd.dict_df_to_excel(minutes_per_year, 'minutes_per_year')
        else:
            print(f'minutes_per_year' + ' generated without saving')

        return minutes_per_year

    """ Plot hour average per year """

    def plot_time_of_day_listened_per_year(self):
        for year, dpy in self.data_per_year.items():
            unique_days_per_year = dpy['date'].unique().tolist()
            minutes_per_day_per_year = []

            for day in unique_days_per_year:
                df_day = dpy.loc[dpy['date'] == day]

                minutes = {'Date': day}
                for h in range(0, 24):
                    i_hour = df_day.loc[df_day['hour'] == h]
                    if len(i_hour) == 0:
                        minute = 0
                    else:
                        try:
                            sum_hour = i_hour['ms_played'].sum()
                            minute = round(sum_hour / 1000 / 60)
                        except Exception as e:
                            print(e)
                            print(day, h)
                            minute = 0

                    minutes[h] = minute

                minutes_per_day_per_year.append(minutes)

            df_minutes_per_day_per_year = pd.DataFrame.from_dict(minutes_per_day_per_year)

            means = df_minutes_per_day_per_year.drop('Date', axis=1).mean(axis=0).to_dict()

            courses = list(means.keys())
            values = list(means.values())

            hourticks = list(range(0, 61, 5))

            plt.figure(figsize=(10, 7))
            plt.grid(axis='y')
            plt.bar(courses, values, color='maroon', width=0.6, zorder=2)

            plt.xlabel("Hour of the day")
            plt.xticks(courses, courses)
            plt.ylabel("Average minutes")
            plt.yticks(hourticks)
            plt.title(f"Average minutes listened per hour {year}")

            if self.save:
                self.cd.plt_to_jpg(plt, f'minutes_listened_per_hour_{year}')
            else:
                print(f'minutes_listened_per_hour_{year} plot' + '   generated without saving')

            plt.show()
