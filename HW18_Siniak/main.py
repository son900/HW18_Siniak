import json

from Group import Group
from Person import Person
from Student import Student
from Teacher import Teacher

# список Persono-в
persons = [Person('Vasya', 'Pupkin', 'trinolyatrulyalya'),
           Person('Gora', 'Tereshkin', '+3874159767165'),
           Person('Angelina', 'Cherkashena', '+04409451235')]
# список Student-ов
students = [Student('Ivasyk', 'Bulkin', 'trinolyatrulyalya', 'Python11'),
            Student('Grigoiy', 'Terkin', '+387415874165', 'Python21'),
            Student('Anna', 'Chechetkina', '+04478451235', 'C++14'),
            Student('Svetlana', 'Bulkina', 'trinolyatrulyalya2', 'Python11'),
            Student('Anatloiy', 'Fedorov', '0991234756', 'C++17')]
# список Teacher-ов
teachers = [Teacher('Olena', 'Vilka', 'trinolyatrulyalya2', 'English'),
            Teacher('Oksana', 'Shmaly', '0991234756', 'Programming')]

# запишем список персонов в json-файл
with open("persons.json", 'w') as pj:
    json.dump([p.to_json_dict() for p in persons], pj)
# прочтем список персонов из json-файла и выведем в консоль
with open("persons.json", "r") as pj:
    person_dict_list = json.load(pj)
    person_list = [Person.from_json_dict(pd) for pd in person_dict_list]
    print(person_list)

print("+++++++++++++++++++++++++++++")
# создадим группу
group = Group(teachers, students)
# выведем группу в консоль
print(group)
# выведем группу в консоль в json-представлении
print(group.to_json_str())
# запишем группу в json-файл
group.to_json_file("group.json", indent=4)
# прочтем группу из json-файла и выведем в консоль
group_from_json = Group.from_json_file("group.json")
print(group_from_json)
# прочтем группу из json-файла вторым способом и выведем в консоль
with open("group.json", "r") as json_file:
    g_from_j_str = Group.from_json_str(json_file.read())
    print(g_from_j_str)
