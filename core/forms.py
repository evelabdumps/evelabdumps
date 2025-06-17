from django import forms
from .models import EveLabFile, NetworkIssue, ConsultancyRequest, LabImage


MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20MB



class LabImageForm(forms.ModelForm):
    class Meta:
        model = LabImage
        fields = ['category', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})

class EveLabFileForm(forms.ModelForm):
    class Meta:
        model = EveLabFile
        fields = ['file']

class EveLabFileForm(forms.ModelForm):
    class Meta:
        model = EveLabFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class NetworkIssueForm(forms.ModelForm):
    class Meta:
        model = NetworkIssue
        fields = ['title', 'description', 'lab_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Issue Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your issue'}),
            'lab_file': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NetworkIssueForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['lab_file'].queryset = user.labs.all()

class ConsultancyRequestForm(forms.ModelForm):
    class Meta:
        model = ConsultancyRequest
        fields = ['topic', 'description']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Consultancy Topic'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your requirements'}),
        }