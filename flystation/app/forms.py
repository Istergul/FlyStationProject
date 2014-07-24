from django import forms


css_attrs = {
    "latitude": {'class': 'form-control', 'placeholder': 'latitude'},
    "longitude": {'class': 'form-control', 'placeholder': 'longitude'}
}


class PointForm(forms.Form):
    latitude = forms.FloatField(
        min_value=-90.0,
        max_value=90.0,
        widget=forms.TextInput(attrs=css_attrs["latitude"])
    )
    longitude = forms.FloatField(
        min_value=-180.0,
        max_value=180.0,
        widget=forms.TextInput(attrs=css_attrs["longitude"])
    )