from setuptools import setup

setup(
    name="add_new_quotes",
    version='0.1',
    py_modules=['add_new_quotes'],
    install_requires=[
        'Click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        add_new_quote=add_new_quotes:add_new_quote
        get_number_of_quotes=add_new_quotes:get_number_of_quotes
    ''',
)