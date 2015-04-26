import glob
from bs4 import BeautifulSoup

from Shared import getPage, getPDF, savePDF, saveFile
from SchoolObject import SchoolObject

class OfsteadSearch:

    def __init__(self):
        pass

    def setSchool(self,school):

        self.school = school

    def filename(self):

        filename = self.school.filename("reports").split(".")[0]
        filename = "{}.pdf".format(filename)

        return filename

    def getOfstead(self):
        
        url = self.school.report
        content = getPage(url)
        soup = BeautifulSoup(content)
        div = soup.find(class_="download-report-link")

        if not div:
            print("Error for school {}".format(self.school))
            return

        link = div.find("a")
        urlPath = link["href"]
        urlBase = "http://reports.ofsted.gov.uk"

        url = urlBase + urlPath
        report = getPDF(url)
        savePDF(self.filename,report)

if (__name__ == "__main__"):
    filenames = glob.glob("schools/*.json")

    for filename in filenames:

        schoolObject = SchoolObject(None)
        schoolObject.load(filename)

        ofsteadSearch = OfsteadSearch()
        ofsteadSearch.setSchool(schoolObject)
        ofsteadSearch.getOfstead()