from enum import Enum


class ErrorMSG(str, Enum):
    EXIST = 'Проект с таким именем уже существует!'
    NOT_FOUND = 'Проект не найден!'
    INVESTED = 'В проект были внесены средства, не подлежит удалению!'
    BELOW_DEPOSIT = 'Нелья установить значение full_amount меньше уже вложенной суммы.'
    CLOSED = 'Закрытый проект нельзя редактировать!'
    NO_NAME = 'Имя проекта не может быть пустым!'
    NO_DESCRIPTION = 'Описание проекта не может быть пустым!'