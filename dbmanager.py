import sqlite3


def create_database_schema():
    connection = sqlite3.connect("categories.db")
    cursor = connection.cursor()

    # Check first if the database already exists
    cursor.execute("SELECT * FROM sqlite_master WHERE name = 'categories' and type='table'")

    if len(cursor.fetchall()) != 1:
        # Create categories table if not exists
        cursor.execute('CREATE TABLE categories ('
                       'CategoryID NUMBER, '
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
    connection = sqlite3.connect("categories.db")
    cursor = connection.cursor()

    categories_data = []
    for category in categories:

        if hasattr(category, 'BestOfferEnabled'):
            best_offer_enabled = category['BestOfferEnabled'] == 'true'
        else:
            best_offer_enabled = False
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
    cursor.execute('SELECT CategoryID, Name, BestOffer, Level, Parent '
                   'FROM categories '
                   'WHERE CategoryID=?',
                   (category_id,))
    return cursor.fetchall()


def _get_tree_html(category, cursor):
    cursor.execute('SELECT CategoryID, Name, BestOffer, Level, Parent '
                   'FROM categories '
                   'WHERE Parent=? and Parent != CategoryID',
                   (category[0],))
    categories = cursor.fetchall()

    category_children_html = ""

    for sub_category in categories:
        children_html = _get_tree_html(sub_category, cursor)
        if children_html:
            category_children_html += children_html

    category_html = """
        <table>
            <tr>
                <td>
                    {}
                </td>
                <td>
                    {}
                </td>
            <tr>
        </table>
    """.format(category[1], category_children_html)

    return category_html


def get_categories_tree(category_id):
    connection = sqlite3.connect("categories.db")
    cursor = connection.cursor()

    root_category = _get_category(category_id, cursor)

    if len(root_category) == 0:
        connection.commit()
        connection.close()
        return None

    category_html = _get_tree_html(root_category[0], cursor)

    open_html = """
    <html>
        <head>
            <title>{}</title>
        </head>
        <body>
            {}
        </body>
    </html>  """.format(str(category_id), category_html)

    html_name = '{}.html'.format(str(category_id))
    html_file = open(html_name, 'w')
    html_file.write(open_html)
    html_file.close()

    connection.commit()
    connection.close()
    return root_category
