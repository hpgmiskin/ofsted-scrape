import os
import re
import time
import json

import urllib.parse

from Shared import getPage, saveJSON
from SchoolObject import SchoolObject

class SchoolSearch():

    def __init__(self):
        self.postcode = "SW17 8RW"
        self.distance = 5

        self.schools = []

    def config(self,postcode,distance = 5):
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

        urlBase = "http://schoolsfinder.direct.gov.uk"
        urlPath = "/school-location-search-results-json/&"

        params = (
            ("searchString", self.postcode),
            ("distanceValue", self.distance)
            )

        urlParams = urllib.parse.urlencode(params)
        url = urlBase+urlPath+urlParams

        pageContent = getPage(url)
        self.setSchools(pageContent)

    def setSchools(self,pageContent):
        """Sets the school ids from the given page content of the search
        results
        """

        jsonObject = json.loads(pageContent)

        colums = jsonObject["QPOSTCODE"]["COLUMNS"]
        data = jsonObject["QPOSTCODE"]["DATA"]

        columnIDs = {}

        columnIDs["URN"] = colums.index("URN")
        columnIDs["schoolName"] = colums.index("SCHOOLNAME")
        columnIDs["toe_desc"] = colums.index("TOE_DESC")

        columnIDs["address"] = colums.index("ADDRESS1")
        columnIDs["town"] = colums.index("TOWN")
        columnIDs["county"] = colums.index("COUNTY")
        columnIDs["postcode"] = colums.index("POSTCODE")

        columnIDs["headteacher"] = colums.index("HEADTEACHER")
        columnIDs["contactName"] = colums.index("CONTACTNAME")
        columnIDs["contactEmail"] = colums.index("CONTACTEMAIL")
        columnIDs["telephone"] = colums.index("TELEPHONE")
        columnIDs["URL"] = colums.index("URL")

        columnIDs["isPrimary"] = colums.index("ISPRIMARY")
        columnIDs["isSecondary"] = colums.index("ISSECONDARY")
        columnIDs["isSixthform"] = colums.index("ISSIXTHFORM")

        columnIDs["isPrivate"] = colums.index("ISPRIVATE")
        columnIDs["isAcademy"] = colums.index("ISACADEMY")
        columnIDs["isCityTech"] = colums.index("ISCITYTECH")
        columnIDs["isExtended"] = colums.index("ISEXTENDED")

        columnIDs["pupils"] = colums.index("PUPILS")
        columnIDs["specialismA"] = colums.index("SPECIALISM")
        columnIDs["specialismB"] = colums.index("SPECIALISM2")
        columnIDs["capacity"] = colums.index("CAPACITY")

        columnIDs["ictLevel"] = colums.index("ICTLEVEL")
        columnIDs["schoolSpecialismID"] = colums.index("SCHOOLSPECIALISMID")

        columnIDs["latestKs2Percentlevel4"] = colums.index("LATESTKS2PERCENTLEVEL4")
        columnIDs["latestKs3AvgPointScore"] = colums.index("LATESTKS3AVGPOINTSCORE")
        columnIDs["latestGcseGradesac"] = colums.index("LATESTGCSEGRADESAC")
        columnIDs["latestBacPercent"] = colums.index("LATESTBACPERCENT")

        columnIDs["ofstedGrade"] = colums.index("LATESTOVERALLOFSTEDGRADE")
        columnIDs["ofstedGradeOrdinal"] = colums.index("LATESTOVERALLOFSTEDGRADEORDINAL")
        columnIDs["latestKs2PercentLevel4Ordinal"] = colums.index("LATESTKS2PERCENTLEVEL4ORDINAL")
        columnIDs["latestGcseGradeSacOrdinal"] = colums.index("LATESTGCSEGRADESACORDINAL")
        columnIDs["latestBacPercentOrdinal"] = colums.index("LATESTBACPERCENTORDINAL")
        
        for school in data:

            schoolObject = {}

            schoolObject["URN"] = school[columnIDs["URN"]]
            schoolObject["schoolName"] = school[columnIDs["schoolName"]]
            schoolObject["toe_desc"] = school[columnIDs["toe_desc"]]

            schoolObject["address"] = school[columnIDs["address"]]
            schoolObject["town"] = school[columnIDs["town"]]
            schoolObject["county"] = school[columnIDs["county"]]
            schoolObject["postcode"] = school[columnIDs["postcode"]]

            schoolObject["headteacher"] = school[columnIDs["headteacher"]]
            schoolObject["contactName"] = school[columnIDs["contactName"]]
            schoolObject["contactEmail"] = school[columnIDs["contactEmail"]]
            schoolObject["telephone"] = school[columnIDs["telephone"]]
            schoolObject["URL"] = school[columnIDs["URL"]]

            schoolObject["isPrimary"] = school[columnIDs["isPrimary"]]
            schoolObject["isSecondary"] = school[columnIDs["isSecondary"]]
            schoolObject["isSixthform"] = school[columnIDs["isSixthform"]]

            schoolObject["isPrivate"] = school[columnIDs["isPrivate"]]
            schoolObject["isAcademy"] = school[columnIDs["isAcademy"]]
            schoolObject["isCityTech"] = school[columnIDs["isCityTech"]]
            schoolObject["isExtended"] = school[columnIDs["isExtended"]]

            schoolObject["pupils"] = school[columnIDs["pupils"]]
            schoolObject["specialismA"] = school[columnIDs["specialismA"]]
            schoolObject["specialismB"] = school[columnIDs["specialismB"]]
            schoolObject["capacity"] = school[columnIDs["capacity"]]

            schoolObject["ictLevel"] = school[columnIDs["ictLevel"]]
            schoolObject["schoolSpecialismID"] = school[columnIDs["schoolSpecialismID"]]

            # schoolObject["latestKs2Percentlevel4"] = school[columnIDs["latestKs2Percentlevel4"]]
            # schoolObject["latestKs3AvgPointScore"] = school[columnIDs["latestKs3AvgPointScore"]]
            # schoolObject["latestGcseGradesac"] = school[columnIDs["latestGcseGradesac"]]
            # schoolObject["latestBacPercent"] = school[columnIDs["latestBacPercent"]]

            schoolObject["ofstedGrade"] = school[columnIDs["ofstedGrade"]]
            schoolObject["ofstedGradeOrdinal"] = school[columnIDs["ofstedGradeOrdinal"]]
            # schoolObject["latestKs2PercentLevel4Ordinal"] = school[columnIDs["latestKs2PercentLevel4Ordinal"]]
            # schoolObject["latestGcseGradeSacOrdinal"] = school[columnIDs["latestGcseGradeSacOrdinal"]]
            # schoolObject["latestBacPercentOrdinal"] = school[columnIDs["latestBacPercentOrdinal"]]

            self.addSchool(schoolObject)

    def addSchool(self,schoolObject):

        try:
            ofstedOverall = schoolObject["ofstedGrade"].split("-")
            schoolObject["ofstedGrade"] = int(ofstedOverall[0].strip())
        except ValueError:
            schoolObject["ofstedGrade"] = 0

        school = SchoolObject()
        school.setAttr(schoolObject)
        self.schools.append(school)

        filename = "{}.json".format(schoolObject["URN"])
        folder = "schools"
        saveJSON(filename,schoolObject,folder)

    def printBadSchools(self):
        """Returns the schools whos ofsted grade is bellow the given
        """

        def show(school):
            "Only show schools with poor ofsted"

            logic = (
                (school.ofstedGrade == 0) and
                (school.isPrimary) and
                (school.isPrivate)
                )

            return logic

        def sort(school):
            return school.pupils

        self.schools.sort(key=sort)

        for school in self.schools:

            if show(school):
                print(school)


if (__name__ == "__main__"):
    schoolSearch = SchoolSearch()
    schoolSearch.config("SW7 2AZ")
    schoolSearch.searchSchools()
    schoolSearch.printBadSchools()
