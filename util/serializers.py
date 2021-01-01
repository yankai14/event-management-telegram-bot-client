from marshmallow import Schema, fields, INCLUDE
from marshmallow.validate import Regexp
from util.errors import ValidationError
from util.enums import Constant


class RegistrationSerializer(Schema):

    username = fields.Int(required=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    password = fields.Str(required=True)

    def dump(self, obj):
        obj = {Constant(k).name.lower(): v for k,v in obj.items()}
        errors = self.validate(obj)
        if errors:
            raise ValidationError(details=errors, message="Invalid fields given")

        return super().dump(obj)


class LoginSerializer(Schema):

    username = fields.Int(required=True)
    password = fields.Str(required=True, validate=[
            Regexp(regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", error="Password must be minimum eight characters, at least one letter and one number"),
        ]
    )

    def dump(self, obj):
        obj = {Constant(k).name.lower(): v for k,v in obj.items()}
        errors = self.validate(obj)
        if errors:
            raise ValidationError(details=errors, message="Password must be minimum eight characters, at least one letter and one number")

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