import json
from copy import deepcopy
from typing import Type, TypeVar, Optional, Generic

from Person import Person
from Student import Student
from Teacher import Teacher

T = TypeVar("T", bound="Person")


# дескриптор для полей класса Group
class PersonListDescriptor(Generic[T]):
    __p_type: Type[T]  # хранит тип основного аргумента

    def __init__(self, param_type: Type[T], param_value: Optional[list[T]] = None):
        if param_value is None:
            param_value = []
        self.__p_type = param_type
        self.__param = param_value  # основной аргумент

    # геттер возвращает копию списка объектов
    def __get__(self, instance, owner) -> list[T]:
        return deepcopy(self.param)

    # сеттер устанавливает значение атрибута,
    # проверяя является ли передаваемое значение списком объектов такого же типа, что и тип атрибута(__p_type)
    def __set__(self, instance, value: list[T]):
        if type(value) is list:
            all_odj_is_correct = True
            wrong_type: Type[Optional[Person]] = type(None)
            for obj in value:
                if not (type(obj) is self.__p_type):
                    wrong_type = type(obj)
                    all_odj_is_correct = False
                    break
            if all_odj_is_correct:
                self.param = value
            else:
                raise TypeError(f"a list[{self.__p_type}] was expected, but list[{wrong_type}] was given")
        else:
            raise TypeError(f"a list was expected, but {type(value)} was received")


class Group:
    teachers = PersonListDescriptor(Teacher)
    students = PersonListDescriptor(Student)

    def __init__(self, teachers: list[Teacher], students: list[Student]):
        self.teachers = teachers  # список объектов класса Teacher
        self.students = students  # список объектов класса Student

    def __str__(self):
        return f"Group:\n\tTeachers: {self.teachers}\n\tStudents: {self.students}"

    # возвращает представление объекта класса в виде словаря (например, для последующей передачи его в json.dump())
    def to_json_dict(self) -> dict:
        group_dict = {"class_name": self.__class__.__name__,
                      "teachers": [Teacher.to_json_dict(teacher) for teacher in self.teachers],
                      "students": [Student.to_json_dict(student) for student in self.students]}
        return group_dict

    # принимает словарь описывающий объекта класса, возвращает объект класса (метод обратный к to_json_dict())
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> 'Group':
        if json_dict["class_name"] == cls.__name__:
            return cls([Teacher.from_json_dict(teach) for teach in json_dict["teachers"]],
                       [Student.from_json_dict(stud) for stud in json_dict["students"]])
        else:
            raise ValueError(f"{json_dict['class_name']} is not possible to recognize as {cls.__name__}")

    # возвращает строку, соответствующую json-представлению объекта класса
    def to_json_str(self) -> str:
        group_dict = self.to_json_dict()
        return json.dumps(group_dict)

    # принимает строку, соответствующую json-представлению объекта класса, возвращает объект класса
    @classmethod
    def from_json_str(cls, json_str: str) -> 'Group':
        json_dict = json.loads(json_str)
        if isinstance(json_dict, dict):
            return cls.from_json_dict(json_dict)
        else:
            raise ValueError(f"{json_dict} cannot be converted to a dictionary")

    # записывает json-представление объекта класса в файл с именем file
    def to_json_file(self, file: str, mode="w", indent: None | int | str = None) -> None:
        with open(file, mode) as jf:
            json.dump(self.to_json_dict(), jf, indent=indent)

    # принимает имя файла с json-представление объекта класса, возвращает объект класса
    @classmethod
    def from_json_file(cls, file: str) -> 'Group':
        with open(file, "r") as jf:
            json_dict = json.load(jf)
            if isinstance(json_dict, dict):
                return cls.from_json_dict(json_dict)
            else:
                raise ValueError(f"{json_dict} cannot be converted to a dictionary")
