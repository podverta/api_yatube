from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404

class APIPost(viewsets.ViewSet):
    queryset = Post.objects.all()
    def list(self, request):
        serializer = PostSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def update(self, request, pk):
        item = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(item, data=request.data)
        if serializer.is_valid():
            if item.author == request.user:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partrial_update(self, request, pk):
        item = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            if item.author == request.user:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_400_BAD_REQUEST)

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

    def update(self, request, pk, post_id):
        comment = get_object_or_404(Comment, pk=pk, post_id=post_id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            if comment.author == request.user:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partrial_update(self, request, pk, post_id):
        comment = get_object_or_404(Comment, pk=pk, post_id=post_id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            if comment.author == request.user:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, post_id):
        comment = get_object_or_404(Comment, pk=pk, post_id=post_id)
        if comment.author == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)