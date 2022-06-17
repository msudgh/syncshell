from halo import Halo


class Spinner:
    __spinner = None

    def __init__(self, text, spinner='dots'):
        self.__spinner = Halo(text=text, spinner=self.__spinner)
        self.__spinner.start()

    def succeed(self, text):
        self.__spinner.succeed(text)
        self.__spinner.stop()

    def fail(self, text):
        self.__spinner.fail(text)
        self.__spinner.stop()
