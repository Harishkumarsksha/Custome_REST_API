from django import forms

from API_App.models import EmployeeData


class EmployeeForm(forms.ModelForm):
    # perfomer the form validation in the forms
    def clean_esal(self):

        inputsal = self.cleaned_data['esal']
        if int(inputsal) < 5000:
            raise forms.ValidationError(
                'The minimum Salary should be greater than 5000')
        return inputsal

    class Meta:

        model = EmployeeData

        fields = '__all__'
