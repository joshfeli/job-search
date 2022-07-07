# start with the imports
import pandas as pd
import random
import requests
import json
import pprint
import sqlalchemy as db
import pdb
from sqlalchemy.types import String

def print_func(query):
    df = pd.DataFrame(query)
    df.columns = ['user_id', 'title', 'company_name', 'location', 'via', 'description', 'job_id', 'detected_extensions.posted_at', 'detected_extensions.schedule_type']
    pprint.pprint(df)

def user_check(user_name):
    if user_name == None:
        return False
    names = user_name.split('_')
    if len(names) != 2:
        print("Invalid firstname_lastname")
        return False
    for name in names:
        for letter in name:
            if not ('a' <= letter <= 'z') and not ('A' <= letter <= 'Z'):
                print("Invalid firstname_lastname")
                return False
    return True
def enter_into_database(data, user):
    data_table = pd.json_normalize(data)
    data_table.insert(0, 'user_id', user)
    name_list = data_table.columns
    print(name_list)
    # print(data_table)
    engine = db.create_engine('sqlite:///job-search-results.db')
    data_table.to_sql('jobs', con=engine, if_exists='replace', index=False)#need to fix
    query = engine.execute(f"SELECT * FROM jobs WHERE user_id='{user}'").fetchall()
    print_func(query)
    return engine

def program_driver(user_name):
    engine = db.create_engine('sqlite:///job-search-results.db')
    num_user = engine.execute(f"SELECT COUNT(user_id) FROM jobs WHERE user_id='{user_name}';").fetchone()[0]
    if num_user > 0:
        print(f"Welcome back, {user_name.replace('_', ' ').title()}!")
        query = engine.execute(f"SELECT * FROM jobs WHERE user_id='{user_name}';")
        print_func(query)
        answer = input("If you would like to research different jobs, press 'y' and hit enter. Otherwise, hit enter.").lower().strip()
        if answer == 'y':
            search_api()
    else:
        search_api()

    


def search_api():
    job_fields = input("Enter comma-separated fields \
in which you would like to search for jobs: ").strip()
    location = input("(OPTIONAL) Enter a location for jobs,\
else hit enter: ").strip()

    # interchange use of API Keys to limit searches
    API_KEYS = ('e21193f2b2ee7a0a7042c7a414822b20b10c84609c42a408732401d8b62ddc06',
                '9e8e77e8075bf5f1bfbbef8848ba3b735d1cf01e0490877307eded9945e41777')

    key_index = random.randint(0, 1)

    # make GET request and convert to json data containing job results
    r = requests.get(f'https://serpapi.com/search.json?engine=google_jobs&q={job_fields}&location={location}&api_key={API_KEYS[key_index]}')
    data = r.json()['jobs_results']
    for job in data:
        job.pop('extensions', None)
        job.pop('thumbnail', None)
    pprint.pprint(data)

    job_nums = input("type the number of the job you are interested in. \
(Number meaning what place in the order shown) If you are interested \
in multiple, seperate numbers with a ',': ")
    nums = job_nums.split(',')
    id_list = []
    dict_list = []
    for num in nums:
        id_list.append(data[int(num) - 1]['job_id'])
        dict_list.append(data[int(num) - 1])
    enter_into_database(dict_list, user_name)

    list_data = []
    # for id in id_list:
    #     request = requests.get(f'https://serpapi.com/search.json?\
    #     engine=google_jobs_listing&q={id}&api_key={API_KEYS[key_index]}')
    #     link_data = request.json()["apply_options"]
    #     list_data.append(link_data)
    # for i in range(len(list_data)):
    #     print(f'job {i + 1}:')
    #     for j in range(len(list_data[i])):
    #         for key, value in list_data[i][j].items():
    #             if key == 'link' and j <= 3:
    #                 print(f'Application Link {j}: {list_data[i][j][key]}')



if __name__ == '__main__':
    user_name = None
    while not user_check(user_name):
        user_name = input("Please type your firstname_lastname: ").lower().strip()
    program_driver(user_name)