from rest_framework import viewsets, status, filters, generics, mixins
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Follow, Group
from .serializers import  (
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupSerializer
)
from django.shortcuts import get_object_or_404

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        item = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        item = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(item, data=request.data)
        if serializer.is_valid():
            # if item.author == request.user:
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        item = get_object_or_404(Post, pk=pk)
        if item.author == request.user:
            serializer = PostSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


    def destroy(self, request, pk):
        item = get_object_or_404(Post, pk=pk)
        if item.author == request.user:
           item.delete()
           return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

class APIComment(viewsets.ViewSet):

    def list(self, request, post_id):
        queryset = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk, post_id):
        comment = get_object_or_404(Comment, pk=pk, post_id=post_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, post_id, pk):
        comment = get_object_or_404(Comment, pk=pk,)
        if comment.author == request.user:
            serializer = CommentSerializer(comment, data=request.data,
                                           )
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


    def partial_update(self, request, post_id, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author == request.user:
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


    def destroy(self, request, pk, post_id):
        comment = get_object_or_404(Comment, pk=pk, post_id=post_id)
        if comment.author == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

class APIFollow(viewsets.ModelViewSet):

        queryset = Follow.objects.all()
        serializer_class = FollowSerializer
        filter_backends = [filters.SearchFilter]
        search_fields = ['user__username', ]

        def list(self, request, *args, **kwargs):
            queryset = Follow.objects.filter(following__username=request.user)
            serializer_class = FollowSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)


        def create(self, request):
            serializer_class = FollowSerializer(data=request.data)
            if request.user.is_authenticated == True:
                if serializer_class.is_valid():
                    serializer_class.save(user=request.user)
                    return Response(serializer_class.data,
                                    status=status.HTTP_201_CREATED)
                return Response(serializer_class.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)


class APIGroup(generics.ListCreateAPIView):
        queryset = Group.objects.all()
        serializer_class = GroupSerializer
        filter_backends = [filters.SearchFilter]
        search_fields = ['title',]