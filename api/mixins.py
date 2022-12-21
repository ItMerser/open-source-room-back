from api.serializers.offer import OfferCreationSerializer
from api.validators import validate_offer_creation_data, validate_offer_response_data
from core.models import Specialist, Project, Offer
from core.models.choices import OfferType


class OfferMixin:
    def create_offer(self, request, offer_type: str) -> dict:
        validate_offer_creation_data(data=request.data)
        self.check_object_permissions(request=request, obj=request.user)
        recipient = Specialist.objects.get(pk=request.data['recipient_id'])
        project = Project.objects.get(pk=request.data['project_id'])
        offer, _ = Offer.objects.get_or_create(
            sender=request.user,
            recipient=recipient,
            project=project,
            type=offer_type,
        )
        return OfferCreationSerializer(offer).data

    def response_to_offer(self, request, offer_id: int):
        validate_offer_response_data(data=request.data)
        self.check_object_permissions(request=request, obj=request.user)
        response = request.data['response']

        successful_response_actions = {
            OfferType.ADD_TO_TEAM: self._add_to_team,
            OfferType.JOIN_TO_TEAM: self._join_to_team,
            OfferType.GIVE_OWNERSHIP: self._give_ownership,
            OfferType.GET_OWNERSHIP: self._get_ownership,
        }

        if response is False:
            Offer.objects.filter(pk=offer_id).update(response=response)
        else:
            offer = Offer.objects.get(pk=offer_id)
            action = successful_response_actions[offer.type]
            action(offer=offer)

    def _add_to_team(self, offer: Offer):
        offer.recipient.current_project = offer.project
        offer.recipient.save()
        offer.recipient.projects.add(offer.project)
        offer.project.team.add(offer.recipient)

    def _join_to_team(self, offer: Offer):
        offer.sender.current_project = offer.project
        offer.sender.save()
        offer.sender.projects.add(offer.project)
        offer.project.team.add(offer.sender)

    def _give_ownership(self, offer: Offer):
        offer.sender.self_projects.remove(offer.project)
        offer.recipient.self_projects.add(offer.project)

    def _get_ownership(self, offer: Offer):
        offer.sender.self_projects.add(offer.project)
        offer.recipient.self_projects.remove(offer.project)
