from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
  routes=[
    'GET /api',
    'GET /api/rooms',
    'GET /api/room/:id',
    
  ]
  # rest automatically serializes the lists gives, you don't need to pass safe=False method here like in JsonResponse
  return Response(routes)

@api_view(['GET'])
def getRooms(request):
  rooms = Room.objects.all()
  serializer = RoomSerializer(rooms,many=True)
  #this alone passes the objects and not the list. So, using serializers.py, we serialize every object into the json format
  return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,pk):
  room = Room.objects.get(id=pk)
  serializer = RoomSerializer(room,many=False)
  return Response(serializer.data)