import re
import time

class PageError(Exception):
      pass

def getName(soup):
      """Returns the name of the school
      """

      areaTitle = soup.find(class_="areaTitle")
      title = areaTitle.find("h2")
      name = title.get_text().strip()

      return name


def getHead(soup):
      """Returns the head of the school
      """

      return getItem(soup,"Headteacher")

def getItem(soup,query):

      label = soup.find(text=re.compile(query))
      item = label.find_next(class_="num ")
      text = item.get_text().strip()

      return text

def getItems(soup,queries):

      queryObject = {}

      for query in queries:
            key = query.lower().replace(" ","")
            value = getItem(soup,query)
            queryObject[key] = value

      return queryObject

def getOfsted(soup):

      # Find inspection report
      link = soup.find("a", href=re.compile(r".*inspection-reports/find-inspection-report\D*(\d+)\D*"))

      # If there is not an ofsted link continue
      if not link: raise PageError("No Ofsted report")

      # Find the parent table of the ofsted report
      table = link.find_parent("table")

      # Retrieve the date date grade and link from ofsted
      date,grade,link = table.find_all(class_="num ")

      # Format these to python
      date = time.strptime(date.string.strip(),"%d %B %Y")
      grade = int(grade.string.strip())
      link = link.find("a")["href"]

      return date,grade,link