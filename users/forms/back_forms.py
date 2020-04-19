from django import forms

from django.forms import ModelForm
from users.models import Profile

class ChangeMemberChildForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('sector', 'parent', 'is_trusted',
            'avatar',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality',
            'fiscal_code',
            'course', 'course_alt', 'course_membership',
            'sign_up', 'privacy', 'med_cert',
            'membership', 'mc_expiry', 'mc_state', 'total_amount', 'settled'
            )

class ChangeMember0Form(ModelForm):

    class Meta:
        model = Profile
        fields = ('sector', 'is_trusted',
            'avatar', 'yes_spam',
            )

class ChangeMember1Form(ModelForm):

    class Meta:
        model = Profile
        fields = ('sector', 'is_trusted',
            'avatar', 'yes_spam', 'bio',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality',
            'fiscal_code',
            'address', 'phone', 'email_2',
            'course', 'course_alt', 'course_membership',
            'sign_up', 'privacy', 'med_cert',
            'membership', 'mc_expiry', 'mc_state', 'total_amount', 'settled'
            )

class ChangeMember2Form(ModelForm):

    class Meta:
        model = Profile
        fields = ('sector', 'is_trusted',
            'avatar', 'yes_spam', 'bio',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality',
            'fiscal_code',
            'address', 'phone', 'email_2',
            'no_course_membership',
            'sign_up', 'privacy', 'med_cert',
            'membership', 'mc_expiry', 'mc_state', 'total_amount', 'settled'
            )

class ChangeMember3Form(ModelForm):

    class Meta:
        model = Profile
        fields = ('sector', 'is_trusted',
            'avatar', 'yes_spam', 'bio',
            'fiscal_code',
            'address', 'phone', 'email_2'
            )
