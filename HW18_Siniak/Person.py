import functools
import json
from typing import TypeVar, Type


class Person:
    __firstname: str
    __lastname: str
    __phone: str

    def __init__(self, firstname: str, lastname: str, phone: str):
        self.set_firstname(firstname)
        self.set_lastname(lastname)
        self.set_phone(phone)

    def get_firstname(self):
        return self.__firstname

    def get_lastname(self):
        return self.__lastname

    def get_phone(self):
        return self.__phone

    def set_firstname(self, firstname: str):
        self.__firstname = firstname.capitalize()

    def set_lastname(self, lastname: str):
        self.__lastname = lastname.capitalize()

    def set_phone(self, phone: str):
        self.__phone = phone

    def __str__(self) -> str:
        attr_values_list = [self.__getattribute__(attr) for attr in self.__dict__.keys()]
        return f'{self.__class__.__name__} {functools.reduce(lambda x, y: str(x) + " " + str(y), attr_values_list)}'

    def __repr__(self) -> str:
        attr_pair_list = [attr + ": " + str(self.__getattribute__(attr)) for attr in self.__dict__.keys()]
        return f'{self.__class__.__name__} {functools.reduce(lambda x, y: x + "    " + y, attr_pair_list)}'

    def to_file(self, filename: str):
        with open(filename, 'a') as file:
            file.write(self.__str__() + '\n')

    T = TypeVar("T", bound="Person")

    @classmethod
    # def from_file(cls: Type["Person"], filename: str) -> list[Union["Person", "Student", "Teacher"]]:
    def from_file(cls: Type[T], filename: str) -> list[T]:
        new_objs = []
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                values = line.split()
                obj_cls, args = values[0], values[1:]
                if cls.__name__ == obj_cls:
                    new_objs.append(cls(*args))
        return new_objs

    # возвращает представление объекта класса в виде словаря (например, для последующей передачи его в json.dump())
    def to_json_dict(self) -> dict:
        person_dict = {"class_name": self.__class__.__name__,
                       "firstname": self.__firstname,
                       "lastname": self.__lastname,
                       "phone": self.__phone}

        return person_dict

    # принимает словарь описывающий объекта класса, возвращает объект класса (метод обратный к to_json_dict())
    @classmethod
    def from_json_dict(cls: Type[T], json_dict: dict) -> T:
        if json_dict["class_name"] == cls.__name__:
            return cls(json_dict["firstname"], json_dict["lastname"], json_dict["phone"])
        else:
            raise ValueError(f"{json_dict['class_name']} is not possible to recognize as {cls.__name__}")

    # возвращает строку, соответствующую json-представлению объекта класса
    def to_json_str(self) -> str:
        person_dict = self.to_json_dict()
        print(person_dict)
        return json.dumps(person_dict)

    # принимает строку, соответствующую json-представлению объекта класса, возвращает объект класса
    @classmethod
    def from_json_str(cls: Type[T], json_str: str) -> T:
        json_dict = json.loads(json_str)
        if isinstance(json_dict, dict):
            return cls.from_json_dict(json_dict)
        else:
            raise ValueError(f"{json_dict} cannot be converted to a dictionary")
