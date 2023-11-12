def validate(database, user):
    errors = {}
    names = [v[0] for (k,v) in database.items()]
    print(f'names: {names}')
    if user.get('name') in names:
        print(f"nick: {user.get('nickname')}")
        errors['nickname'] = "nickname in database!"

    if not user.get('email'):
        result['email'] = "Can't be blank"
    return errors

"""
user = {
    'nickname': 'alex',
    'email': 'a@a'
    }
"""