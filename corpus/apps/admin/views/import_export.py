from django.views.generic import TemplateView, View
from django.conf import Settings
from django.http import JsonResponse, FileResponse
from ..forms import ImportForm, ExportForm
from ..helpers import handle_phrase_import, handle_phrase_export

class ImportExportAdminView(TemplateView):
    template_name='admin/import_export.html'


class ImportAPIView(View):
    form_class= ImportForm
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)

    def form_valid(self, form):
        source_language = form.cleaned_data.get('source_language')
        target_language = form.cleaned_data.get('target_language')
        uploaded_file = form.cleaned_data.get('file')
        try:
           self.handle_import(source_language, target_language, uploaded_file)
        except Exception as e:
            print(e)
            return JsonResponse({'error':'Import failed'}, status=400)


        return JsonResponse({'success': 'File uploaded'})

    def handle_import(self, source_language, target_language, uploaded_file):
        handle_phrase_import(source_language, target_language,uploaded_file)       

        
class ExportAPIView(View):
    def post(self, request):
        form = ExportForm(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        source_language = form.cleaned_data.get('source_language')
        target_language = form.cleaned_data.get('target_language')
        export_as = form.cleaned_data.get('export_as')

        #try:
        file_path = self.handle_export(source_language, target_language, export_as)
        #except Exception as e:
        #    print(e)
        #    return JsonResponse({'error':'Export failed'}, status=400)
        
        return FileResponse(open(file_path, 'rb'), charset='utf-8')
    
    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)
    
    def handle_export(self, source_language, target_language, export_as):
        return handle_phrase_export(source_language, target_language, export_as)