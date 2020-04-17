from django import forms
from django.contrib.auth import (password_validation, )
from django.contrib.auth.forms import (AuthenticationForm, UsernameField,
    PasswordResetForm, SetPasswordForm)
from users.models import User

class FrontAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
        }))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
            }),
    )

    def clean(self):
        cd = super().clean()
        try:
            username = cd.get('username')
            user = User.objects.get(username = username)
            if user.profile.parent:
                self.add_error(None, forms.ValidationError(
                    """I minori non possono effettuare il login autonomamente!
                    Il loro account è gestito dai genitori.""",
                    code='minor_no_login',
                ))
        except:
            pass

class FrontPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254, label='Email di registrazione',
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
            })
    )

class FrontSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            }),
        strip=False, label='Nuova password',
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False, label='Ripeti la nuova password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
            }),
    )

class FrontPasswordChangeForm(FrontSetPasswordForm):
    old_password = forms.CharField(
        strip=False, label='Vecchia password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
            'autofocus': True, }),
    )
