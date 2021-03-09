class LowTempException(Exception):
    def __init__(self, text):
        print('Выход за минимальную температуру, вещества : ', text)


class HighTempException(Exception):
    def __init__(self, text):
        print('Выход за максимальную температуру, вещества : ', text)
