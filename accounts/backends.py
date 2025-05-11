# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         if username is None:
#             username = kwargs.get('email')  # Try 'email' as a fallback
#         try:
#             user = UserModel.objects.get(email=username)  # changed from username to email
#         except UserModel.DoesNotExist:
#             return None  # Or raise an exception if you prefer
#         else:
#             if user.check_password(password):
#                 return user
#         return None

#     def get_user(self, user_id):
#         UserModel = get_user_model()
#         try:
#             return UserModel.objects.get(pk=user_id)
#         except UserModel.DoesNotExist:
#             return None