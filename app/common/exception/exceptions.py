class SecretManagerCannotBeReachedException(Exception):

    def __str__(self):
        return 'Secret manager cannot be reached. Verify your input data'


class EnvironmentalVariableNotSetException(Exception):
    variable_name: str

    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def __str__(self):
        return f'The environmental variable \'{self.variable_name}\' isn\'t set'
