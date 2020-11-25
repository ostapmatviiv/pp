#LAB4
I used ```pyenv``` and ```poetry```.
Python version 3.8.2


There are some steps that you want to use:

- Using pyenv install current version of python:
```
pyenv install 3.8.2
pyenv local 3.8.2
```

- Install poetry:

```
pip install poetry waitress
```

- Run server:

```
poetry run python wsgi.py
```