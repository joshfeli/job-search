# start with the imports
import pandas as pd
import random
import requests
import json
import pprint
import sqlalchemy as db

# using SerpAPI -- no import needed, just the keys
job_fields = input("Enter comma-separated fields \
in which you would like to search for jobs: ").strip()
location = input("(OPTIONAL) Enter a location for jobs,\
 else hit enter: ").strip()

# # validate job_field input formatting
# def is_valid_input(job_field):
#     if not ('a' < job_field < 'z' or 'A' < job_field < 'Z':
#         print("Improper formatting")
#         return False

# leave input as-is: API takes care of weird inputs with an "error" key in JSON

# interchange use of API Keys to limit searches
API_KEYS = ('e21193f2b2ee7a0a7042c7a414822b20b10c84609c42a408732401d8b62ddc06',
            '9e8e77e8075bf5f1bfbbef8848ba3b735d1cf01e0490877307eded9945e41777')


counter = random.randint(0, 1)
key_index = random.randint(0, 1)


# make GET request and convert to json data containing job results
r = requests.get(f'https://serpapi.com/search.json?engine=google_jobs\
&q={job_fields}&location={location}&api_key={API_KEYS[key_index]}')
data = r.json()['jobs_results']
# enter_into_database(data)
pprint.pprint(data)

job_nums = input("type the number of the job you are interested in. \
(Number meaning what place in the order shown) If you are interested \
in multiple, seperate numbers with a ',': ")
nums = job_nums.split(',')
id_list = []
for num in nums:
    id_list.append(data[int(num)]['job_id'])
list_data = []
for id in id_list:
    request = requests.get(f'https://serpapi.com/search.json?\
    engine=google_jobs_listing&q={id}&api_key={API_KEYS[key_index]}')
    link_data = request.json()["apply_options"]
    list_data.append(link_data)
for i in range(len(list_data)):
    print(f'job {i + 1}:')
    for j in range(len(list_data[i])):
        for key, value in list_data[i][j].items():
            if key == 'link' and j <= 3:
                prev_link = link_data
                print(f'Application Link {j}: {list_data[i][j][key]}')


# Now that we have list of dictionaries with seperate job offerings data
# , we must now convert it into sql database
def enter_into_database(data):
    data_table = pd.json_normalize(data)
    engine = db.create_engine('sqlite:///job-search-results.db')
    data_table.to_sql('jobs', con=engine, if_exists='replace', index=False)
    return engine
