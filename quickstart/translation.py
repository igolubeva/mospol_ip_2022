# coding: utf-8
from modeltranslation.translator import translator, TranslationOptions
from quickstart.models import Advice


class AdviceOptions(TranslationOptions):
    fields = ('title', 'text')


translator.register(Advice, AdviceOptions)
