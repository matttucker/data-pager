#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2014 <Company>. All rights reserved.
Created by Matt Tucker on 2014-01-04.

The Model module is the base model for the <service> service.
"""
import random

ID_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

from couchdbkit import Document


class Model(Document):

    """
    A Model object

    """

    @staticmethod
    def generate_id(doc_type):
        num = random.getrandbits(122)
        encoding = ''
        for _ in xrange(21):
            num, rem = divmod(num, 62)
            encoding += ID_ALPHABET[rem]
        return '{}_{}'.format(doc_type, encoding)

    @classmethod
    def wrap(cls, data):
        return cls(_d=data)

    def __init__(self, **kwargs):
        """
        Model class

        """

        super(Model, self).__init__(**kwargs)
        if '_d' not in kwargs:
            self._id = self.generate_id(self.doc_type)

    def to_api_dict(self, version=None):
        return {
            'id': self._id,
            'doc_type': self.doc_type
        }
