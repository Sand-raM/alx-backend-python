#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_paginate  # Corrected function name

try:
    for page in lazy_paginator(100):  # Load pages lazily with 100 users per page
        for user in page:  # Iterate through each user in the page
            print(user)
except BrokenPipeError:
    sys.stderr.close()