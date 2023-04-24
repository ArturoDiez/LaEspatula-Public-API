from django import forms


# aria-label: ayuda a saber que es, pero no aparece en la web


class jugadorTFTForm(forms.Form):
    cuenta = forms.CharField(max_length=100,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario',
                                        'aria-label': 'jugadorTFT', 'aria-describedby': 'add-btn'}))
