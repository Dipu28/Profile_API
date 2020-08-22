from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated


from profile_api import serializers
from profile_api import models
from profile_api import permissions
# Create your views here.


# In APIView we add functions to a particular HTTP methods  to support your enpoints
class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]
        return Response({'message':'Hello','an_apiview':an_apiview})


    def post(self, request):
        """"Create a hello message with our name """
        serializer = self.serializer_class(data=request.data)

        # To validate the field
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object
           It will replace the whole object"""
        return Response({'method':'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object
           It will make changes only partially"""
        return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
        """It will delete"""
        return Response({'method':'DELETE'})



# In ViewSet you add functions that represent action that you will perform on a typical API
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet """
    serializer_class = serializers.HelloSerializer

    def list(self,list):
        """Return a hello message """
        a_view = [
            'Uses action (list, create, retrive, destroy, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        return Response({'message':'Hello','a_view':a_view})

    def create(self,request):
        """Create a new hello message """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST,
            )

    def retrive(self, request, pk=None):
        """Handle getting object by its ID """
        return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        """Handling updating an object"""
        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """ Handle removing an object"""
        return Response({'http_method':'DELETE'})


# Creating new model ViewSet:

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UdateOwmProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens. We have overide it to show in the API"""
    renderer_classes =api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handle creating , reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus,IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
