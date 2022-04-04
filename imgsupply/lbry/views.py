import requests

from django.views.generic import FormView, TemplateView
from django.core.files.storage import FileSystemStorage

from imgsupply.settings import BASE_DIR, MEDIA_URL
from lbry.forms import ImageForm


class ImageFormView(FormView):
    template_name = 'lbry/image_form.html'
    form_class = ImageForm
    success_url = '/'

    def form_valid(self, form):
        # store the uploaded file in media directory
        fs = FileSystemStorage()
        filename = fs.save(form.cleaned_data['image'].name, form.cleaned_data['image'])
        full_path_file = str(BASE_DIR) + MEDIA_URL + filename
        print(full_path_file)

        # do a POST request to LBRY API
        r = requests.post("http://localhost:5279", json={"method": "publish",
                                                         "params": {"name": "imgsupply-stream",
                                                                    "bid": "1.0",
                                                                    "file_path": full_path_file,
                                                                    "validate_file": False,
                                                                    "optimize_file": False,
                                                                    "tags": [],
                                                                    "languages": [],
                                                                    "locations": [],
                                                                    "channel_account_id": [],
                                                                    "funding_account_ids": [],
                                                                    "preview": False,
                                                                    "blocking": False}}).json()

        print(r['result']['outputs'][0]['claim_id'])
        return super().form_valid(form)


class ImageDetail(TemplateView):
    template_name = 'lbry/image_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = requests.post("http://localhost:5279", json={
            "method": "get",
            "params": {"uri": "lbry://imgsupply-stream#%s" % self.kwargs['lbry_id']}
        }).json()
        print(r['result'])
        context['img_path'] = MEDIA_URL + str(r['result']['metadata']['source']['name'])
        context['img_metadata'] = r['result']['metadata']
        return context
