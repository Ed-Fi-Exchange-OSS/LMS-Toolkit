# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

"""
Originally from https://github.com/ErikBoesen/schoolopy

Cloned and modified for bug fixes. Original license:

    Copyright (c) 2017 Erik Boesen

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

class _base_model(dict):
    def __init__(self, json={}):
        self.update(json)
        self.update(self.__dict__)
        self.__dict__ = self

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.json())

    def json(self):
        return dict.__repr__(self)


def _model(class_name):
    return type(class_name, (_base_model,), {})

School = _model('School')
Building = _model('Building')
User = _model('User')
Enrollment = _model('Enrollment')
Group = _model('Group')
Course = _model('Course')
Section = _model('Section')
Event = _model('Event')
BlogPost = _model('BlogPost')
BlogPostComment = _model('BlogPostComment')
Discussion = _model('Discussion')
DiscussionReply = _model('DiscussionReply')
Update = _model('Update')
UpdateComment = _model('UpdateComment')
Reminder = _model('Reminder')
MediaAlbum = _model('MediaAlbum')
Media = _model('Media')
Document = _model('Document')
GradingScale = _model('GradingScale')
GradingCategory = _model('GradingCategory')
GradingGroup = _model('GradingGroup')
Rubric = _model('Rubric')
Assignment = _model('Assignment')
FriendRequest = _model('FriendRequest')
Invite = _model('Invite')
Grade = _model('Grade')
Language = _model('Language')
Association = _model('Association')
Session = _model('Session')
MessageThread = _model('MessageThread')
Message = _model('Message')
Action = _model('Action')

class NoDifferenceError(Exception):
    """
    This exception represents a case where schoology returns a String with the API
    and makes it easier to tell what went wrong.
    """
    pass

# Ed-Fi additions
Role = _model('Role')
Submission = _model('Submission')
GradingPeriod = _model('GradingPeriod')
