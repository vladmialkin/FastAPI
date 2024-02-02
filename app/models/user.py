from core import *


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int

    def check_adult(self):
        adult = {self.age >= 18}
        return {'first_name': self.first_name, 'last_name': self.last_name, 'age': self.age, 'adult': adult}



