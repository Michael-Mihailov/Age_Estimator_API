from pathlib import Path

class LifeTable:
    def __init__(self, path: Path, target_year: int):
        self.__path = path
        self.__target_year = target_year

        self.__starting_births_count = 0 # default to 0, will be set when loading the life table
        self.__life_table = self.__load_life_table()

    def __load_life_table(self):
        life_table = {} # life_table[birth_year] = alive_probability (probability of being alive at target_year)
        
        with open(self.__path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                try:
                    int(parts[0]) # check if the first part is an integer (birth year), if not, skip this line (header or malformed line)
                except (ValueError, IndexError):
                    continue

                birth_year = int(parts[0])
                age = int(parts[1].replace('+', ''))

                if age == 0:
                    self.__starting_births_count = int(parts[5])

                if birth_year + age == self.__target_year:
                    life_table[birth_year] = int(parts[5]) / self.__starting_births_count
        
        return life_table
    
    def get_alive_probability(self, birth_year: int) -> float:
        if birth_year in self.__life_table:
            return self.__life_table[birth_year]
        else:
            return 0.0