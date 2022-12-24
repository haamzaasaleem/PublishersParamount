from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from .plagCheck import *
from accounts.models import Author
from manuscripts.mail import *
from manuscripts.models import *
from accounts.models import *
from manuscripts.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
# from PIL import Image
# from core.settings import BASE_DIR
# from PyPDF2 import PdfFileMerger
# import convertapi
from accounts.serializers import *
from .utils import converting2Pdf
from journals import serialiazers
from .mail import *
from .tasks import *
import uuid


##Creating Manuscript
class ManuscriptViewSet(viewsets.ModelViewSet):
    queryset = Manuscript.objects.all()
    serializer_class = ManuscriptSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        user = request.user.id
        author = Author.objects.get(user_id=user)

        manuscript = Manuscript.objects.filter(author_id=author.id)
        serializer = ManuscriptSerializer(manuscript, many=True)
        return Response(serializer.data)

    def create(self, request):
        author = Author.objects.get(user_id=request.user.id)
        manuscript_data = {
            "journal": request.data['journal_id'],
            "title": request.data['title'],
            "abstract": request.data['abstract'],
            "keywords": request.data['keywords'],
            "article_type": request.data['article_type'],
            "manuscript_file": request.data['article_file'],
            "cover_file": request.data['cover_letter'],
            "abstract_file": request.data['abstract_file'],
            "figure_file": request.data['figure_file'],
            "author": author.id
        }

        serializer = ManuscriptSerializer(data=manuscript_data)

        if serializer.is_valid():

            serializer.save()
            # new_manuscript_email_task.apply_async([manuscript_data['title'], request.user.email])
            mergedFile = converting2Pdf(serializer.data)
            manuscript = Manuscript.objects.get(title=request.data['title'])
            # PdfMergerAndConverter.apply_async([serializer.data,manuscript.id])
            temp = mergedFile.split('/')

            str = '/'
            for i in range(temp.index('media'), len(temp)):
                str += temp[i]
                str += '/'
            manuscript.mergedPdf = str
            manuscript.save()
            coAuthor_data = {
                "name": request.data['coAuthor_name'],
                "email": request.data['coAuthor_email'],
                "manuscript": manuscript.id,
            }
            coAuthor_serializer = CoAuthorSerializer(data=coAuthor_data)
            if coAuthor_serializer.is_valid():
                coAuthor_serializer.save()

                new_manuscript_email(manuscript_data["title"], request.user.email)
                coAuthor_new_manuscript_email_task.apply_async([manuscript_data["title"], coAuthor_data['email']])
                return Response({
                    "msg": "Manuscript added",
                    "data": coAuthor_serializer.data | serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(coAuthor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        manuscript = Manuscript.objects.get(id=pk)
        data = request.data

        serializer = ManuscriptSerializer(manuscript, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Status Updated"}
            )


# Saving Manuscript by Author
class SaveManuscriptView(viewsets.ModelViewSet):
    queryset = Manuscript.objects.all()
    serializer_class = ManuscriptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, pk=None):
        manuscript_id = request.data['id']

        manuscript = Manuscript.objects.get(id=manuscript_id)
        manuscript.saved = True
        manuscript.save()
        author = Manuscript.objects.get(id=manuscript.author)
        user = User.objects.get(id=author.user)
        submitManuscriptMail(user.email)

        return Response(
            {'msg': 'uploaded'},
            status=status.HTTP_200_OK
        )


class AssignedManuscript2Reviewer(viewsets.ModelViewSet):
    queryset = ManuRev.objects.all()
    serializer_class = ManuRevSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user_id = request.user.id
        reviewer = Reviewer.objects.get(user=user_id)
        ManuRedIDs = ManuRev.objects.filter(reviewer=reviewer.id)
        manuRecSerialzier = ManuRevSerializer(ManuRedIDs, many=True)
        manuscripts = []
        for manu in ManuRedIDs:
            manuscripts.append(manu.manuscript)
            if manuscripts[-1].saved == False:
                manuscripts.pop()
            # manuscripts=Manuscript.objects.filter(id=ManuRedIDs)
        serializer = ManuscriptSerializer(manuscripts, many=True)
        # return Response(serializer.data)
        return Response(serializer.data)

    # Comment
    def partial_update(self, request, pk=None):
        reviewer = Reviewer.objects.get(user=request.user.id)
        manu = ManuRev.objects.get(manuscript=pk, reviewer=reviewer.id)

        if manu:
            manu.comment = request.data['comment']
            manu.recommendation = request.data['recommendation']
            manu.save()
            serializer = ManuRevSerializer(manu)
            return Response(
                {

                    "msg": "Updated Successfully"
                },
                status=status.HTTP_200_OK)
        return Response({
            "msg": "Error in Updating Comment"
        },
            status=status.HTTP_400_BAD_REQUEST
        )


class AssignedManuscript2Editor(viewsets.ModelViewSet):
    queryset = ManuEditor.objects.all()
    serializer_class = ManuEditorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user_id = request.user.id
        editor = Editor.objects.get(user=user_id)
        manuEditorID = ManuEditor.objects.filter(editor=editor.id)
        manuscripts = []
        for manu in manuEditorID:
            manuscripts.append(manu.manuscript)
            if manuscripts[-1].saved == False:
                manuscripts.pop()
            # manuscripts=Manuscript.objects.filter(id=ManuRedIDs)
        serializer = ManuscriptSerializer(manuscripts, many=True)
        # return Response(serializer.data)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def AssignManuscriptToEditor(request):
    serializer = ManuEditorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def savedManuscript(request, pk=None):
    manuscripts = Manuscript.objects.filter(journal=pk, saved=True)

    serializer = ManuscriptSerializer(manuscripts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def sendAssignedReviewers(request, pk=None):
    try:
        asignRev = ManuRev.objects.filter(manuscript=pk)
        serializer = ManuRevSerializer(asignRev, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def GiveReviewToAuthor(request, pk=None):
    manuscript = Manuscript.objects.get(id=pk)
    manuED = ManuEditor.objects.get(manuscript=manuscript.id)
    manuEditorSerializer = ManuEditorSerializer(manuED, data=request.data, partial=True)
    if manuEditorSerializer.is_valid():
        manuEditorSerializer.save()
        manuscriptSerializer = ManuscriptSerializer(manuscript, data=request.data, partial=True)
        if manuscriptSerializer.is_valid():
            manuscriptSerializer.save()

            # sendDecisionToAuthor(manuscript.)
            return Response(manuscriptSerializer.data, status=status.HTTP_201_CREATED)
        return Response(manuscriptSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(manuEditorSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def listApprovedArticles(request):
    try:
        manuscripts = Manuscript.objects.filter(status='approved')
        serializer = ManuscriptSerializer(manuscripts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'msg': "No Manuscript is Published Yet"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def listApprovedJournalArticles(request, pk):
    try:
        manuscripts = Manuscript.objects.filter(status='approved', journal=pk)

        serializer = ManuscriptSerializer(manuscripts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'msg': "No Manuscript is Published Yet"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def addReviewer(request):
    addReviewerMail(request.data['reviewerEmail'])
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def checkAssignedManuToEditor(request, pk):
    try:
        manuED = ManuEditor.objects.get(manuscript=pk)
        serializer = ManuEditorSerializer(manuED)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def plagCheckWebhook(request):
    print("webhook_hit", request.data)
    return Response(status=status.HTTP_200_OK)






@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def sendEmailforReviewerApproval(request):
    string = str(uuid.uuid4())

    url = f'http://localhost:3000/manuscriptApproval/{string}'
    rev = Reviewer.objects.get(id=request.data["reviewer"])
    user = User.objects.get(id=rev.user.id)
    data = {
        'string': string,
        'reviewer': request.data["reviewer"],
        'manuscript': request.data["manuscript"],
        'email': user.email
    }

    serializer = ReviewerEmailModelSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        revManuscriptApproval(url, user.email)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def assignOrRejectManuByReviewer(request):
    if request.data['status'] == False:
        try:
            string = ManuRevStringModel.objects.get(string=request.data['string'])
            if string:
                ManuRevStringModel.objects.get(string=request.data['string']).delete()
                return Response(status=status.HTTP_200_OK)
        except:
            return Response({'msg': "This link is expired"}, status=status.HTTP_200_OK)

    if request.data['status'] == True:
        try:
            string = ManuRevStringModel.objects.get(string=request.data['string'])
            if string:
                data = {
                    "reviewer": request.data['reviewer'],
                    "manuscript": request.data['manuscript']
                }

                serializer = ManuRevSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg': "Manuscript Accepted Please Login to view"}, status=status.HTTP_200_OK)

        except:
            return Response({'msg': "This link is expired"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def listManuscriptANY(request,pk):
    manuscript=Manuscript.objects.get(id=pk)
    serializer=ManuscriptSerializer(manuscript)
    return Response(serializer.data,status=status.HTTP_200_OK)