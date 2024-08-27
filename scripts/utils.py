from datetime import datetime
import re
def parse_date(text):
    """
    Parse a date given as a string in the format '%B %d, %Y'
    and return a datetime.date object.

    The function also replaces 'Aug.' with 'August' in the input string
    (because the AP News website uses that format).
    """
    # replace 'Aug.' with 'August' in the input string
    text = re.sub(r'Aug\.', 'August', text)
    # parse the date
    date_object = datetime.strptime(text, "%B %d, %Y")
    # return the date part of the datetime object
    return date_object.date()
