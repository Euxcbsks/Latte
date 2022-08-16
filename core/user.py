from core.data import UserData


class User:
    def __init__(self, user_data: UserData) -> None:
        self.__data = user_data

    def UserData(self, **update):
        return UserData.from_items(self.__data.items | update)
