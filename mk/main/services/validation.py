from typing import Any, Literal, Tuple
from main.models import MyUser
from main.serializers import SignUpSerializer

def merge_dicts(serializer_errors:dict, signup_data_errors:dict):
    result = serializer_errors.copy()
    result.update(signup_data_errors)
    return result

def create_user(serializer: SignUpSerializer):
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    gender = serializer.validated_data['gender']
    my_extra_fields = {
        'last_name': serializer.validated_data['last_name'],
        'first_name': serializer.validated_data['first_name'],
        'middle_name': serializer.validated_data['middle_name'],
    }
    user: MyUser = MyUser.objects.create_user(email = email, password=password, **my_extra_fields)
    user.gender = gender
    user.save()
    return user

class SignUpValidator:

    def __init__(self, data: dict) -> None:
        self.data = data
        self.errors = []
        self.raw_data = data

    def is_valid(self) -> Tuple[bool, dict]:
        errors = self.validate()
        if type(errors) != dict:
            return False, self.raw_data
        return True, self.data

    def validate(self) -> list[dict[Literal['error'], Any]] | bool:
        pswd1 = self.data['password1'].strip()
        pswd2 = self.data['password2'].strip()
        gender = self.data['gender'].strip()
        admission: str | None = self.data.get('admission')
        faculty: str | None = self.data.get('faculty')
        study_group: str | None = self.data.get('group')
        type: str | None = self.data.get('type')
        birth_place: str | None = self.data.get('birth_place')
        if admission != None and faculty != None and study_group != None and type != None and birth_place != None:
            self.data['make_student'] = True
            type = type.lower()

        if gender != 'M' and gender != 'F':
            self.errors.append({'error': 'Неправильно указан Ваш пол'})
        if pswd1 != pswd2 and pswd2 != pswd1:
            self.errors.append({'error': 'Пароли не совпадают'})
        else:
            password = pswd2
            self.data.pop('password1')
            self.data.pop('password2')
            self.data['password'] = password

        if len(self.errors) == 0:
            return self.data
        else:
            return self.errors