from graphene import ObjectType, List
from graphene_django import DjangoObjectType

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from graphql_auth import mutations

from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields= '__all__'

class AuthQuery(UserQuery, MeQuery, ObjectType):
    all_users = List(UserType)
    def resolve_all_users(root, info):
        return User.objects.all()

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