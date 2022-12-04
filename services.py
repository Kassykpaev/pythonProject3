import datetime

from models import get_all_users
from google_configs import client


async def add_fist_row(sheet):
    row = ["id", "name", "age", "phone_number", "username"]
    sheet.insert_row(row, 1)


async def create_row_from_user(user):
    return [user.id, user.name, user.age, user.phone_number, user.username]


async def add_row(index, user, sheet):
    if not user.is_in_lottery:
        return
    sheet.insert_row(await create_row_from_user(user), index)


async def create_google_table(users):
    sheet = client.create(datetime.datetime.now().timestamp()).sheet1
    client.insert_permission(file_id=sheet.spreadsheet.id, role='writer', value=None,
                             with_link=True, perm_type='anyone')
    await add_fist_row(sheet)
    for index, user in enumerate(users):
        await add_row(index+2, user, sheet)
    return sheet


async def create_table_link():
    users = await get_all_users()
    sheet = await create_google_table(users)
    return sheet.spreadsheet.url
