from django.db import models
from django.core.files.base import ContentFile
from django.urls import reverse
import qrcode
from io import BytesIO


class Court(models.Model):
    class Meta:
        verbose_name = 'Суд'
        verbose_name_plural = 'Суды'
        db_table = 'court'

    name = models.CharField(max_length=100, help_text='Наименование суда')
    kbju_code = models.CharField(max_length=20, unique=True, help_text='Уникальный код суда')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, help_text='Qr-код для суда')

    def __str__(self):
        return self.name

    # def generate_qr_code(self):
    #     base_url = ''
    #     qr_url = f'{base_url}{reverse('survey-page')}?kbju_code={self.kbju_code}'
    #
    #     qr = qrcode.make(qr_url)
    #     qr_image = BytesIO()
    #     qr.save(qr_image, format='PNG')
    #     qr_image.seek(0)
    #
    #     self.qr_code.save(f'{self.kbju_code}.png', ContentFile(qr_image.read()), save=False)


class Survey(models.Model):
    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        db_table = 'survey'

    title = models.CharField(max_length=255, help_text='Название опроса')
    description = models.TextField(blank=True, null=True, help_text='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    courts = models.ManyToManyField(Court, related_name='surveys')

    def __str__(self):
        return self.title


class CourtSurvey(models.Model):
    class Meta:
        verbose_name = 'Суд - Опрос'
        verbose_name_plural = 'Суды - Опросы'
        db_table = 'court_survey'

    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.court.name} {self.survey.title}'


class Question(models.Model):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        db_table = 'question'

    text = models.TextField(help_text='Текст вопроса')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    has_other_option = models.BooleanField(default=False, help_text='Есть ли другой вариант ответа')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class AnswerOption(models.Model):
    class Meta:
        verbose_name = 'Другой вариант ответа'
        verbose_name_plural = 'Другие варианты ответов'
        db_table = 'answer_option'

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(help_text='Текст ответа')

    def __str__(self):
        return self.question.text


class SurveyResponse(models.Model):
    class Meta:
        verbose_name = 'Ответ на опрос'
        verbose_name_plural = 'Ответы на опрос'
        db_table = 'survey_response'

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.survey


class QuestionResponse(models.Model):
    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Отвветы на вопрос'
        db_table = 'question_response'

    survey_response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)
    custom_answer = models.CharField(max_length=255, help_text='Другой ответ')

    def __str__(self):
        return self.survey_response
