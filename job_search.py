# start with the imports
import pandas as pandas
import random
import requests
import json
import SQLAlchemy as db

# using SerpAPI -- no import needed, just the keys?

job_fields = input("Enter comma-separated fields you would like to search for jobs: ")
location = input("(OPTIONAL) Enter a location for jobs, else hit enter: ").strip()


# # validate job_field input formatting
# def is_valid_input(job_field):
#     if not ('a' < job_field < 'z' or 'A' < job_field < 'Z':
#         print("Improper formatting")
#         return False

# leave input as-is: API takes care of weird inputs with an "error" key in JSON


# while not is_valid_input(job_field):
#     job_field = input("Enter comma-separated fields you would like to search for jobs: ")

#interchange use of API Keys to limit searches since we only get 100 each
API_KEYS = ('e21193f2b2ee7a0a7042c7a414822b20b10c84609c42a408732401d8b62ddc06',
            '9e8e77e8075bf5f1bfbbef8848ba3b735d1cf01e0490877307eded9945e41777')

counter = random.randint(0, 1) #?

#make GET request and convert to json data containing job results
r = requests.get(f'https://serpapi.com/search.json?engine=google_jobs&q={job_fields}&location={location}&api_key={API_KEYS[counter]}')
data = r.json()['jobs_results']

#Now that we have list of dictionaries with seperate job offerings data, we must now convert it into sql database
print(data) #testing
