from flask import (
Flask, redirect,
render_template,
request,
flash,
url_for,
get_flashed_messages
)
from validator import validate
import json

app = Flask(__name__)
app.secret_key = "secret_key"



@app.route('/')
def index():
    return redirect(url_for('get_user'))

@app.route('/users')
def get_user():
    term = request.args.get('term')
    messages = get_flashed_messages(with_categories=True)
    with open('users.json') as f:
        users_data = f.read()
        users = json.loads(users_data)
    if term:
        filtered_users = {k:v for (k, v) in users.items() if str(term) in users[k][0]}
    else:
        filtered_users = users
    return render_template(
        'users/index.html',
        users=filtered_users,
        search=term,
        messages=messages,
    )


@app.route('/users/<id>')
def get_users(id):
    with open('users.json') as f:
        users_data = f.read()
        users = json.loads(users_data)
    for userid, data in users.items():
        if userid == id:
            nickname = data[0]
            email = data[1]
            break
    return render_template(
        '/users/show.html',
        id=id,
        name=nickname,
        email=email
    )

@app.route('/users/<id>/edit') #СТРАНИЦА РЕДАКТИРОВАНИЯ ПОЛЬЗОВАТЕЛЯ
def edit_user(id):
    with open('users.json') as f:
        users_data = f.read()
        users = json.loads(users_data)
    for userid, data in users.items():
        if userid == id:
            nickname = data[0]
            email = data[1]
            break
    errors = []

    return render_template(
           'users/edit.html',
            id=id,
            name=nickname,
            email=email,
            errors=errors,
        )

# ОБРАБОТЧИК РЕДАКТИРОВАНИЯ ПОЛЬЗОВАТЕЛЯ
@app.route('/users/<id>/patch', methods=['POST'])
def patch_user(id):
    with open('users.json') as f:
        users_data = f.read()
        users_dict = json.loads(users_data)
    user = request.form.to_dict()
    print(f'base: {users_dict}')
    print(user)
    errors = validate(users_dict, user)
    print(errors)
    if errors:
        return render_template(
          'users/edit.html',
            id=id,
          user=user,
          errors=errors,
        ), 422

    flash('User updated sucessfully!', 'success')

    users_dict[id] = [user.get('name'), user.get('email')]
    with open('users.json', 'w') as f:
        f.writelines(f'{json.dumps(users_dict)}')
    return redirect(url_for('get_users', id=id), code=302)

@app.route('/users/new')
def users_new():
    user = {'nickname': '',
            'email': '',}
    errors = {}

    return render_template(
        'users/new.html',
        user=user,
        errors=errors
    )

# ОБРАБОТЧИК РЕГИСТРАЦИИ НОВОГО ПОЛЬЗОВАТЕЛЯ
@app.post('/users/new-user')
def post_user():

    with open('users.json') as f:
        users_data = f.read()
        users_dict = json.loads(users_data)

    user = request.form.to_dict()
    errors = validate(users_dict, user)
    if errors:
        return render_template(
          '/users/new.html',
          user=user,
          errors=errors,
        ), 422

    flash('New user registrated sucessfully!', 'success')
    id = len(users_dict) + 1
    users_dict[id] = [user.get('nickname'), user.get('email')]
    with open('users.json', 'w') as f:
        f.writelines(f'{json.dumps(users_dict)}')
    return redirect(url_for('get_user'), code=302)


