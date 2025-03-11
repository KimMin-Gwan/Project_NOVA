import re


def check_password_format(password: str) -> bool:
    pattern = re.compile(
        r'^(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$'
    )
    return bool(pattern.match(password))
    
    
print(check_password_format('qadalasdfl15!@'))


    