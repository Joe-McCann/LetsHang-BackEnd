"""Events Resource Submodule"""

import falcon
import json

class eventsResource(object):

    def on_get(self, req, resp):
        
        # Hardcoding the resource until Firebase is hooked in.
        events = {
            'events': [
                {
                    'id': '123456789',
                    'eventDescription': 'Just hanging out',
                    'date': '2018-03-22',
                    'time': '18:30',
                    'invited': [
                        {
                            'id': '123456789',
                            'firstName': 'Bill',
                            'lastName': 'McCann',
                            'nickName': 'Dad',
                            'address': '9 Appletree Dr., Matawan, NJ',
                            'phone': '732-812-0367',
                            'email': 'bill.mccann@gmail.com',
                        },
                        {
                            'id': '987654321',
                            'firstName': 'William',
                            'lastName': 'McCann',
                            'nickName': 'Joe',
                            'address': '9 Appletree Dr., Matawan, NJ',
                            'phone': '732-609-7755',
                            'email': 'wjm9@njit.edu',
                        }
                    ]
                },
                {
                    'id': '162748596',
                    'eventDescription': 'Just hanging out',
                    'date': '2018-03-22',
                    'time': '18:30',
                    'invited': [
                        {
                            'id': '123456789',
                            'firstName': 'Bill',
                            'lastName': 'McCann',
                            'nickName': 'Dad',
                            'address': '9 Appletree Dr., Matawan, NJ',
                            'phone': '732-812-0367',
                            'email': 'bill.mccann@gmail.com',
                        },
                        {
                            'id': '869504734',
                            'firstName': 'Susan',
                            'lastName': 'McCann',
                            'nickName': '',
                            'address': '9 Appletree Dr., Matawan, NJ',
                            'phone': '848-459-2130',
                            'email': 'susan.m.mccann@gmail.com',
                        }
                    ]
                }
            ]
        }
        resp.body = json.dumps(events, ensure_ascii=False)
        resp.status = falcon.HTTP_200