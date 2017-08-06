from django import forms


class AlertForm(forms.Form):
    address = forms.CharField(label='Event Address', max_length=200, widget=forms.Textarea)


class FollowUpForm(forms.Form):
    num_people = forms.IntegerField(label='Number People Detained', min_value=0)
    city = forms.CharField(label='City', max_length=200)
    target_name = forms.CharField(label='Person to Call for Release', max_length=200)
    target_phone_num = forms.CharField(label='Phone Number of Person to Call', max_length=20)
