from pathlib import Path

class BirthsTable:
    def __init__(self, path: Path):
        self.__path = path

        
        (self.__births_list_female,
        self.__births_list_male 
        ) = self.__load_births_table()
        
    def __load_births_table(self):
        births_list_female = []
        births_list_male = []

        with open(self.__path, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) != 3:
                    continue # skip malformed lines
                
                name = parts[0]
                sex = parts[1]
                count = int(parts[2])

                if sex == 'F':
                    births_list_female.append((name, count))
                elif sex == 'M':
                    births_list_male.append((name, count))

        return births_list_female, births_list_male

    def get_birth_list_female(self):
        return self.__births_list_female

    def get_birth_list_male(self):
        return self.__births_list_male
    
    def get_birth_list_combined(self):
        births_list_combined = [] # combined and sorted by count

        length_female = len(self.__births_list_female)
        length_male = len(self.__births_list_male)
        pointer_female = 0
        pointer_male = 0
        while pointer_female < length_female and pointer_male < length_male:
            name_female, count_female = self.__births_list_female[pointer_female]
            name_male, count_male = self.__births_list_male[pointer_male]

            if count_female > count_male:
                births_list_combined.append((name_female, count_female))
                pointer_female += 1
            else:
                births_list_combined.append((name_male, count_male))
                pointer_male += 1

        # Append any remaining names from either list
        births_list_combined.extend(self.__births_list_female[pointer_female:])
        births_list_combined.extend(self.__births_list_male[pointer_male:])

        return births_list_combined