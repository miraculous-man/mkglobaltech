from django.test import TestCase

# Create your tests here.
date_of_birth = self.cleaned_data.get('date_of_birth'),
LG_origin = self.cleaned_data.get('LG_origin'),
state_origin = self.cleaned_data.get('state_origin'),
parent_name = self.cleaned_data.get('parent_namet'),
parent_adress = self.cleaned_data.get('parent_adress'),
Parent_number = self.cleaned_data.get('Parent_number'),
Emergency_contact = self.cleaned_data.get('Emergency_contact'),
relationship = self.cleaned_data.get('relationship'),
emergency_address = self.cleaned_data.get('emergency_address'),
emergency_number = self.cleaned_data.get('emergency_number'),
file = self.cleaned_data.get('file'),
student_certificate_waec_image = self.cleaned_data.get(
    'student_certificate_waec_image '),
student_certificate_jamb_image = self.cleaned_data.get(
    'student_certificate_jamb_image'),
student_certificate_other_image = self.cleaned_data.get(
    'student_certificate_other_imag')



 picture = forms.ImageField(label= "image:")
    news_feed = forms.CharField(   max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Image Title:",)
    event_feed = forms.CharField(max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="image Title2:",)
    contact_us = forms.CharField(   max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Description:")