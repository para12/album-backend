from graphene import ObjectType, List, Field, String
from graphene_django import DjangoObjectType

from graphql_auth import mutations

from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields= '__all__'

# class UserQuery(ObjectType):
#     Argument : 

class AllUsers(ObjectType) :
    all_users = List(UserType)
    def resolve_all_users(root, info):
        return User.objects.all()

class Me(ObjectType):
    me = Field(UserType)
    def resolve_me(root, info):
        if info.context.user.is_authenticated:
            return info.context.user
        else:
            return None

class UserByName(ObjectType):
    user_by_name = Field(UserType, username = String())
    def resolve_user_by_name(root, info, username):
        return User.objects.get(username = username)

class AuthQuery(AllUsers, Me, UserByName):
    pass


class AuthMutation(ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()