from core import *


class User(Base):
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    def check_adult(self):
        adult = {self.age >= 18}
        return {'first_name': self.first_name, 'last_name': self.last_name, 'age': self.age, 'adult': adult}



