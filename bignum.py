class BigNum:
    """A generic class for operations with big numbers"""

    _maximum_digits = 1000

    def __digits_count(self):
        return len(self.__arr_digits)

    def __reset(self):
        self.__arr_digits = []  # internal representation - array of digits

    def __check_digits(self, nr_digits, err: Exception = "Maximum digits count reached!"):
        if nr_digits > self._maximum_digits:
            raise err

    def __from_int(self, value: int):
        assert isinstance(value, int), "Value is not int!"
        assert value >= 0

        self.__check_digits(len(str(value)))

        self.__reset()

        if value == 0:
            self.__arr_digits.append(0)
            return
        while value > 0:
            self.__arr_digits.append(value % 10)
            value //= 10

    def __from_string(self, value: str):
        assert isinstance(value, str), "Value is not str!"

        self.__check_digits(len(value))

        self.__reset()

        try:
            for el in value[::-1]:
                self.__arr_digits.append(int(el))
        except ValueError:
            assert True, "Invalid numeric string!"

    def __from_array(self, value: list):
        assert isinstance(value, list), "Value is not list!"

        self.__check_digits(len(value))

        self.__reset()

        try:
            for el in value:
                self.__arr_digits.append(int(el))
        except ValueError:
            assert True, "Invalid list value!"

    def __from_bignum(self, value):
        assert isinstance(self, BigNum)
        self.__arr_digits = value.__arr_digits.copy()

    @staticmethod
    def __normalize_arrays(arr1_, arr2_):
        if len(arr1_) != len(arr2_):
            if len(arr1_) > len(arr2_):
                arr2_ = arr2_ + [0] * (len(arr1_) - len(arr2_))
            else:
                arr1_ = arr1_ + [0] * (len(arr2_) - len(arr1_))
        return arr1_, arr2_

    def __trim_zeroes(self):
        tmp = self.__arr_digits[-1:] == 0
        while self.__digits_count() > 1 and self.__arr_digits[-1] == 0:
            self.__arr_digits.pop()
        return self

    def __init__(self, value):
        if isinstance(value, int):
            self.__from_int(value)
        elif isinstance(value, str):
            self.__from_string(value)
        elif isinstance(value, list):
            self.__from_array(value)
        elif isinstance(value, BigNum):
            self.__from_bignum(value)
        else:
            raise "Invalid value type!"

    def __eq__(self, other):
        other = BigNum(other)
        return \
            self.__digits_count() == other.__digits_count() and \
            all([self.__arr_digits[i] == other.__arr_digits[i] for i in range(self.__digits_count())])

    def __ne__(self, other):
        other = BigNum(other)
        return not self.__eq__(other)

    def __gt__(self, other):
        other = BigNum(other)
        if self.__digits_count() != other.__digits_count():
            return self.__digits_count() > other.__digits_count()
        for i in range(self.__digits_count() - 1, -1, -1):
            if self.__arr_digits[i] > other.__arr_digits[i]:
                return True
            elif self.__arr_digits[i] < other.__arr_digits[i]:
                return False
        return False

    def __ge__(self, other):
        other = BigNum(other)
        return not self < other

    def __lt__(self, other):
        other = BigNum(other)
        return other.__gt__(self)

    def __add__(self, other):
        other = BigNum(other)

        def __add_eq_len_arrays(arr1_, arr2_):
            result = []
            remainder = 0
            for i in range(len(arr1_)):
                res = arr1_[i] + arr2_[i] + remainder
                result.append(res % 10)
                remainder = res // 10
            if remainder:
                result.append(remainder)
            return result

        __result = __add_eq_len_arrays(*BigNum.__normalize_arrays(self.__arr_digits, other.__arr_digits))

        return BigNum(__result).__trim_zeroes()

    def __sub__(self, other):
        other = BigNum(other)
        assert self >= other, "Invalid sub operation!"

        def __sub_eq_len_arrays(arr1_, arr2_):
            result = []
            remainder = 0
            for i in range(len(arr1_)):
                res = arr1_[i] - arr2_[i] - remainder
                remainder = 0
                if res < 0:
                    res += 10
                    remainder = 1
                result.append(res)
            assert remainder == 0, "Negative result!"
            return result

        __result = __sub_eq_len_arrays(*BigNum.__normalize_arrays(self.__arr_digits, other.__arr_digits))

        return BigNum(__result).__trim_zeroes()

    def __mul__(self, other):
        other = BigNum(other)
        if self == BigNum(0) or other == BigNum(0):
            return BigNum(0)

        def __mul_arrays(arr1_, arr2_):
            """ Compute arr1 * arr2 """
            result = [0] * (len(arr1_) + len(arr2_))
            for j in range(len(arr2_)):
                remainder = 0
                for i in range(len(arr1_)):
                    res = arr1_[i] * arr2_[j] + remainder
                    res += result[i + j]
                    result[i + j] = res % 10
                    remainder = res // 10
                if remainder:
                    result[len(arr1_) + j] += remainder
            return result

        # optimize -- biggest array/number first
        arr1, arr2 = [self.__arr_digits, other.__arr_digits] \
            if self.__digits_count() >= other.__digits_count() \
            else [other.__arr_digits, self.__arr_digits]

        __result = __mul_arrays(arr1, arr2)

        return BigNum(__result).__trim_zeroes()

    @staticmethod
    def __internal_pow(n, p):
        if p == 0:
            return BigNum(1)
        if p == 1:
            return BigNum(n)
        if p.__arr_digits[0] % 2 == 0:
            return BigNum.__internal_pow(n * n, p // 2)
        return n * BigNum.__internal_pow(n * n, p // 2)

    def __pow__(self, power, modulo=None):
        power = BigNum(power)
        if power == 0:
            return 1
        if power == 1:
            return BigNum(self.__arr_digits)  # copy
        res = BigNum.__internal_pow(self, power)
        assert res >= self
        return res

    def __mod__(self, other):
        other = BigNum(other)
        assert other > 0, "Invalid modulo operand!"
        res = self - (self // other) * other
        assert res < other
        return res

    def __floordiv__(self, other):
        """ long division """
        a = self
        b = BigNum(other)

        assert b != 0, "Division by 0!"

        if a <= BigNum(0):
            return BigNum(0)

        __q_array = [0] * a.__digits_count()
        r = BigNum(0)

        for i in range(a.__digits_count())[::-1]:
            r = r * 10 + a.__arr_digits[i]
            while r >= b:
                __q_array[i] += 1
                r -= b

        return BigNum(__q_array).__trim_zeroes()

    def sqrt(self):
        n = BigNum(self.__arr_digits)  # copy
        if n < 2:
            return n

        def __internal_sqrt(n_: BigNum):
            if n_ < 2:
                return n_
            start, stop = BigNum(1), n_ // 2
            while start <= stop:
                m = (start + stop) // 2
                sq = m * m
                sq1 = (m+1) * (m+1)
                if sq == n_ or (sq < n_ < sq1):
                    return m
                elif sq < n_:
                    start = m + 1
                else:
                    stop = m - 1

        def __find_d(p_: BigNum, r_: BigNum):
            """ find the greatest digit d such that ((2p)|d) * d ≤ r """
            n_ = p_ * 2
            tmp_num = BigNum(n_)
            tmp_num.__arr_digits.insert(0, 0)  # *= 10
            for d_ in range(0, 10):
                tmp_num.__arr_digits[0] = d_
                if tmp_num * d_ <= r_:
                    if d_ != 9:
                        if (tmp_num + 1) * (d_ + 1) <= r_:
                            continue
                    return d_, tmp_num * d_

        # pad with zero to have pairs of 2, if needed
        if n.__digits_count() % 2 == 1:
            n.__arr_digits.append(0)

        r = BigNum(n.__arr_digits[-1] * 10 + n.__arr_digits[-2])
        p = __internal_sqrt(r)
        r = r - (p * p)

        if n.__digits_count() > 2:
            for i in range(0, n.__digits_count(), 2)[:-1][::-1]:
                r = r * 100 + n.__arr_digits[i + 1] * 10 + n.__arr_digits[i]
                d, tmp_r = __find_d(p, r)
                p.__arr_digits.insert(0, 0)  # *= 10
                p.__arr_digits[0] = d
                r -= tmp_r  # r -= ((2p)|d * d)

        res = p

        assert res * res <= self < (res+1) * (res+1)

        return res

    def __str__(self):
        return "".join(str(el) for el in self.__arr_digits[::-1])

    @classmethod
    def exponent(cls, value = None):
        """Getter and setter for maximum digits class variable"""
        
        if value is None:
            return cls._maximum_digits

        if value == 0:
            raise Exception("invalid exponent value")

        cls._maximum_digits = value 


if __name__ == '__main__':
    """ Small Tests """
    a, b = BigNum("2"), BigNum(31)
    # print(a+b)
    # print(a-b)
    # print(a*b)
    # print(a//b)
    # print(a**b)
    # assert BigNum("50965321").sqrt() == 7139
    # assert BigNum("2989441").sqrt() == 1729
    # print(BigNum("12319023812011111111111111111948032589340697450657430693405").sqrt())
    print(BigNum("123190238120111111111111").sqrt())
    print(BigNum("12319023812011111111111").sqrt())
    assert BigNum("12319023812011111111111").sqrt() == 110991097895
    assert BigNum("123190238120111111111111").sqrt() == 350984669351
    # assert BigNum("1231902381201111111111").sqrt() == 35098466935


