import os


if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

test2= os.environ.get("FLASK_CONFIG")
tester=os.environ.get("API_KEY")
print(test2)
print(tester)
