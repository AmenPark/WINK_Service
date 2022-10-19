import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class IncludeNumberValidator(object):
    def validate(self, password, user=None):
        if not(re.search(r'\d',password )):
            raise ValidationError("No digit", code="no_digit")
class OnlyNumAlphSpecialValidator(object):
    def validate(self,password,user=None):
        if re.search(r'[^a-zA-Z\d!@#$%^&*]', password):
            raise ValidationError("Only digit, alphabets, !@#$%^&* available", code="bad_char")
class IncludeSpecialValidator(object):
    def validate(self,password,user=None):
        if not(re.search(r'[!@#$%^&*]', password)):
            raise ValidationError("No Special mark", code="no_special")


