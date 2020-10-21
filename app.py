from flask import Flask, request
from flask_restful import Resource, Api

import logging
import reusables
import os

from libs.fct_lod import LoD
from libs.fct_zip import ZfS,UzU
from libs.fct_output import Output
from libs.fct_inputs import ValidateInput
from libs.fct_auth import Auth
from libs.fct_config import ConfigFile

log = reusables.get_logger('main', level=logging.DEBUG)

debug = True

conf = ConfigFile("config.json")

app = Flask(__name__)
api = Api(app)

auth = Auth(conf.auth)

# List of possible command
LOC = {
    "GET" :
        {
            'lod' : LoD,
            'zfs' : ZfS,
            'uzu' : UzU,
    },
}


class Root(Resource):
    def get(self):
        loc=LOC["GET"]
        output = Output()
        if debug:
            log.debug(request.args)

        validate = ValidateInput(request.args, auth, ttl=conf.ttl, loc=loc)
        if validate.validate() and validate.isok():
            if debug:
                log.debug("request is valid")

                Ccommand = loc[request.args['command']](conf, request.args['payload'])  # changed for each commands

                if Ccommand.isok():
                    payload = Ccommand.GetPayload()
                else :
                    payload = None

                if Ccommand.isok():
                    if debug:
                        log.debug("payload ok")
                    output.SetStatus(Ccommand.GetStatus())
                    output.SetPayload(payload)
                    return output.generate()
                else:
                    if debug:
                        log.debug("error with payload ")
                    output.SetStatus(Ccommand.GetStatus())
                    return output.generate()

        else:
            if debug:
                log.debug("request is invalid")
            output.SetStatus(validate.GetStatus())
            return (output.generate())


api.add_resource(Root, '/')

if __name__ == '__main__':
    app.run()
