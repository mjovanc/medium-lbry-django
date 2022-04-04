from django import forms


LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('de', 'German'),
]

LICENSE_CHOICES = [
    ('public-domain', 'Public domain'),
]


class ImageForm(forms.Form):
    image = forms.ImageField()
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    language = forms.ChoiceField(widget=forms.Select, choices=LANGUAGE_CHOICES, initial='en')
    license = forms.ChoiceField(widget=forms.Select, choices=LICENSE_CHOICES, initial='public-domain')

    def clean(self):
        cleaned_data = super(ImageForm, self).clean()
        image = cleaned_data.get('image')
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        if not image and not title and not description:
            raise forms.ValidationError('You have to input something!')
