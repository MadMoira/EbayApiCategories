from settings import ENDPOINT
from settings import HEADERS
from settings import XML_PARAMETERS
from dbmanager import create_database_schema
from dbmanager import create_categories_rows
from dbmanager import get_categories_tree
from utils import is_valid_id
import requests
import xmltodict
import json
import sys


if sys.argv[1] == "--rebuild":

    request = requests.post(ENDPOINT, data=XML_PARAMETERS, headers=HEADERS)
    parsed_request = xmltodict.parse(request.content)
    data = parsed_request['GetCategoriesResponse']

    if data['Ack'] == 'Success':
        categories_data = data['CategoryArray']['Category']
        create_database_schema()
        create_categories_rows(categories_data)

    elif data['Ack'] == 'Failure':
        print("There was an error with your request, try again please")
        print(json.dumps(data['Errors'], indent=4))

elif sys.argv[1] == "--render":
    # Check if there are at least three parameters, router + render + category ID
    if len(sys.argv) < 3:
        print("Error. Please enter a category id")
    # Check if the category ID is a valid value, must be a number
    elif not is_valid_id(sys.argv[2]):
        print("Invalid ID. Please enter  a number")
    else:
        # This function return the root category of the tree and render the tree in a html file
        categories = get_categories_tree(int(sys.argv[2]))
        if not categories:
            print("No category with ID: {}".format(sys.argv[2]))
        else:
            print("The tree has been rendered")

else:
    print("Please, enter a valid command")



