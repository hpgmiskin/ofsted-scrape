class PageObject(object):
    """PageObject stores the objects which exist on a pdf page"""

    def __init__(self):
        """Constructs the class and defines default parameters for page
        object attributes
        """
        
        # Top left corner
        self.x0 = None
        self.y0 = None

        # Bottom right corner
        self.x1 = None
        self.y1 = None

        # Center
        self.xC = None
        self.yC = None             

        # Content of page object
        self.text = ""

    def setBoundingBox(self,coordinates):
        """Defines the bounding box which the page object is within

        Params:
            coordinates - list of coordinates of bounding box
        """

        self.x0 = coordinates[0]
        self.y0 = coordinates[1]
        self.x1 = coordinates[2]
        self.y1 = coordinates[3]

        self.xC = (self.x0 + self.x1) / 2.0
        self.yC = (self.y0 + self.y1) / 2.0

    def __str__(self):
        """Returns the string representation of the object
        """

        return self.text.decode("ascii","ignore").strip("\n")
