class Calculator:
    def _check_val(self, val):
        if not isinstance(val, (int, float)):
            raise TypeError("Переменные должны быть int или float")
        return True

    def divine(self, x, y):
        if self._check_val(x) and self._check_val(y):
            if y == 0:
                raise ZeroDivisionError("Вторая переменная не может быть 0")
            return x / y

    def add(self, x, y):
        if self._check_val(x) and self._check_val(y):
            return x + y


if __name__ == '__main__':
    calculator = Calculator()
