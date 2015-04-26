from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

import glob
from Shared import saveFile
from PageObject import PageObject
from TextCompare import TextCompare

class ReportObject(object):
    """
    ReportObject is used to analyse the layout of a pdf document
    """

    def __init__(self, filename=None):
        """Contructs the class with the option of loading the given
        document
        """

        self.pageObjects = {}

        if filename:
            self.filename = filename.split(".")[0]
            self.loadDocument(filename)
        
    def loadDocument(self,filename):
        """loads the document of the given name as a class attribute
        """

        # open the pdf file
        with open(filename, 'rb') as openFile:

            # crease a parser object from the open file
            self.parser = PDFParser(openFile)

            # store the document structure
            self.document = PDFDocument()

            # set document and parser relations
            self.parser.set_document(self.document)
            self.document.set_parser(self.parser)
            self.document.initialize('')

            # define the pages of the pdf document
            self.pages = self.document.get_pages()

            # process the pages
            self.processPages()

    def processPages(self):
        """extracts the text from the pdf document
        """
        manager = PDFResourceManager()
        parameters = LAParams()
        device = PDFPageAggregator(manager, laparams=parameters)
        interpreter = PDFPageInterpreter(manager, device)

        for pageNumber, page in enumerate(self.pages):

            interpreter.process_page(page)
            layout = device.get_result()
            
            self.pageObjects[pageNumber] = []
            self.extractText(layout, pageNumber)

    def extractText(self, layout, pageNumber):
        """extracts the text from the given page and adds all text
        instances to the text dictionary
        """

        for layoutObject in layout:

            # If the text object is a text box then extract text again
            if (isinstance(layoutObject, LTTextBox)):

                self.extractText(layoutObject,pageNumber)

            # if the text object then add child to parent if required
            elif (isinstance(layoutObject, LTTextLine)):

                # Create new page object
                pageObject = PageObject()

                # Add the object text
                text = layoutObject.get_text()
                text = text.encode("utf-8","ignore")
                pageObject.text = text

                # Define the bounding box
                pageObject.setBoundingBox(layoutObject.bbox)

                # Add to page objects list
                self.pageObjects[pageNumber].append(pageObject)


    def processObjects(self):
        """processes the extracted objects so that all objects have
        north, east, south and west relations where possible
        """

        for pageNumber, pageObjects in self.pageObjects.items():
            for pageObject in pageObjects:
                self.processObject(pageNumber, pageObject)


    def processObject(self,pageNumber, pageObject):
        """processes the given object so that it has a north, east
        south and west relation
        """

        for otherPageObject in self.pageObjects[pageNumber]:

            # If the same object then continue
            if (pageObject == otherPageObject):
                continue

    def findObject(self,searchString):
        """returns the object whos text most resembles the provided
        search string
        """

        bestRatio = 0
        bestObject = None

        textCompare = TextCompare()
        textCompare.setSearch(searchString)
        # searchSet = set(searchString.split())

        for page in self.pageObjects.values():
            for pageObject in page:

                # matchSet = set(pageObject.text.split())
                # ratio = len(searchSet&matchSet)/len(searchSet|matchSet)

                textCompare.setMatch(pageObject.text)
                ratio = textCompare.ratio()

                if ratio > bestRatio:
                    bestRatio = ratio
                    bestObject = pageObject

        return bestObject

    def findText(self,searchList):

        results = []

        for search in searchList:
            searchObject = self.findObject(search)
            if searchObject: results.append(str(searchObject))

        if (len(results) > 0):
            return results

    def __str__(self):
        """returns a string representation of the text
        """

        pageDivide = "\n" + "="*10 + "\n"
        itemDivide = "-" * 5

        pages = self.pageObjects.values()
        toPrint = ""

        for page in pages:
            for pageObject in page:
                toPrint += str(pageObject)
                toPrint += itemDivide
            toPrint += pageDivide

        return toPrint

if (__name__ == "__main__"):
    filenames = glob.glob("reports/*.pdf")

    for filename in filenames:

        reportObject = ReportObject(filename)
        results = reportObject.findText(["computing","ict","technology"])
        if results:
            filename = filename.split("/")[1].split(".")[0]
            print("{} - {}".format(filename,results))
            saveFile("results/{}.txt".format(filename),str(results))
