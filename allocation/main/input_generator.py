import os
import csv
import random


inputs_path = os.path.abspath('../../inputs/')


def generate_disciplines():
    main_file = f'{inputs_path}/1.csv'
    disciplines_qnt = [3, 4, 4, 5, 5, 5, 6, 6, 7, 7]
    with open(main_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = list(reader.fieldnames)
        disciplines = list(reader)
        for i, v in enumerate(disciplines_qnt):
            partial_disciplines = random.sample(disciplines, v)
            with open(f'{inputs_path}/{i + 2}.csv', 'w', newline='') as partial_csvfile:
                whiter = csv.DictWriter(partial_csvfile, fieldnames=fieldnames)
                whiter.writeheader()
                whiter.writerows(partial_disciplines)


generate_disciplines()
