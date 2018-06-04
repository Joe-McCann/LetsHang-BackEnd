"""Map Resource Submodule"""

import falcon
import json
import letshang.Map_API.mapMaker as mapMaker
from falcon_cors import CORS

class mapResource(object):
    """
    mapResource class
    This class handles the REST API resource for a map
    """

    def on_post(self, req, resp):
        """
        on_get method
        This method handles the REST get verb. This function should only be
        invoked by the Falcon framework.

        Arguments:
        req       HTTP request (incoming)
        resp      HTTP response (outgoing)

        Request Format:
        {
            "mapData":{
                "someID":{
                    "address":"someaddress"
                    "color":"somehex"
                }
                ...
            }
        }
        """

        if req.content_length:
            data =  json.loads(req.stream.read().decode('utf-8'))
            print(data)
            mMaker = mapMaker.mapMaker(data)
            print(mMaker)
            ret_data = mMaker.getDict()

        resp.body = json.dumps(ret_data, ensure_ascii=False)
        resp.status = falcon.HTTP_200