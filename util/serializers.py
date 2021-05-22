from types import FunctionType
from marshmallow import Schema, fields, INCLUDE
from util.errors import ValidationError
class RegistrationSerializer(Schema):

    username = fields.Int(required=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    password = fields.Str(required=True)

    def dump(self, obj, callback: FunctionType):
        errors = self.validate(obj)
        if errors:
            raise ValidationError(details=errors, message="Invalid fields given, please update your information", callback=callback)
        return super().dump(obj)


class LoginSerializer(Schema):

    username = fields.Int(required=True)
    password = fields.Str(required=True)

    def dump(self, obj, callback: FunctionType):
        errors = self.validate(obj)
        if errors:
            raise ValidationError(details=errors, message=errors, callback=callback)

        return super().dump(obj)


class EnrollmentSerializer(Schema):

    username = fields.Int(required=True)
    eventInstanceCode = fields.Str(required=True)
    role = fields.Int(required=True)

    class Meta:
        unknown = INCLUDE

    def dump(self, obj):
        errors = self.validate(obj)
        if errors:
            raise ValidationError(details=errors, message=errors)

        dataRequired = {
            "username": obj.get("username"),
            "eventInstanceCode": obj.get("eventInstanceCode"),
            "role": obj.get("role")
        }

        return super().dump(dataRequired)