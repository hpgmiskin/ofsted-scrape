import urllib.request
import urllib.parse

import re
import os
import time

def cache(function):
    """Returns the given function unless a cached version is available 
    with the given arguments
    """

    def decorate(*args):
        """decorator to load the cache or call the function
        """

        stripArgs = [re.sub(r"\W","",arg) for arg in args]
        filename = "_".join(stripArgs) + ".cache"

        filename = os.path.join("cache",filename)

        try:
            with open(filename) as openFile:
                content = openFile.read()
        except FileNotFoundError:
            content = function(*args)
            with open(filename, "w") as openFile:
                openFile.write(content)

        return content

    return decorate

@cache
def getPage(url):
    page = urllib.request.urlopen(url)
    return page.read().decode("utf-8")