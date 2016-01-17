import sqlite3
from utils import generate_tree_html


def create_database_schema():
    """
    Generate the database and the categories table, if the database
    already exists, delete all the rows in the table
    """

    connection = sqlite3.connect("categories.db")
    cursor = connection.cursor()

    # Check first if the categories table already exists
    cursor.execute("SELECT * FROM sqlite_master WHERE name = 'categories' and type='table'")

    if len(cursor.fetchall()) != 1:
        # Create categories table if not exists
        cursor.execute('CREATE TABLE categories ('
                       'CategoryID NUMBER PRIMARY KEY, '
                       'Name TEXT, '
                       'Parent NUMBER, '
                       'BestOffer BOOLEAN, '
                       'Level NUMBER)'
                       )
    else:
        # Delete data if table already exist
        cursor.execute('DELETE FROM categories')

    connection.commit()
    connection.close()


def create_categories_rows(categories):
    """
    Format the data recovered from the Ebay api, before inserting it into the database
    """
    connection = sqlite3.connect("categories.db")
    cursor = connection.cursor()

    categories_data = []
    for category in categories:
        best_offer_enabled = category.get('BestOfferEnabled', False)
        formatted = (
            int(category['CategoryID']),
            category['CategoryName'],
            int(category['CategoryParentID']),
            best_offer_enabled,
            int(category['CategoryLevel']),
        )
        categories_data.append(formatted)

    cursor.executemany('INSERT INTO categories(CategoryID, Name, Parent, BestOffer, Level) '
                       'VALUES (?, ?, ?, ?, ?)', categories_data)

    connection.commit()
    connection.close()


def _get_category(category_id, cursor):
    """
    Return a category

    :param category_id:
    :param cursor:
    """
    cursor.execute('SELECT CategoryID, Name, BestOffer, Level, Parent '
                   'FROM categories '
                   'WHERE CategoryID=?',
                   (category_id,))
    return cursor.fetchall()


def get_categories_tree(category_id):
    """
    Retrieve the root category, if it does not exist, close the connection to the
    database and return a null value
    """
    connection = sqlite3.connect("categories.db")
    cursor = connection.cursor()

    root_category = _get_category(category_id, cursor)

    # if the query does not retrieve any value, return a null value
    if len(root_category) == 0:
        connection.commit()
        connection.close()
        return None

    generate_tree_html(root_category[0], cursor)

    connection.commit()
    connection.close()
    return root_category
