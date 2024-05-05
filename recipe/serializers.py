from rest_framework.serializers import ModelSerializer

from recipe.models import Vendor, PurchaseOrder


class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        # fields = "__all__"
        fields = ["contact_details", "name", "address"]

    def create(self, validated_data):
        # user = validated_data.pop("user")
        user = self.context["request"].user
        vendor = Vendor.objects.create(user=user, **validated_data)
        return vendor


class PurchaseOrderSerializer(ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = "__all__"
