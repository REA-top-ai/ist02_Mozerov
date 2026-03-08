long_string=lambda my_string: 'true' if len(my_string)>12 else 'false'
print(long_string('Hello World DDDDDD?'))
print(long_string('lol'))