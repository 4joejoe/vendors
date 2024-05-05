from rest_framework.request import Request
from django.shortcuts import render
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PurchaseOrder, Vendor
from recipe.serializers import PurchaseOrderSerializer, VendorSerializer
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class VendorView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=VendorSerializer)
    def post(self, request: Request) -> Response:

        serialized_data = VendorSerializer(
            data=request.data, context={"request": request}
        )
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=201)
        return Response(serialized_data.errors, status=400)

    @swagger_auto_schema()
    def get(self, request, *args, **kwargs):
        print("-->KWARGS<--", kwargs)
        print("-->ARGS<--", args)
        if "vendor_id" in kwargs:
            return self.get_single_vendor(request, kwargs["vendor_id"])
        else:
            return self.get_all_vendors(request)

    def get_single_vendor(self, request, vendor_id):
        """Fetch and return a single vendor based on the vendor_id"""
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data, status=200)
        except Vendor.DoesNotExist:
            return Response("Vendor not found", status=404)

    def get_all_vendors(self, request):
        """Fetch and return all vendors paginated to 20 per request"""
        try:
            paginator = PageNumberPagination()
            paginator.page_size = 20
            vendors = Vendor.objects.all()
            result_page = paginator.paginate_queryset(vendors, request)
            serializer = VendorSerializer(result_page, many=True)
            return Response(serializer.data, status=200)

        except Vendor.DoesNotExist:
            return Response("Vendor not found", status=404)

    @swagger_auto_schema(request_body=VendorSerializer)
    def put(self, request, *args, **kwargs):
        if "vendor_id" in kwargs:
            try:
                vendor = Vendor.objects.get(id=kwargs["vendor_id"])
                serializer = VendorSerializer(vendor, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            except:
                return Response("Vendor not found", status=400)

        else:
            return Response("No vendor found", status=404)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "vendor_id",
                openapi.IN_PATH,
                description="ID of the Vendor",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        if "vendor_id" in kwargs:
            try:
                vendor = Vendor.objects.get(id=kwargs["vendor_id"])
                vendor.delete()
                return Response("Vendor deleted successfully", status=200)
            except Vendor.DoesNotExist:
                return Response("Vendor not found", status=404)
        else:
            return Response("No vendor id found", status=404)


class PurchaseOrderView(APIView):
    # permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=PurchaseOrderSerializer)
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Purchase order created", status=201)
        else:
            return Response(serializer.errors, status=400)

    def get(self, request, *args, **kwargs):
        if "po_id" in kwargs:
            print("Single PO")
            return self.get_single_purchase_order(po_id=kwargs["po_id"])
        elif "vendor_id" in kwargs:
            print("--> Vendor Specific <--")
            return self.get_all_purchase_order(vendor_id=kwargs["vendor_id"])
        else:
            print("--> All Vendor <--")
            return self.get_all_purchase_order()

            # return all purchase order

    def get_all_purchase_order(self, *args, **kwargs):
        """If vendor_id present in then return all purchase order by vendor id, if not then return all purchase orders"""

        if "vendor_id" in kwargs:
            print("--> Vendor <--")
            try:
                po = PurchaseOrder.objects.filter(vendor_reference=kwargs["vendor_id"])
            except:
                return Response("Vendor not found", status=404)
        else:
            print("All Vendor func")
            po = PurchaseOrder.objects.all()

        serializer = PurchaseOrderSerializer(po, many=True)

        # if serializer.is_valid():
        return Response(serializer.data, status=200)
        # else:
        #     return Response(serializer.errors, status=400)

    def get_single_purchase_order(self, *args, **kwargs):
        if "po_id" in kwargs:
            try:
                po = PurchaseOrder.objects.get(id=kwargs["po_id"])
                serializer = PurchaseOrderSerializer(po)
                return Response(serializer.data, status=200)
            except:
                return Response(serializer.errors, status=400)

        else:
            return Response("No purchase order id found")

    @swagger_auto_schema(request_body=PurchaseOrderSerializer)
    def put(self, request, *args, **kwargs):
        if "po_id" in kwargs:
            try:
                po = PurchaseOrder.objects.get(id=kwargs["po_id"])

                serializer = PurchaseOrderSerializer(po, data=request.data)
                if serializer.is_valid():
                    print("Serializer valid")
                    serializer.save()
                    return Response(serializer.data, status=200)
                else:
                    return Response(serializer.errors, status=400)
            except Exception as e:
                print("-> Exception", e)
                return Response("No PO found with given id")
        else:
            return Response("No po_id found in request")

    @swagger_auto_schema(
        # auto_schema=False,
        manual_parameters=[
            openapi.Parameter(
                "po_id",
                openapi.IN_PATH,
                description="ID of the purchase order",
                type=openapi.TYPE_INTEGER,
            )
        ],
    )
    def delete(self, request, *args, **kwargs):
        if "po_id" in kwargs:
            try:
                po = PurchaseOrder.objects.get(id=kwargs["po_id"])
                po.delete()
                return Response(f"{kwargs['po_id']} Successfully removed", status=203)
            except:
                return Response(f"No PO found with {kwargs['po_id']} id", status=404)
        else:
            return Response("Invalid request", status=400)


class PurchaseOrderAcknowledgement(APIView):

    def get(self, request, *args, **kwargs):
        if "po_id" in kwargs:
            try:
                po = PurchaseOrder.objects.get(id=kwargs["po_id"])
                serializer = PurchaseOrderSerializer(po, data=request.data)
                # current date time
                po.acknowledgement_date = timezone.now()
                po.save()
                return Response("PO Acknowledged", status=200)
            except:
                return Response("PO not found", status=404)
        else:
            return Response("No PO id found", status=404)


# Vendor Performance Endpoint (GET /api/vendors/{vendor_id}/performance):
# ● Retrieves the calculated performance metrics for a specific vendor.
# ● Should return data including on_time_delivery_rate, quality_rating_avg,
# average_response_time, and fulfillment_rate.


class VendorPerformance(APIView):
    def get(self, request, *args, **kwargs):
        if "vendor_id" in kwargs:
            try:
                vendor = Vendor.objects.get(id=kwargs["vendor_id"])
                serializer = VendorSerializer(vendor)
                return Response(serializer.data, status=200)
            except:
                return Response("Vendor not found", status=404)
        else:
            return Response("No Vendor id found", status=404)
