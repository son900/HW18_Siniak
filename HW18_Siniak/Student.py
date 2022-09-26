from Person import Person


class Student(Person):
    __group = ""

    def __init__(self, firstname: str, lastname: str, phone: str, group: str):
        super().__init__(firstname, lastname, phone)
        self.set_group(group)

    def get_group(self) -> str:
        return self.__group

    def set_group(self, group: str):
        self.__group = group

    # возвращает представление объекта класса в виде словаря (например, для последующей передачи его в json.dump())
    def to_json_dict(self) -> dict:
        person_dict = super().to_json_dict()
        person_dict.update({"group": self.__group})
        return person_dict

    # принимает словарь описывающий объекта класса, возвращает объект класса (метод обратный к to_json_dict())
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> 'Student':
        if json_dict["class_name"] == cls.__name__:
            return cls(json_dict["firstname"], json_dict["lastname"], json_dict["phone"], json_dict["group"])
        else:
            raise ValueError(f"{json_dict['class_name']} is not possible to recognize as {cls.__name__}")
