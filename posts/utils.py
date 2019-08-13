import re
import math
import datetime
from django.utils.html import strip_tags
def count_word(html_string):
    word_string=strip_tags(html_string)
    matching_words=re.findall(r'\w+',word_string)
    count=len(matching_words)
    return count


def get_read_time(html_string):
    count=count_word(html_string)
    read_time_min=math.ceil(count/200.0)
    read_time=datetime.timedelta(minutes=read_time_min)
    return read_time