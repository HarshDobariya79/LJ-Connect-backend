from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from data.models import StaffDetail, StudentSemesterRecord

class is_active_staff(BaseAuthentication):

    def authenticate(self, request):
        
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            raise AuthenticationFailed('Authorization header missing.')

        auth_token = auth_header.split(' ')
        if len(auth_token) != 2 or auth_token[0] != 'Bearer':
            raise AuthenticationFailed('Invalid authorization header.')

        token = auth_token[1]

        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)

            user = jwt_authentication.get_user(validated_token)

            staff_data = StaffDetail.objects.filter(email=user.email, active=True)

            if not staff_data:
                raise AuthenticationFailed("Access not allowed.")

            return (user, None)

        except AuthenticationFailed as e:
            raise e
        except Exception:
            raise AuthenticationFailed('Something went wrong')

class is_active_student(BaseAuthentication):
    
    def authenticate(self, request):
        
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            raise AuthenticationFailed('Authorization header missing.')

        auth_token = auth_header.split(' ')
        if len(auth_token) != 2 or auth_token[0] != 'Bearer':
            raise AuthenticationFailed('Invalid authorization header.')

        token = auth_token[1]

        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)

            user = jwt_authentication.get_user(validated_token)

            student_obj = StudentSemesterRecord.objects.filter(student__email=user.email, student__graduated=False)
            print(student_obj)

            if not student_obj:
                raise AuthenticationFailed("Access not allowed.")
        
            return (user, None)

        except AuthenticationFailed as e:
            raise e
        except Exception:
            raise AuthenticationFailed('Something went wrong.')
