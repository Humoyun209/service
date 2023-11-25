from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from api.serializers import (
    AdWithRequestSerializer,
    AdvertisementForManageSerializer,
    AdvertisementSerializer,
    RequestCreateSerializer,
)
from api.models import Advertisement, Request
from api.serializers import UserSerializer


class AdvertisementCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        author_id = request.user.id
        serializer = AdvertisementForManageSerializer(
            data=request.data, context={"request": request, "author_id": author_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": "serializer.data"})


class AdvertisementUpdateDesroyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, advertisement_id):
        advertisement = get_object_or_404(Advertisement, id=advertisement_id)
        if request.user == advertisement.author:
            serializer = AdvertisementForManageSerializer(
                data=request.data, instance=advertisement, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"Error": "Forbidden"}, status=403)

    def delete(self, request, advertisement_id):
        advertisement = get_object_or_404(Advertisement, id=advertisement_id)
        if request.user == advertisement.author:
            advertisement.delete()
            return Response({"Success": "ok"}, status=200)
        else:
            return Response({"Error": "Forbidden"}, status=403)


class AdvertisementView(RetrieveAPIView):
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Advertisement.objects.filter(author=user)
        return queryset


class AdvertisementsApiView(APIView):
    def get(self, request, category=None):
        advertisements = Advertisement.objects.all()
        if category is None:
            serializer = AdvertisementSerializer(advertisements, many=True)
        else:
            advertisements = advertisements.filter(category__slug=category)
            serializer = AdvertisementSerializer(advertisements, many=True)
        return Response({"advertisements": serializer.data})


class AddRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, advertisement_id):
        advertisement = get_object_or_404(Advertisement, id=advertisement_id)
        data = request.data
        data['advertisement'] = advertisement.id
        if advertisement.author != request.user:
            serializer = RequestCreateSerializer(
                data=data,
                context={
                    "request": request,
                    "advertisement": advertisement,
                    "user": request.user,
                },
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Success": "ok"}, status=200)
        else:
            return Response({"Error": "You don't do it"}, status=404)


class RequestListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, advertisement_id=None):
        advertisements = Advertisement.objects.filter(author=request.user)
        if advertisement_id is None:
            serializer = AdWithRequestSerializer(advertisements, many=True)
            return Response(serializer.data)
        else:
            advertisement = get_object_or_404(Advertisement, id=advertisement_id)
            if advertisement.author == request.user:
                
                serializer = AdWithRequestSerializer(
                    instance=advertisement
                )
                return Response(serializer.data)
            else:
                return Response({"error": 'Forbidden'}, status=403)


class ConfirmRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        request_ = get_object_or_404(Request, id=request_id)
        if request_.advertisement.author == request.user and request.user != request_.user:
            request_.is_pleasant = True
            request_.save()
            return Response({"Success": "ok"})
        else:
            return Response({"Error": "Forbidden"}, status=403)


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
