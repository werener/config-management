import tomllib as toml

with open("config.TOML", 'rb') as file:
    a = toml.load(file)    
print(a)