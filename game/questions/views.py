import math
import random

from django.views import generic

from countries.models import Country
from questions.forms import QuestionForm, PreviousForm
from questions.models import Account, Question


LEVEL_CHOICES = {
    1: [150],  # Europe
    2: [150, 19],  # +Americas
    3: [150, 19, 142],  # + Asia
    4: [150, 19, 142, 2],  # + Africa
    5: [150, 19, 142, 2, 9],  # + Oceania
}

NEW_REGIONS = {
    2: 'America',
    3: 'Asia',
    4: 'Africa',
    5: 'Oceania',
}

def level_for_count(question_count):
    """
    Returns a level for a given number of correct questions
    """
    return int(math.log(questions_count + 1))


class LevelMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                request.account = request.user.account
            except Account.DoesNotExist:
                request.account = Account.objects.create(user=request.user)
            num = request.questions.filter(country=models.Q('answer')).count()
            level = level_for_count(num)
            if not request.account.level == level:
                request.account.level = level
                request.account.save()
        else:
            if not 'questions' in request.session:
                request.session['questions'] = []
            request.account = AnonymousAccount(level=request.session['level'])



class QuestionView(generic.FormView):
    form_class = QuestionForm
    template_name = 'questions/question.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            level = request.user.twitter.level
        else:
            level = 1
        if not level in LEVEL_CHOICES:
            level = 1
        regions = LEVEL_CHOICES[level]
        left, right = Country.objects.svg().filter(
            region__in=regions,
        ).order_by('?')[:2]
        self.right_answer = random.choice((left, right))
        if request.user.is_authenticated():
            user = request.user
            self.initial_level = request.user.twitter.level
        else:
            user = None
        self.new_question = Question.objects.create(
            country=self.right_answer,
            left_choice=left,
            right_choice=right,
            user=user,
        )
        return super(QuestionView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'key': self.new_question.pk}

    def get_context_data(self, **kwargs):
        ctx = super(QuestionView, self).get_context_data(**kwargs)
        x0, y0, x1, y1 = self.right_answer.mpoly.extent
        y0, y1 = -1 * y0, -1 * y1
        box = "%f %f %f %f" % (min(x0, x1),
                               min(y0, y1),
                               abs(x0 - x1),
                               abs(y0 - y1))
        ctx.update({
            'box': box,
            'question': self.new_question,
            'country': self.right_answer,
        })
        return ctx

    def form_valid(self, form):
        try:
            question = Question.objects.get(pk=form.cleaned_data['key'])
            if question.answer:
                return self.suspicious_attempt()
        except Question.DoesNotExist:
            return self.suspicious_attempt()

        if 'left' in self.request.POST and 'right' in self.request.POST:
            return self.suspicious_attempt()

        if not 'left' in self.request.POST and not 'right' in self.request.POST:
            return self.suspicious_attempt()

        if (self.request.user.is_authenticated() and
            question.user != self.request.user):
            return self.suspicious_attempt()

        if 'left' in self.request.POST:
            attr = 'left_choice'
        elif 'right' in self.request.POST:
            attr = 'right_choice'

        answer = getattr(question, attr)
        correct = question.country == answer
        delta = 2 if correct else -3
        question.answer = answer
        question.save()

        message = None
        if self.request.user.is_authenticated():
            self.request.user.twitter.score += delta
            self.request.user.twitter.save()

            current_level = self.request.user.twitter.level
            if current_level > self.initial_level:
                message = ('You just reached level %s! New location unlocked: '
                           '%s' % (current_level, NEW_REGIONS[current_level]))
            elif current_level < self.initial_level:
                message = 'You just went back to level %s' % current_level

        form = self.form_class(initial={'key': self.new_question.pk})
        return self.render_to_response(
            self.get_context_data(
                form=form,
                correct=correct,
                previous=question,
                previous_form=PreviousForm(
                    initial={'previous': question.country.mpoly},
                ),
                message=message,
            ),
        )
question = QuestionView.as_view()
