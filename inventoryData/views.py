from inventoryData.models import Boxes
from authe.models import User
from inventoryData.serializer import BoxSerializer, UserBoxSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from inventoryData.permissions import IsStaffPermission
from datetime import datetime

# Create your views here.


# adding a box
class AddBoxApi(APIView):

    permission_classes = [IsAuthenticated, IsStaffPermission]

    def post(self, request):
        data = request.data
        data['created_by'] = request.user
        serializer = BoxSerializer(data=data)
        if serializer.is_valid():
            box = serializer.save(created_by=request.user)
            return Response({"msg" : "Added box successfully!", "data":BoxSerializer(box).data}, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors, "data":None}, status=status.HTTP_400_BAD_REQUEST)

# updating a box
class UpdateBoxApi(APIView):

    permission_classes = [IsStaffPermission]

    def patch(self, request):
        try:
            box = Boxes.objects.get(pk=request.data.get('box_id'))
        except Boxes.DoesNotExist:
            return Response({"error": "Box not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if ('created_by' in data) or ('created_at' in data):
            return Response({"msg":"You can't update created_at and created_by", "data" : None}, status=status.HTTP_400_BAD_REQUEST)

        data['updated_on'] = datetime.now()
        del data['box_id']

        serializer = BoxSerializer(box, data=data, partial=True)
        if serializer.is_valid():
            box = serializer.save()
            return Response({"msg":"box data updated successfully!", "data":BoxSerializer(box).data}, status=status.HTTP_200_OK)
        return Response({"msg" : serializer.errors, "data": None}, status=status.HTTP_400_BAD_REQUEST)

# Deleting a box
class DeleteBoxApi(APIView):

    def delete(self, request):
        try:
            box = Boxes.objects.get(pk=request.data.get('box_id'))
            print(box,"----------")
        except Boxes.DoesNotExist:
            return Response({"msg": "Box not found.", "data":None}, status=status.HTTP_404_NOT_FOUND)
        
        if box.created_by != request.user:
            return Response({"msg": "You are not authorized to delete this box.", "data":None}, status=status.HTTP_403_FORBIDDEN)
        
        box.delete()
        return Response({"msg":"Box deleted successfully!", "data":None}, status=status.HTTP_204_NO_CONTENT)

# List all boxes
class ListAllBoxesApi(APIView):

    def get(self, request):
        length_more_than = request.query_params.get('length_more_than')
        length_less_than = request.query_params.get('length_less_than')
        width_more_than = request.query_params.get('width_more_than')
        width_less_than = request.query_params.get('width_less_than')
        height_more_than = request.query_params.get('height_more_than')
        height_less_than = request.query_params.get('height_less_than')
        area_more_than = request.query_params.get('area_more_than')
        area_less_than = request.query_params.get('area_less_than')
        volume_more_than = request.query_params.get('volume_more_than')
        volume_less_than = request.query_params.get('volume_less_than')
        created_by_username = request.query_params.get('created_by')
        created_before = request.query_params.get('created_before')
        created_after = request.query_params.get('created_after')

        boxes = Boxes.objects.all()

        if length_more_than:
            boxes = boxes.filter(length__gt=length_more_than)
        if length_less_than:
            boxes = boxes.filter(length__lt=length_less_than)
        if width_more_than:
            boxes = boxes.filter(width__gt=width_more_than)
        if width_less_than:
            boxes = boxes.filter(width__lt=width_less_than)
        if height_more_than:
            boxes = boxes.filter(height__gt=height_more_than)
        if height_less_than:
            boxes = boxes.filter(height__lt=height_less_than)
        if area_more_than:
            boxes = boxes.filter(area__gt=area_more_than)
        if area_less_than:
            boxes = boxes.filter(area__lt=area_less_than)
        if volume_more_than:
            boxes = boxes.filter(volume__gt=volume_more_than)
        if volume_less_than:
            boxes = boxes.filter(volume__lt=volume_less_than)
        if created_by_username:
            print(created_by_username)
            try:
                user = User.objects.get(username=created_by_username)
            except:
                return Response({"msg":"No Staff member exists with this username!", "data":None}, status=status.HTTP_404_NOT_FOUND)
            boxes = boxes.filter(created_by=user)
        if created_before:
            created_before_date = datetime.strptime(created_before, "%Y-%m-%d")
            boxes = boxes.filter(created_at__lt=created_before_date)
        if created_after:
            created_after_date = datetime.strptime(created_after, "%Y-%m-%d")
            boxes = boxes.filter(created_at__gt=created_after_date)

        is_staff = request.user.is_staff
        serializer = ""
        if is_staff:
            serializer = BoxSerializer(boxes, many=True)
        else:
            serializer = UserBoxSerializer(boxes, many=True)

        return Response({"msg":"data found!", "data":serializer.data}, status=status.HTTP_200_OK)

# list my boxes 
class ListMyBoxesApi(APIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]

    def get(self, request):
        length_more_than = request.query_params.get('length_more_than')
        length_less_than = request.query_params.get('length_less_than')
        width_more_than = request.query_params.get('width_more_than')
        width_less_than = request.query_params.get('width_less_than')
        height_more_than = request.query_params.get('height_more_than')
        height_less_than = request.query_params.get('height_less_than')
        area_more_than = request.query_params.get('area_more_than')
        area_less_than = request.query_params.get('area_less_than')
        volume_more_than = request.query_params.get('volume_more_than')
        volume_less_than = request.query_params.get('volume_less_than')

        boxes = Boxes.objects.filter(created_by=request.user)

        if length_more_than:
            boxes = boxes.filter(length__gt=length_more_than)
        if length_less_than:
            boxes = boxes.filter(length__lt=length_less_than)
        if width_more_than:
            boxes = boxes.filter(width__gt=width_more_than)
        if width_less_than:
            boxes = boxes.filter(width__lt=width_less_than)
        if height_more_than:
            boxes = boxes.filter(height__gt=height_more_than)
        if height_less_than:
            boxes = boxes.filter(height__lt=height_less_than)
        if area_more_than:
            boxes = boxes.filter(area__gt=area_more_than)
        if area_less_than:
            boxes = boxes.filter(area__lt=area_less_than)
        if volume_more_than:
            boxes = boxes.filter(volume__gt=volume_more_than)
        if volume_less_than:
            boxes = boxes.filter(volume__lt=volume_less_than)

        serializer = BoxSerializer(boxes, many=True)
        return Response({"msg":"data found!", "data":serializer.data}, status=status.HTTP_200_OK)
