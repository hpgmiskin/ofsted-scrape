from bs4 import BeautifulSoup
import urllib.parse

import re
import time

from Shared import getPage
from SchoolObject import SchoolObject
from PageUtils import PageError, getName, getHead, getItems, getOfsted

class SchoolSearch():

    def __init__(self):
        self.postcode = "SW17 8RW"
        self.distance = 5

        self.schoolIDs = []
        self.schools = []

    def config(self,postcode,distance):
        """Configuration for the searching of schools search

        Params:
            postcode: string of postcode
            distance: integer of distance from [1,3,5,10,15,25]
        """

        distances = [1,3,5,10,15,25]
        if distance not in distances:
            raise ValueError("Distance must be in {}".format(distances))

        self.postcode = postcode
        self.distance = distance

    def searchSchools(self):
        """Searches for schools using the configuration given previously
        the school IDs are stored as a class varaibles for later use
        """

        urlBase = "http://www.education.gov.uk"
        urlPath = "/cgi-bin/schools/performance/search.pl?"

        params = (
            ("searchType", "postcode"),
            ("postcode", self.postcode),
            ("distance", self.distance),
            ("phase", "all")
            )

        urlParams = urllib.parse.urlencode(params)
        url = urlBase+urlPath+urlParams

        pageContent = getPage(url)
        self.setSchools(pageContent)

    def setSchools(self,pageContent):
        """Sets the school ids from the given page content of the search
        results
        """

        soup = BeautifulSoup(pageContent)

        # Obtain list of school IDS close to the given postcode
        for school in soup.find_all(class_='schoolname'):

            link = school.find("a")["href"]
            match = re.match(r"\D*(\d+)\D*",link)

            if not match: continue
            schoolID = match.group(1)

            self.schoolIDs.append(schoolID)

    def setSchoolDetails(self):

       for schoolID in self.schoolIDs:

            url = "http://www.education.gov.uk/schools/performance/school/{}".format(schoolID)

            content = getPage(url)
            soup = BeautifulSoup(content)

            queries = ["Head","Street","Town","Postcode","Telephone number"]

            try:
                name = getName(soup)
                attrObject = getItems(soup,queries)
                date,grade,link = getOfsted(soup)
            except PageError:
                continue

            school = SchoolObject(schoolID)
            school.url = url
            school.setName(name)
            school.setAttr(attrObject)
            school.setOfsted(date,grade,link)

            self.schools.append(school)


    def printBadSchools(self):
        """Returns the schools whos ofsted grade is bellow the given
        """

        def date(school):
            return school.date

        self.schools.sort(key=date)

        for school in self.schools:

            if school.grade > 2:
                print(school)
                school.save()

            # if school.date > time.strptime("01/01/14")


if (__name__ == "__main__"):
    schoolSearch = SchoolSearch()
    schoolSearch.searchSchools()
    schoolSearch.setSchoolDetails()
    schoolSearch.printBadSchools()
