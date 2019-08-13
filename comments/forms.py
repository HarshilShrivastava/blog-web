from django import forms


class Commentform(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    content_id = forms.IntegerField(widget=forms.HiddenInput)
    # parent_id = forms.IntegerField(widget=forms.HiddenInput, required   =False)
    content = forms.CharField(widget=forms.Textarea)
