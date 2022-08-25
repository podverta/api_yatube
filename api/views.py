from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class APIPost(viewsets.ViewSet):
    queryset = Post.objects.all()
    def list(self, request):
        serializer = PostSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)