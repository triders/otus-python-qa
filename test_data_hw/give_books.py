import json
from csv import DictReader


with open("books.csv", "r") as books_file:
    result = []
    books_dr_object = DictReader(books_file)

    with open("users.json", "r") as users_file:
        users_json = json.load(users_file)

        for user in users_json:
            result.append(
                {
                    "name": user["name"],
                    "gender": user["gender"],
                    "address": user["address"],
                    "age": user["age"],
                    "books": []
                }
            )

        user_num = len(result)
        i = 0
        for book in books_dr_object:
            user = result[i % user_num]
            user["books"].append(
                {
                    "title": book["Title"],
                    "author": book["Author"],
                    "pages": book["Pages"],
                    "genre": book["Genre"]
                }
            )
            i += 1

        with open("result.json", "w") as results_file:
            res = json.dumps(result, indent=4)
            results_file.write(res)
