from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializer import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer


class MovieListView(APIView):
    #Input of films list
    def get(self, request): #for GET request
        movies = Movie.objects.filter(draft=False) # shows all films which are not in draft
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """All film"""
    def get(self, request, pk): #for GET request
        movies = Movie.objects.get(id=pk, draft=False) # shows all films which are not in draft
        serializer = MovieDetailSerializer(movies)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    '''Adding reviews to film or cartoon'''
    def post(self, request):
        print(request)
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            res = {
                'error': False,
                'message': "Create successuly"
            }
            status = 201
            review.save()

        else:
            res = {
                'error': True,
                'message': review.errors,
            }
            status = 400
        return Response(res, status=status)


class AddStarRatingView(APIView):
    '''adding rating to film'''
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=self.get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
