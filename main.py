from ConvertDataClass import ConvertData
from AnalyseDataClass import AnalyseData

if __name__ == '__main__':
    username = 'Anna'
    start_year = 2016
    end_year = 2024
    convert = False
    save = True
    spotify_data_folder = 'Spotify Extended Streaming History'

    cd = ConvertData(username, start_year, end_year)

    """ CONVERT & LOAD DATA """
    # Convert raw json data to csv data separated by year
    if convert:
        cd.convert_data(spotify_data_folder)

    # Load csv data as dataframes
    data_per_year = cd.load_data()

    """ ANALYSE DATA """
    ad = AnalyseData(username, data_per_year, save, start_year, end_year)

    """ TOP PER YEAR """
    top_tracks = ad.get_top_tracks_per_year()
    top_albums = ad.get_top_albums_per_year()
    top_artists = ad.get_top_artists_per_year()

    top_episodes = ad.get_top_episodes_per_year()
    top_podcasts = ad.get_top_podcasts_per_year()

    """ UNIQUE PER YEAR """
    unique_songs_per_year, total_unique_songs = ad.get_unique_songs_per_year()
    unique_artists_per_year, total_unique_artists = ad.get_unique_artists_per_year()

    unique_episodes_per_year, total_unique_episodes = ad.get_unique_episodes_per_year()
    unique_podcasts_per_year, total_unique_shows = ad.get_unique_podcasts_per_year()

    """ MINUTES PER YEAR """
    minutes_per_year = ad.get_minutes_per_year()

    """ PLOT """
    ad.plot_time_of_day_listened_per_year()
