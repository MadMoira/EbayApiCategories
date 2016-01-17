def is_valid_id(string_id):
    try:
        int(string_id)
        return True
    except ValueError:
        return False
