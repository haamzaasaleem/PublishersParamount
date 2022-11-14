from rest_framework import permissions, viewsets
from accounts.models import Author
from manuscripts.models import Manuscript, Figure, ManuRev, ManuEditor
from accounts.models import *
from manuscripts.serializers import ManuscriptSerializer, FigureSerializer, ManuRevSerializer, ManuEditorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from core.settings import BASE_DIR
from PyPDF2 import PdfFileMerger
import convertapi


#
def converting2Pdf(manuscriptID):
    manuscript = Manuscript.objects.get(id=manuscriptID)

    # converting Manuscript to pdf
    inputPath = f'{BASE_DIR}/media/{manuscript.manuscript_file}'
    fileList = [f'{BASE_DIR}/media/mergedPdfs/{manuscript.manuscript_file}']
    result = convertapi.convert('pdf', {'File': f'{inputPath}'})
    result.file.save(f'{fileList[0]}')

    allfiles = Figure.objects.filter(manuscript=manuscriptID)
    fileList = []
    for file in range(len(allfiles)):
        img = Image.open(rf'{BASE_DIR}/media/{file.file}')
        filename = file.split('/')
        temp = img.convert('RGB')
        temp.save(rf'{BASE_DIR}/media/convertedpdfs/{manuscriptID}-{filename[-1]}.pdf')
        fileList.append(temp)

    merger = PdfFileMerger()
    for pdf_file in fileList:
        merger.append(pdf_file)

    merger.write()


class ManuscriptViewSet(viewsets.ModelViewSet):
    # import pdb; pdb.set_trace()
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

        author = Author.objects.get(user_id=request.data['author'])

        request.data['author'] = author.id

        serializer = ManuscriptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            manuscript = Manuscript.objects.get(title=request.data['title'])

            for figure in range(len(request.data['figure_files'])):
                file = {
                    'file': figure,
                    'manuscript': manuscript.id
                }

                figure = FigureSerializer(data=file)
                if figure.is_valid():
                    figure.save()
                else:
                    return Response(figure.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
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


class SaveManuscriptView(viewsets.ModelViewSet):
    queryset = Manuscript.objects.all()
    serializer_class = ManuscriptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, pk=None):
        manuscript_id = request.data['id']

        manuscript = Manuscript.objects.get(id=manuscript_id)
        manuscript.saved = True
        manuscript.save()
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
        manuRecSerialzier = ManuRevSerializer(ManuRedIDs)
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
            manu.save()
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

    # def

