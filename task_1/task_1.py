# https://api.themoviedb.org
# As of December 16, 2019, we have disabled the original API rate
# limiting (40 requests every 10 seconds.) If you have any questions about this,
# please head over to our API support forum.
#
# While our legacy rate limits have been disabled for some time, we do still have some upper
# limits to help mitigate needlessly high bulk scraping. They sit somewhere in the 50 requests per second range.
# This limit could change at any time so be respectful of the service we have built
# and respect the 429 if you receive one.
import csv
import json
import time

import requests
from pprint import pprint
from datetime import datetime


# You write some data preparation tool which will be used for building diagrams.
# Prepare a class which will grab some movie data from themoviedb by a URL template:
# https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={!!!}
# Information about genres could be fetched by a
#
# URL: https://api.themoviedb.org/3/genre/movie/list?language=en
# You must remember about authentication. Apply headers:
# {
#     "accept": "application/json",
#     "Authorization": "Bearer {your token}"
# }

import os
import copy
from datetime import datetime
from dateutil.relativedelta import relativedelta


class GrabData:

    def __init__(self, return_number_of_pages=None):
        self.page_count = return_number_of_pages if return_number_of_pages else self.__input_numder_page()
        self.url = 'https://api.themoviedb.org/3/discover/movie?include_adult1=false' \
                   '&include_video=false&sort_by=popularity.desc&page={}'
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNk"
                             "OTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZ"
                             "CJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
        }
        self.full_data = []
        self.filtered_list = []
        self.top_list_from_genre = []
        self.collection_of_present_genres = ()
        self.collection_movie_grouped_by_genre = ()
        self.restructured_movies_list = []
        self.csv_out_file_name_fulldata = ''
        self.csv_out_file_name_fulldata_default = 'out_full_data.csv'
        self.csv_out_file_name_each_4 = ''
        self.csv_out_file_name_each_4_default = 'out_each_4_move.csv'

        self.__request()

    @staticmethod
    def __input_numder_page():
        i = 0
        while i < 10:
            user_input = input('How many page download(max 500): ')
            try:
                n = int(user_input)
            except ValueError:
                print("Bad input.\nPlease enter a valid integer.")
                i += 1
            else:
                return n
        print('Too many input errors\n------ Good by. ------')
        exit()

    def __request(self):
        # comeback count of need pages (self.page_count)
        self.full_data.clear()
        i = 1
        while i <= self.page_count:
            response = requests.get(url=self.url.format(i), headers=self.headers)
            try:
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print("An error occurred:", e)
                if response.status_code == 422:
                    print(f'Error: page number {i} not present.')
                elif response.status_code == 429:
                    print(
                        f'response=429\nYour request count ({i}) '
                        'is over the allowed limit of (40) per second.\nPlease wait 10s.')
                    time.sleep(10)
                    continue
                elif response.status_code == 404:
                    print('Error HTTP: Page not found.')
                break
            else:
                print(i)
                i += 1
                for film in response.json()["results"]:
                    self.full_data.append(film)

    def validate_path(self, f_path):
        file_path = os.path.dirname(f_path)
        file_name = os.path.basename(f_path)

        if file_path:
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_path += '\\'

        return file_path, file_name

    def __add_file_extention(self, name):
        f_name = name if (name.find('.csv', -4)) != -1 else name + '.csv'
        return f_name


    # 2.	Give a user all data
    def get_full_data(self, f_name=None):  # Give a user all data

        if not f_name:
            self.csv_out_file_name_fulldata = self.csv_out_file_name_fulldata_default
        else:
            file_path, file_name = self.validate_path(f_name)
            self.csv_out_file_name_fulldata = file_path + self.__add_file_extention(file_name)

        with open(self.csv_out_file_name_fulldata, mode='w', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=dict(self.full_data[0]).keys())
            writer.writeheader()
            writer.writerows([data for data in self.full_data])

        return self.full_data

    # 3.	All data about movies with indexes from 3 till 19 with step 4
    def get_each_4_move(self, f_name=None):  # All data about movies with indexes from 3 till 19 with step 4f_name=''
        if not f_name:
            self.csv_out_file_name_each_4 = self.csv_out_file_name_each_4_default
        else:
            file_path, file_name = self.validate_path(f_name)
            self.csv_out_file_name_each_4 = file_path +  self.__add_file_extention(f_name)

        with open(self.csv_out_file_name_each_4, mode='w', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=dict(self.full_data[0]).keys())
            writer.writeheader()
            writer.writerows([data for data in self.full_data[3:19:4]])

        return [data for data in self.full_data[3:19:4]]

    # 4.	Name of the most popular title
    def get_max_popularity_title(self):  # 4. Name of the most popular title
        movie = max(self.full_data, key=lambda val: val['popularity'])
        return movie['title']

    # 5. Names of titles which has in description key words which a user put as parameters
    def find_in_description(self, find_str):
        return [item['title'] for item in self.full_data if item['overview'].find(find_str) != -1]

    # 6.	Unique collection of present genres (the collection should not allow inserts)
    def get_present_genres(self):  # 6. Unique collection of present genres (the collection should not allow inserts)
        self.collection_of_present_genres = tuple(
            sorted(set([genre_id for item in self.full_data for genre_id in item['genre_ids']])))
        return self.collection_of_present_genres

    # 7.	Delete all movies with user provided gnere
    def delete_movies_with_genre(self, list_id=''):  # 7. Delete all movies with user provided genre
        list_id = input('Delete genre separete with ",": ') if not list_id else list_id
        list_id = set(list_id.split(','))

        rows_to_delete = []
        for del_genre_id in list_id:
            [rows_to_delete.append(idx) for idx in range(len(self.full_data))
             if int(del_genre_id) in self.full_data[idx]['genre_ids']]

        rows_to_delete = sorted(set(rows_to_delete), reverse=True)
        self.filtered_list = [self.full_data[i] for i in range(len(self.full_data)) if i not in rows_to_delete]

        return f'7. Deleted {len(rows_to_delete)} movies with genre {list_id} and update filtered_list'

    # 8.?	Names of most popular genres with numbers of time they appear in the data
    def top_movie_from_genre(self):
        self.top_list_from_genre.clear()

        for genre_id in self.collection_of_present_genres:
            temp = [movie for movie in self.full_data if genre_id in movie['genre_ids']]
            top_movie = (max(temp, key=lambda item: item['popularity']))
            self.top_list_from_genre.append([top_movie['title'], top_movie['release_date'], genre_id])

        return self.top_list_from_genre

    # 9.	Collection of film titles grouped in pairs by common genres (the groups should not allow inserts)
    def get_collection_movie_grouped_by_genre(self):
        grouping_movie = []
        for genre in self.collection_of_present_genres:
            grouping_movie.append([genre, [movie['title'] for movie in self.full_data if genre in movie['genre_ids']]])
        self.collection_movie_grouped_by_genre = tuple(grouping_movie)

        return self.collection_movie_grouped_by_genre

    # 10.	Return initial data and copy of initial data where first id in list of film genres was replaced with 22
    def replace_first_genre(self):
        full_data_with_replace_genre = copy.deepcopy(self.full_data)
        for movie in full_data_with_replace_genre:
            movie['genre_ids'][0] = 22
        return self.full_data, full_data_with_replace_genre

    # 11.	Collection of structures with part of initial data which has the following fields:
    # •	Title
    # •	Popularity (with 1 decimal point with maximum precision)
    # •	Score (vote_average without fractional part)
    # •	Last_day_in_cinema (2 months and 2 weeks after the release_date)
    # Collection should be sorted by score and popularity
    def restruct_data(self):
        self.restructured_movies_list = [{
            'Title': movie['title'],
            'Popularity': round(movie['popularity'], 1),
            'Score': int(movie['vote_average']),
            'Last_day_in_cinema': (datetime.strptime(movie['release_date'], '%Y-%m-%d') +
                                   relativedelta(months=2, weeks=2)).strftime('%Y-%m-%d')
        } for movie in self.full_data]
        return self.restructured_movies_list


    # 12.	Write information from previous step to a csv file using path provided by user
    def save_collection_new_fields(self):

        while(True):
            f_name = input('Enter path/name file: ')
            if f_name:
                break

        file_path, file_name = self.validate_path(f_name)
        f_name = file_path +  self.__add_file_extention(f_name)

        with open(f_name, mode='w', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=dict(self.restructured_movies_list[0]).keys())
            writer.writeheader()
            writer.writerows([data for data in self.restructured_movies_list])


def main():

    # 1.	Fetch the data from desired amount of pages
    # quantity page or NONE to input from keyboard
    m = GrabData()  # it generates follow-up queries and adds all responses.json()["results"] to the list full_data
    print('1. get data from server.')
    # pprint(m.full_data[0])

    # 2.	Give a user all data
    # m.get_full_data(r"d:\test\full_data")
    # m.get_full_data(r"..\test\test")
    m.get_full_data()  # input fileName or none for default fileName
    print(f'2. All data exported in {m.csv_out_file_name_fulldata}')

    # 3.	All data about movies with indexes from 3 till 19 with step 4
    m.get_each_4_move()  # input fileName or none for default fileName
    print(f'3. All data about movies with indexes from 3 till 19 with step 4 exported in {m.csv_out_file_name_each_4}')

    # 4.	Name of the most popular title
    print(f'4. Name of the most popular title - {m.get_max_popularity_title()}')

    # 5.	Names of titles which has in description key words which a user put as parameters
    find_txt = input("Find in description: ")
    print(f'5. Names of titles which has in description key words which a user put as parameters = {find_txt} \n'
          f'movie list:\n{m.find_in_description(find_txt)}')

    # 6. Unique collection of present genres (the collection should not allow inserts)
    print(f'6. Unique collection of present genres - {m.get_present_genres()}')

    # 7.	Delete all movies with user provided genre
    print(m.delete_movies_with_genre('12, 16'))  # or NONE if need input from keybord

    # 8.	Names of most popular genres with numbers of time they appear in the data
    print('8. Names of most popular genres:')
    pprint(m.top_movie_from_genre())

    # 9.	Collection of film titles grouped in pairs by common genres (the groups should not allow inserts)
    print('9. Collection of film titles grouped in pairs by common genres')
    pprint(m.get_collection_movie_grouped_by_genre())

    # 10.	Return initial data and copy of initial data where first id in list of film genres was replaced with 22
    print('10. Origin data and edited copy origin')
    origin, copy_origin = m.replace_first_genre()
    pprint(origin[0])
    pprint(copy_origin[0])

    # 11.	Collection of structures with part of initial data which has the following fields:
    # •	Title
    # •	Popularity (with 1 decimal point with maximum precision)
    # •	Score (vote_average without fractional part)
    # •	Last_day_in_cinema (2 months and 2 weeks after the release_date)
    # Collection should be sorted by score and popularity
    print('11. Collection with new fields')
    pprint(m.restruct_data()[0])

    # 12.	Write information from previous step to a csv file using path provided by user
    m.save_collection_new_fields()


if __name__ == '__main__':
    main()
