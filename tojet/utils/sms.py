import random
import string


def generate_otp_code(digit_count: int) -> str:
    """
    Generate a One-Time Password (OTP) code with the specified number of digits.

    :param digit_count: Number of digits in the OTP code.
    :return: A string representing the OTP code.
    """
    code = ''.join(random.choices(string.digits, k=digit_count))
    return code
