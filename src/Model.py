"""Model
    Contains the model class needed for the MVC model
    
    Attributes:
        * name: SALFIC
        * date: 25.04.2021
        * version: 0.0.1 Beta- free
"""
class ModelMVC():
    """ModelMVC
        Contains the data shown in the view
    """
    def __init__(self):
        """Inits empty Dictionary
        """
        self.values = {}

    def fillValues(self):
        """fillValues
            Fills the dictionary with the wished value
        """
        self.values = {"Brandenburg" : "DE-BB", "Berlin":"DE-BE", "Baden-Württemberg":"DE-BW", "Bayern":"DE-BY", "Bremen":"DE-HB",
                    "Hessen":"DE-HE", "Hamburg":"DE-HH", "Mecklenburg-Vorprommen":"DE-MV", "Niedersachsen":"DE-NI",
                    "Nordrhein-Westfalen":"DE-NW", "Rheinland-Pfalz":"DE-RP", "Schleswig-Holstein":"DE-SH",
                    "Saarland":"DE-SL", "Sachsen":"DE-SN", "Sachsen-Anhalt":"DE-ST", "Thüringen":"DE-TH"}
    
    def getValues(self):
        """getValues
            Returns the values that should be shown

        Returns:
            dict: Contains the information to show in the view
        """ 
        return self.values