from Person import Person


class Teacher(Person):
    __subject = ""

    def __init__(self, firstname: str, lastname: str, phone: str, subject: str):
        super().__init__(firstname, lastname, phone)
        self.set_subject(subject)

    def get_subject(self) -> str:
        return self.__subject

    def set_subject(self, subject: str):
        self.__subject = subject

    # возвращает представление объекта класса в виде словаря (например, для последующей передачи его в json.dump())
    def to_json_dict(self) -> dict:
        person_dict = super().to_json_dict()
        person_dict.update({"subject": self.__subject})
        return person_dict

    # принимает словарь описывающий объекта класса, возвращает объект класса (метод обратный к to_json_dict())
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> 'Teacher':
        if json_dict["class_name"] == cls.__name__:
            return cls(json_dict["firstname"], json_dict["lastname"], json_dict["phone"], json_dict["subject"])
        else:
            raise ValueError(f"{json_dict['class_name']} is not possible to recognize as {cls.__name__}")
