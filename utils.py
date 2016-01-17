def _get_tree_html(category, cursor):
    """
    Create the HTML string of the categories, with all the subcategories
    """
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
                    Category ID: {}
                    Category Name: {}
                    Category Level: {}
                    Best offer enabled: {}
                    Parent category ID: {}
                </td>
                <td>
                    {}
                </td>
            <tr>
        </table>
    """.format(
            category[0],
            category[1],
            category[3],
            category[2],
            category[4],
            category_children_html
    )

    return category_html


def generate_tree_html(root_category, cursor):
    """
    Create or replace the HTML file with the root category id
    as the file name
    """
    category_html = _get_tree_html(root_category, cursor)

    open_html = """
    <html>
        <head>
            <title>{}</title>
        </head>
        <body>
            {}
        </body>
    </html>  """.format(str(root_category[0]), category_html)

    html_name = '{}.html'.format(str(root_category[0]))
    html_file = open(html_name, 'w')
    html_file.write(open_html)
    html_file.close()


def is_valid_id(string_id):
    """
    Check if the ID is a number, if the cast fails, throw a Value Error and return False
    """
    try:
        int(string_id)
        return True
    except ValueError:
        return False
