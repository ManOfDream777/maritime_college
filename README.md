
# Maritime college
## Site was developed for Maritime college in Novorossyisk.



## Tech Stack

**Client:** Pure JS, HTML5, CSS3

**Server:** Django, DRF


## Installation and start

```bash
  https://github.com/Urodec777/maritime_college.git
```
Next step is creating venv
```bash
  python3 -m venv *your venv name*
```
Install all requirements from `requirements.txt` file

```
cd mk/
```
Then `python manage.py makemigrations` then `python manage.py migrate` 
_____
`python manage.py runserver` to start server.

Enjoy :blush:



## Features

- DRF + pure JS
- Cross platform
- Custom Login / Sign up implementation



## API Reference
#### Part of available API endpoints

#### Get seniors list (this info displaying in `seniors/` path)

```http
  GET api/senior_staff/<int:id>/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | **Required**. ID of senior group |


#### Auth (Login / Sign Up)

```http
  POST api/auth/
```

### SIGN UP

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `marker` (send with headers request) | `string` | **Required**. sign up |
| `first_name`      | `string` | **Required**. First name |
| `last_name`      | `string` | **Required**. Last name|
| `middle_name`      | `string` | **Required**. Middle name |
| `email`      | `email` | **Required**. Email |
| `gender`      | `string` | **Required**. Gender |
| `password1`      | `string` | **Required**. Password1 |
| `password2`      | `string` | **Required**. Password2 |
| `faculty`      | `string` | **Optional**. Faculty |
| `group`      | `string` | **Optional**. group |
| `type`      | `string` | **Optional**. Type |
| `admission`      | `string` | **Optional**. Admission |
| `birth_place`      | `string` | **Optional**. Birth place |


### LOGIN

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `marker` (send with headers request) | `string` | **Required**. login |
| `email`      | `email` | **Required**. Email |
| `password`      | `string` | **Required**. Password|


#### Logout
```http
  GET /api/logout/
```

#### Create request to contact with user

```http
  POST /api/contact_create/
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `first_name`      | `string` | **Required**. First name |
| `last_name`      | `string` | **Required**. Last name |
| `email`      | `email` | **Required**. Email |
| `subject`      | `string` | **Required**. Subject |
| `body`      | `string` | **Required**. Body |



