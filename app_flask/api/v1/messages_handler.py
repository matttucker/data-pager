"""
Copyright (c) 2014 <Company>. All rights reserved.

The messages_handler module handles all messages/ API requests.
"""
from __future__ import print_function
from flask import jsonify
from flask import request

from app_flask.model.message import Message
from app_flask.utils import utils

# from pprint import pprint


def get_messages():
    """
    Get a message


    Returns:
        A message.
    """
    limit = utils.get_limit_from_query_params(request.args)
    skip = utils.get_skip_from_query_params(request.args)
    descending = utils.parse_boolean(request.args.get('descending', "false"))

    bookmark = request.args.get('bookmark', {} if descending else None)
    print("bookmark", bookmark, "descending:", descending)

    messages = Message.get_messages(
        startkey=bookmark, descending=descending, limit=limit, skip=skip)

    total_rows = messages.total_rows

    messages = [message.to_api_dict() for message in messages]
    if len(messages) == 0:
        bookmarks = ["", ""]
    elif len(messages) == 1:
        bookmarks = [messages[0]['id'], ""]
    elif len(messages) < limit:
        bookmarks = [messages[0]['id'], ""]
    else:
        bookmarks = [messages[0]['id'], messages[-1]['id']]

    if not bookmark:
        bookmarks[0] = ""

    return jsonify({'messages': messages, 'bookmarks': bookmarks, 'total_rows': total_rows})
