
class NameStats:
    def __init__(self, name: str, sex: str):
        self.__name = name
        self.__sex = sex

        self.__occurrence_by_year = {} # {year: count}
        self.__alive_occurrence_by_year = {} # {year: count}

        self.__total_occurrence_count = 0 # Total number of people to ever have this name
        self.__estimated_alive_count = 0.0 # Estimated number of them still alive

    def input_year_data(self, year: int, occurrence_count: int, alive_occurrence_count: int):
        self.__occurrence_by_year[year] = occurrence_count
        self.__alive_occurrence_by_year[year] = alive_occurrence_count

        self.__total_occurrence_count += occurrence_count
        self.__estimated_alive_count += alive_occurrence_count
