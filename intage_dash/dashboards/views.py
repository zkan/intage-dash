from django.shortcuts import render
from django.views.generic import TemplateView

import pandas as pd

from .utils import clean_html
from form_submissions.models import FormResponse
from typeforms.models import Typeform


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, typeform_uid):
        typeform = Typeform.objects.get(uid=typeform_uid)
        questions = typeform.payload['questions']
        df_questions = pd.DataFrame(questions)

        form_responses = FormResponse.objects.filter(typeform=typeform)
        answers = [each.answers for each in form_responses if each.answers]
        df_answers = pd.DataFrame(answers)

        question_groups = list(filter(
            lambda x: type(x) == str, df_questions.group.unique()
        ))

        charts = []
        for each_question_group in question_groups:
            chart = {'data': []}
            chart['id'] = each_question_group
            chart['label'] = df_questions[
                df_questions['id'] == each_question_group
            ]['question'].iloc[0] + '...'
            questions_each_group = df_questions[
                df_questions['group'] == each_question_group
            ][['id', 'question']]
            question_list = zip(
                questions_each_group.id,
                questions_each_group.question
            )
            for idx, question in question_list:
                chart['data'].append(
                    [
                        clean_html(question.replace('\xa0', '')),
                        df_answers[idx].mean()
                    ]
                )
            charts.append(chart)

        chart = {'data': []}
        chart['id'] = 'group_others'
        chart['label'] = 'Others'
        questions_in_no_group = df_questions[
            df_questions['group'].isnull() &
            df_questions['id'].str.contains('rating_')
        ][['id', 'question']]
        question_list = zip(
            questions_in_no_group.id,
            questions_in_no_group.question
        )
        for idx, question in question_list:
            chart['data'].append(
                [
                    clean_html(question.replace('\xa0', '')),
                    df_answers[idx].mean()
                ]
            )
        charts.append(chart)

        return render(
            request,
            self.template_name,
            {
                'charts': charts
            }
        )


class DashboardBranchView(TemplateView):
    template_name = 'dashboard_branch.html'

    def get(self, request, typeform_uid):
        typeform = Typeform.objects.get(uid=typeform_uid)
        questions = typeform.payload['questions']
        df_questions = pd.DataFrame(questions)

        form_responses = FormResponse.objects.filter(typeform=typeform)
        answers = [each.answers for each in form_responses if each.answers]
        df_answers = pd.DataFrame(answers)

        branch_column_name = 'list_53368385_choice'
        branches = list(filter(
            lambda x: type(x) == str, df_answers[branch_column_name].unique()
        ))

        question_groups = list(filter(
            lambda x: type(x) == str, df_questions.group.unique()
        ))

        charts = []
        for each_question_group in question_groups:
            chart = {'data': []}
            chart['id'] = each_question_group
            chart['label'] = df_questions[
                df_questions['id'] == each_question_group
            ]['question'].iloc[0] + '...'
            questions_in_group = df_questions[
                df_questions['group'] == each_question_group
            ][['id', 'question']]
            question_list = zip(
                questions_in_group.id,
                questions_in_group.question
            )
            for question_id, question in question_list:
                for idx, each_branch in enumerate(branches):
                    if idx == 0:
                        data_point = [
                            clean_html(question.replace('\xa0', ''))
                        ]
                    df_branch = df_answers[
                        df_answers[branch_column_name] == each_branch
                    ]
                    data_point.append(df_branch[question_id].mean())
                chart['data'].append(data_point)
            charts.append(chart)

        chart = {'data': []}
        chart['id'] = 'group_others'
        chart['label'] = 'Others'
        questions_in_no_group = df_questions[
            df_questions['group'].isnull() &
            df_questions['id'].str.contains('rating_')
        ][['id', 'question']]
        question_list = zip(
            questions_in_no_group.id,
            questions_in_no_group.question
        )
        for question_id, question in question_list:
            for idx, each_branch in enumerate(branches):
                if idx == 0:
                    data_point = [
                        clean_html(question.replace('\xa0', ''))
                    ]
                df_branch = df_answers[
                    df_answers[branch_column_name] == each_branch
                ]
                data_point.append(df_branch[question_id].mean())
            chart['data'].append(data_point)
        charts.append(chart)

        branches = ['Score'] + branches

        return render(
            request,
            self.template_name,
            {
                'branches': branches,
                'charts': charts
            }
        )
