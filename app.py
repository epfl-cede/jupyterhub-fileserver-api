from flask import Flask, request
from flask_restful import Resource, Api

import logging
import os

from libs.fct_lod import LoD, Ls, LoF
from libs.fct_zip import ZfS, UzU
from libs.fct_output import Output
from libs.fct_inputs import ValidateInput
from libs.fct_auth import Auth
from libs.fct_config import ConfigFile

from libs.flask_stats.flask_stats import Stats

# Configure logging
#
# Evaluate log level setting. Set 'LOGLEVEL' env variable to configure.
log = logging.getLogger("main")
logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO").upper(),
)

# Silence werkzeug logger, replaced by stats logging
logging.getLogger("werkzeug").disabled = True

conf = ConfigFile("config.json")

app = Flask(__name__)
api = Api(app)
Stats(app)
auth = Auth(conf.auth)

log.info("API ready")


class CallFct(Resource):
    def run(self, fct, request):
        output = Output()
        log.debug(request.args)

        validate = ValidateInput(request.args, auth, ttl=conf.ttl)
        if validate.validate() and validate.is_ok():
            log.debug("request is valid")

            command = fct(
                conf, request.args["payload"], request.files
            )  # changed for each commands

            if command.is_ok():
                payload = command.get_payload()
                log.debug("Payload fetched: {0}".format(payload))
                output.set_payload(payload)
            else:
                log.error("error with payload in callfct: {0}".format(command.status))

            output.set_status(command.get_status())
            return output.generate()

        else:
            log.error("request is invalid")
            output.set_status(validate.get_status())
            return output.generate()


@app.route("/")
def hello():
    output = Output()
    output.set_status(status={"code": 0, "status": "OK"})
    return output.generate()


@app.route("/healthz")
def healthz():
    return "OK"


@app.route("/ls", methods=["GET"])
def get_ls():
    cfct = CallFct()
    return cfct.run(Ls, request)


@app.route("/lof", methods=["GET"])
def get_lof():
    cfct = CallFct()
    return cfct.run(LoF, request)


@app.route("/lod", methods=["GET"])
def get_lod():
    cfct = CallFct()
    return cfct.run(LoD, request)


@app.route("/zfs", methods=["GET"])
def get_zfs():
    cfct = CallFct()
    return cfct.run(ZfS, request)


@app.route("/uzu", methods=["POST"])
def post_uzu():
    cfct = CallFct()
    return cfct.run(UzU, request)


if __name__ == "__main__":  # pragma: nocover
    app.run()
