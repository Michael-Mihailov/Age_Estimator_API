from pathlib import Path

class BirthsTable:
    def __init__(self, path: Path):
        self.__path = path

        
        (self.__births_list_female,
        self.__births_list_male,
        self.__births_list_combined 
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

        births_list_female = sorted(births_list_female, key=lambda x: x[1], reverse=True)
        births_list_male = sorted(births_list_male, key=lambda x: x[1], reverse=True)
        births_list_combined = self.__combine_births_lists(births_list_female, births_list_male)

        return births_list_female, births_list_male, births_list_combined
    
    def __combine_births_lists(self, births_list_female, births_list_male):
        births_list_combined = [] # combined and sorted by count

        length_female = len(births_list_female)
        length_male = len(births_list_male)
        pointer_female = 0
        pointer_male = 0
        while pointer_female < length_female and pointer_male < length_male:
            name_female, count_female = births_list_female[pointer_female]
            name_male, count_male = births_list_male[pointer_male]

            if count_female > count_male:
                births_list_combined.append((name_female, 'F', count_female))
                pointer_female += 1
            else:
                births_list_combined.append((name_male, 'M', count_male))
                pointer_male += 1

        # Append any remaining names from either list
        while pointer_female < length_female:
            name_female, count_female = births_list_female[pointer_female]
            births_list_combined.append((name_female, 'F', count_female))
            pointer_female += 1
        while pointer_male < length_male:
            name_male, count_male = births_list_male[pointer_male]
            births_list_combined.append((name_male, 'M', count_male))
            pointer_male += 1

        return births_list_combined
    
    def get_birth_list_ordered_female(self):
        return self.__births_list_female

    def get_birth_list_ordered_male(self):
        return self.__births_list_male

    def get_birth_list_ordered_combined(self):
        return self.__births_list_combined