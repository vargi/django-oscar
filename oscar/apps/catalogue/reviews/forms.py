from django import forms
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

Vote = get_model('reviews', 'vote')
ProductReview = get_model('reviews', 'productreview')


class ProductReviewForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), required=True)
    email = forms.EmailField(label=_('Email'), required=True)

    def __init__(self, product, user=None, *args, **kwargs):
        super(ProductReviewForm, self).__init__(*args, **kwargs)
        self.instance.product = product
        if user and user.is_authenticated():
            self.instance.user = user
            del self.fields['name']
            del self.fields['email']

    class Meta:
        model = ProductReview
        fields = ('title', 'score', 'body', 'name', 'email')


class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = ('delta',)

    def __init__(self, review, user, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.instance.review = review
        self.instance.user = user

    @property
    def is_up_vote(self):
        return self.cleaned_data['delta'] == Vote.UP

    @property
    def is_down_vote(self):
        return self.cleaned_data['delta'] == Vote.DOWN
