#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2014 <Company>. All rights reserved.
Created by Matt Tucker on 2014-01-04.

The User module is user model for the messages service.
"""
from __future__ import print_function
from app_flask.model.model import Model

# from pprint import pprint


class Message(Model):

    """
    A Message object

    """
    doc_type = 'message'

    def __init__(self, **kwargs):
        """
        Message class

        """
        super(Message, self).__init__(**kwargs)

    @classmethod
    def wrap(cls, data):
        return cls(_d=data)

    def to_json(self):
        json = super(Message, self).to_json()
        return json

    def to_api_dict(self, version=None):
        api_dict = super(Message, self).to_api_dict(version=version)
        api_dict.update({
            'text': self.text,
            'status_date': self.status_date
        })
        return api_dict

    @staticmethod
    def get_messages(startkey=None, descending=True, limit=10, skip=None):

        if not startkey:
            if descending:
                startkey = {}
            else:
                startkey = None

        print("bookmark:" + str(startkey))
        print("descending:" + str(descending))
        print("limit:" + str(limit))
        print("skip:" + str(skip))

        messages = Message.view("messages/messages",
                                startkey=startkey,
                                descending=descending,
                                limit=limit,
                                skip=skip,
                                include_docs=True,
                                reduce=False)

        return messages
