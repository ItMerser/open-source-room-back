from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from api.permissions import (
    IsRecipient,
    IsNotRecipient,
    SenderIsProjectOwner,
    IsNotTeamMember,
    RecipientIsProjectOwner,
)
from core.models.choices import OfferType
from api.mixins import OfferMixin


class OfferAddingToTeamApiView(OfferMixin, APIView):
    permission_classes = [IsAuthenticated, IsNotRecipient, SenderIsProjectOwner]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        created_offer = self.create_offer(request=request, offer_type=OfferType.ADD_TO_TEAM)
        return Response(status=HTTP_201_CREATED, data=created_offer)


class OfferJoiningToTeamApiView(OfferMixin, APIView):
    permission_classes = [IsAuthenticated, IsNotRecipient, RecipientIsProjectOwner, IsNotTeamMember]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        created_offer = self.create_offer(request=request, offer_type=OfferType.JOIN_TO_TEAM)
        return Response(status=HTTP_201_CREATED, data=created_offer)


class OfferGivingOwnershipApiView(OfferMixin, APIView):
    permission_classes = [IsAuthenticated, IsNotRecipient, SenderIsProjectOwner]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        created_offer = self.create_offer(request=request, offer_type=OfferType.GIVE_OWNERSHIP)
        return Response(status=HTTP_201_CREATED, data=created_offer)


class OfferGettingOwnershipApiView(OfferMixin, APIView):
    permission_classes = [IsAuthenticated, IsNotRecipient, RecipientIsProjectOwner]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        created_offer = self.create_offer(request=request, offer_type=OfferType.GET_OWNERSHIP)
        return Response(status=HTTP_201_CREATED, data=created_offer)


class OfferResponseApiView(OfferMixin, APIView):
    permission_classes = [IsAuthenticated, IsRecipient]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, offer_id: int):
        self.response_to_offer(request=request, offer_id=offer_id)
        return Response(status=HTTP_200_OK)
