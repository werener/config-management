import tomllib as toml
import validators
import re

KEYS = {'name', 'url', 'test_repos', 'version', 'title_graph', 'substring'}

def validate(package: dict):
    def force_type(parameter, type_):
        parameter_type = type(parameter)
        if parameter_type is not type_:
            raise TypeError(f"{parameter} should be a {repr(type)}, not '{repr(parameter_type)}'")
        

    for k in package.keys():
        if k not in KEYS:
            raise ValueError(f"'{k}' is not a configurable parameter")
    for k in KEYS:
        if k not in package.keys():
            raise ValueError(f"'{k}' was not provided")
        

    for k in KEYS:
        parameter = package[k]
        match(k):
            case 'name':
                force_type(parameter, str)
            case 'url':
                if not validators.url(parameter):
                    raise ValueError(f"URL for this package is invalid: '{parameter}'")
            case 'test_repos':
                force_type(parameter, bool)
            case 'version':
                force_type(parameter, str)
                if not re.match(r'\d+\.\d+(|\.|\.\d+)$', parameter):
                    raise ValueError(f"Version should have format x.x.x or x.x. or x.x not {parameter}")
            case 'title_graph':
                force_type(parameter, str)
                if not(parameter.endswith('.jpeg') or parameter.endswith('.png')):
                    raise ValueError(f"Image type should be .jpeg or .png on {parameter}")
            case 'substring':
                force_type(parameter, str)
i = ""
while (True):
    i = input("Choose which config to test: ")
    if (i == 'q'):
        break
    with open(f"config{i}.TOML", 'rb') as file:
        a = toml.load(file)    
    package = a['package']
    print("Contents of your file:")
    for k in package.keys():
        print(k, package[k], sep=':\t')

    try:
        validate(package)
        print('\nValidation was succesful')
    except Exception as e:
        print(f"\nValidation raised an error:\n{e}")
    
    print('-'*25)