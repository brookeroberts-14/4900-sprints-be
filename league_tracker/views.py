from rest_framework import status, generics
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view(['GET', 'POST'])
def league_list(request):
    #Retrieve or update the league list.
    if request.method == 'GET':
        leagues = League.objects.all()
        serializer = LeagueSerializer(leagues, context={'request': request}, many=True)
        return Response({'data': serializer.data})
    elif request.method == 'POST':
        serializer = LeagueSerializer(data=request.data)
        if serializer.is_valid():
            #had to change this save function to set the owner because I was getting another 500 error bc owner wasn't
            #set
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def decks(request):
    if request.method == 'GET':
        decks = Deck.objects.select_related('league_player').all()
        serializer = DeckSerializer(decks, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = DeckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def formats(request):
    # Retrieve or Update Formats
    if request.method == 'GET':
        formats = Format.objects.all()
        serializer = FormatSerializer(formats, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = FormatSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def league_players(request):
    if request.method == 'GET':
        league_players = League_Player.objects.all()
        serializer = LeaguePlayerSerializer(league_players, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        league_id = request.data.get('league')
        player_input = request.data.get('player')

        try:
            if player_input and not str(player_input).isdigit():
                target_user = User.objects.get(username=player_input)
            else:
                target_user = request.user

            obj, created = League_Player.objects.get_or_create(
                league_id=league_id,
                player=target_user
            )

            serializer = LeaguePlayerSerializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"detail": f"User '{player_input}' not found."}, status=404)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

@api_view(['GET', 'POST'])
def matches(request):
    if request.method == 'GET':
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def match_player_details(request):
    if request.method == 'GET':
        match = Match_Player_Detail.objects.all()
        serializer = MatchPlayerDetailSerializer(match, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = MatchPlayerDetailSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def match_rounds(request):
    if request.method == 'GET':
        match_rounds = Match_Round.objects.all()
        serializer = MatchRoundSerializer(match_rounds, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = MatchRoundSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def match_round_players(request):
    if request.method == 'GET':
        match_round_players = Match_Round_Player.objects.all()
        serializer = MatchRoundPlayerSerializer(match_round_players, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = MatchRoundPlayerSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def getLeague(request, pk):
    #Retrieve, update or delete a league instance.
    try:
        league = League.objects.get(pk=pk)
    except League.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LeagueSerializer(league,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LeagueSerializer(league, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        league.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def getDeck(request, pk):
    #Retrieve, update, or delete a deck instance
    try:
        deck = Deck.objects.get(pk=pk)
    except Deck.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DeckSerializer(deck, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DeckSerializer(deck, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        deck.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def getFormat(request, pk):
    # Retrieve, update, or delete a format instance
    try:
        format = Format.objects.get(pk=pk)
    except Format.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FormatSerializer(format, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FormatSerializer(format, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        format.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def getLeaguePlayer(request, pk):
    try:
        league_players = League_Player.objects.get(pk=pk)
    except League_Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LeaguePlayerSerializer(league_players, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LeaguePlayerSerializer(league_players, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        league_players.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def getMatches(request, pk):
    try:
        matches = Match.objects.get(pk=pk)
    except Match.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MatchSerializer(matches, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MatchSerializer(matches, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        matches.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def getMatchPlayerDetail(request, pk):
    try:
        match_player_details = Match_Player_Detail.objects.get(pk=pk)
    except Match_Player_Detail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MatchPlayerDetailSerializer(match_player_details, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MatchPlayerDetailSerializer(match_player_details, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        match_player_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def getMatchRoundDetail(request, pk):
    try:
        match_rounds = Match_Round.objects.get(pk=pk)
    except Match_Round.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MatchRoundSerializer(match_rounds, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MatchRoundSerializer(match_rounds, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        match_rounds.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def getMatchRoundPlayerDetail(request, pk):
    try:
        match_round_players = Match_Round_Player.objects.get(pk=pk)
    except Match_Round_Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MatchRoundPlayerSerializer(match_round_players, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MatchRoundPlayerSerializer(match_round_players, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        match_round_players.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterView(generics.CreateAPIView):
    #Register a new user - requester need not be authorized
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer