
class ModelMVC():
    def __init__(self):
        self.values = {}

    def fillValues(self):
        self.values = {"Brandenburg" : "DE-BB", "Berlin":"DE-BE", "Baden-Württemberg":"DE-BW", "Bayern":"DE-BY", "Bremen":"DE-HB",
                    "Hessen":"DE-HE", "Hamburg":"DE-HH", "Mecklenburg-Vorprommen":"DE-MV", "Niedersachsen":"DE-NI",
                    "Nordrhein-Westfalen":"DE-NW", "Rheinland-Pfalz":"DE-RP", "Schleswig-Holstein":"DE-SH",
                    "Saarland":"DE-SL", "Sachsen":"DE-SN", "Sachsen-Anhalt":"DE-ST", "Thüringen":"DE-TH"}
        return self.values