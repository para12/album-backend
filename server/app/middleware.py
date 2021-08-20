import jwt
from graphql import GraphQLError
from graphql_auth import mutations
from .schema import schema

def refreshTokenMiddleWare(get_response):

    def middleware(request):
        token = request.headers.get('Authorization')
        refreshToken = request.headers.get('X-Requested-With')
        response = get_response(request)
        if token :
            token = token.replace('JWT ', '')
            result = schema.execute(
                        '''
                        mutation VerifyToken($token: String!) {
                            verifyToken(token: $token) {
                                success
                            }
                        }
                        ''',
                        variables = {'token' : token},
                    )
            if result.data["verifyToken"]["success"] :
                print("token verified")
            else :
                print("token not verified")
                result = schema.execute(
                    '''
                    mutation RefreshToken($refreshToken: String!) {
                        refreshToken(refreshToken: $refreshToken) {
                            success
                            refreshToken
                            token
                        }
                    }
                    ''',
                    variables = {'refreshToken' : refreshToken},
                )
                if result.data['refreshToken']['success'] :
                    print("token refreshed")
                    response.set_cookie('token', result.data['refreshToken']['token'])
                    response.set_cookie('refreshToken', result.data['refreshToken']['refreshToken'])
                else :
                    print("token refresh fail")
        return response

    return middleware
