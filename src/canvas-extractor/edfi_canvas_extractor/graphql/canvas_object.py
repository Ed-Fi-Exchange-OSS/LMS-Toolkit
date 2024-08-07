# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import arrow
import pytz


class CanvasObject(object):
    """
    Base class for all classes representing objects returned by the APIs.

    This makes a call to :func:`canvasapi.canvas_object.CanvasObject.set_attributes`
    to dynamically construct this object's attributes with a JSON object.
    """

    def __getattribute__(self, name):
        return super(CanvasObject, self).__getattribute__(name)

    def __init__(self, requester, attributes):
        """
        Parameters
        ----------
        requester: class:`canvasapi.requester.Requester`
            The requester to pass HTTP requests through.
        attributes: dict
            The JSON object to build this object with.
        """
        self._requester = requester
        self.set_attributes(attributes)

    def __repr__(self):  # pragma: no cover
        classname = self.__class__.__name__
        attrs = ", ".join(
            [
                "{}={}".format(attr, val)
                for attr, val in self.__dict__.items()
                if attr != "attributes"
            ]
        )  # noqa
        return "{}({})".format(classname, attrs)

    def set_attributes(self, attributes):
        """
        Load this object with attributes.

        This method attempts to detect special types based on the field's content
        and will create an additional attribute of that type.

        Consider a JSON response with the following fields::

            {
                "name": "New course name",
                "course_code": "COURSE-001",
                "start_at": "2012-05-05T00:00:00Z",
                "end_at": "2012-08-05T23:59:59Z",
                "sis_course_id": "12345"
            }

        The `start_at` and `end_at` fields match a date in ISO8601 format,
        so two additional datetime attributes are created, `start_at_date`
        and `end_at_date`.

        attributes: dict
            The JSON object to build this object with.
        """
        for attribute, value in attributes.items():
            self.__setattr__(attribute, value)

            try:
                naive = arrow.get(str(value)).datetime
                aware = naive.replace(tzinfo=pytz.utc) - naive.utcoffset()
                self.__setattr__(attribute + "_date", aware)
            except arrow.ParserError:
                pass
            except ValueError:
                pass
