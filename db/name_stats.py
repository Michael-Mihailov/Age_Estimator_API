class NameStats:
    def __init__(self, name: str, sex: str):
        self.__name = name
        self.__sex = sex

        self.__occurrence_by_year = {} # {year: count}
        self.__alive_occurrence_by_year = {} # {year: count}

        self.__total_occurrence_count = 0 # Total number of people to ever have this name
        self.__estimated_alive_count = 0.0 # Estimated number of them still alive

        self.__baby_name_popularity_rank_non_gendered_by_year = {} # {year: rank} for the rank of this name among baby names in that year
        self.__baby_name_popularity_rank_gendered_by_year = {} # {year: rank} for the rank of this name among baby names in that year within gender

        # Fields to be modified externally after all data is inputted
        self.all_time_popularity_rank_non_gendered = None
        self.all_time_popularity_rank_gendered = None
        self.alive_popularity_rank_non_gendered = None
        self.alive_popularity_rank_gendered = None

    def input_year_data(self, year: int, occurrence_count: int, alive_occurrence_count: int, rank_gendered: int, rank_overall: int):
        self.__occurrence_by_year[year] = occurrence_count
        self.__alive_occurrence_by_year[year] = alive_occurrence_count

        self.__total_occurrence_count += occurrence_count
        self.__estimated_alive_count += alive_occurrence_count

        self.__baby_name_popularity_rank_non_gendered_by_year[year] = rank_overall
        self.__baby_name_popularity_rank_gendered_by_year[year] = rank_gendered

    @property
    def name(self):
        return self.__name
    @property
    def sex(self):
        return self.__sex
    @property
    def occurrence_by_year(self):
        return self.__occurrence_by_year
    @property
    def alive_occurrence_by_year(self):
        return self.__alive_occurrence_by_year
    @property
    def total_occurrence_count(self):
        return self.__total_occurrence_count
    @property
    def estimated_alive_count(self):
        return self.__estimated_alive_count
    @property
    def baby_name_popularity_rank_non_gendered_by_year(self):
        return self.__baby_name_popularity_rank_non_gendered_by_year
    @property
    def baby_name_popularity_rank_gendered_by_year(self):
        return self.__baby_name_popularity_rank_gendered_by_year
    
    def compute_average_age(self, current_year: int):
        total_age = 0.0
        total_count = 0
        for year, count in self.__alive_occurrence_by_year.items():
            age = current_year - year
            total_age += age * count
            total_count += count
        return total_age / total_count if total_count > 0 else 0.0

    def compute_most_likely_age(self, current_year: int):
        most_likely_age = 0
        highest_count = 0
        for year, count in self.__alive_occurrence_by_year.items():
            if count > highest_count:
                highest_count = count
                most_likely_age = current_year - year
        return most_likely_age
    
    def compute_age_distribution(self, current_year: int):
        age_distribution = {}
        total_alive_count = self.estimated_alive_count
        for year, count in self.__alive_occurrence_by_year.items():
            age = current_year - year
            age_distribution[age] = count / total_alive_count if total_alive_count > 0 else 0.0
        return age_distribution
    
    def compute_popular_years_list(self):
        return sorted(self.__occurrence_by_year.keys(), key=lambda year: self.__occurrence_by_year[year], reverse=True)