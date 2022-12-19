from PIL import Image
from core.settings import BASE_DIR
from PyPDF2 import PdfFileMerger
import convertapi

convertapi.api_secret='aeaNORkfmTYYvVGD'

def converting2Pdf(data):
    import pdb;
    pdb.set_trace()
    manuscript = data['manuscript_file']
    cover_file = data['cover_file']
    abstract_file = data['abstract_file']
    figure_file = data['figure_file']

    # converting Manuscript to pdf
    inputPath = f'{BASE_DIR}{manuscript}'
    temp = manuscript.split('/')
    temp=temp[4].split('.')
    manuscript_path = f'{BASE_DIR}/media/mergedPdfs/{temp[0]}.pdf'
    fileList = [manuscript_path]
    result = convertapi.convert('pdf', {'File': f'{inputPath}'})
    result.file.save(f'{fileList[0]}')

    if abstract_file is not None:
        temp = abstract_file.split('/')
        temp = temp[4].split('.')
        abstract_path = f'{BASE_DIR}/media/mergedPdfs/{temp[0]}.pdf'
        fileList.append(abstract_path)
        inputPath = f'{BASE_DIR}{abstract_file}'
        result = convertapi.convert('pdf', {'File': f'{inputPath}'})
        result.file.save(f'{fileList[1]}')

    if cover_file is not None:
        temp = cover_file.split('/')
        temp = temp[4].split('.')
        cover_path = f'{BASE_DIR}/media/mergedPdfs/{temp[0]}.pdf'
        fileList.append(cover_path)
        inputPath = f'{BASE_DIR}{cover_file}'
        result = convertapi.convert('pdf', {'File': f'{inputPath}'})
        result.file.save(f'{fileList[2]}')

    if figure_file is not None:


        temp = figure_file.split('/')
        temp = temp[4].split('.')
        figure_path = f'{BASE_DIR}/media/mergedPdfs/{temp[0]}.pdf'
        img = Image.open(rf'{BASE_DIR}{figure_file}')

        temp = img.convert('RGB')
        temp.save(f'{figure_path}')
        fileList.append(figure_path)

    merger = PdfFileMerger()
    for pdf_file in fileList:
        merger.append(pdf_file)
    temp = manuscript.split('/')
    temp = temp[4].split('.')
    mergedPdfPath = f'{BASE_DIR}/media/mergedPDfs/{temp[0]}.pdf'
    merger.write(mergedPdfPath)
    merger.close()
    return mergedPdfPath
