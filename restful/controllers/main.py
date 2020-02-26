"""Part of odoo. See LICENSE file for full copyright and licensing details."""

import functools
import logging
import werkzeug.wrappers
import json

from odoo import http
from odoo.addons.restful.common import (
    make_json_err_response
)
from odoo.http import request, Response

_logger = logging.getLogger(__name__)


def validate_token(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        access_token = request.httprequest.headers.get("Authorization")
        if not access_token:
            if request.httprequest.method == 'POST':
                info = "missing access token in request header"
                error = "missing access token in request header"
                Response.status = '401'
                _logger.error(info)
                res = {"error": error}
                return res
            return make_json_err_response("missing access token in request header", 401)

        access_token_data = (
            request.env["api.access_token"]
            .sudo()
            .search([("token", "=", access_token)], order="id DESC", limit=1)
        )

        if (
            access_token_data.find_one_or_create_token(
                user_id=access_token_data.user_id.id
            )
            != access_token
        ):
            if request.httprequest.method == 'POST':
                info = "token seems to have expired or invalid"
                error = "token seems to have expired or invalid"
                Response.status = '401'
                _logger.error(info)
                res = {"error": error}
                return res
            elif request.httprequest.method == 'GET':
                info = "token seems to have expired or invalid"
                error = "token seems to have expired or invalid"
                Response.status = '401'
                _logger.error(info)
                res = {"error": error}
                return res
            return make_json_err_response("token seems to have expired or invalid", 401)

        request.session.uid = access_token_data.user_id.id
        request.uid = access_token_data.user_id.id
        return func(self, *args, **kwargs)
    return wrap


_routes = ["/api/<model>", "/api/<model>/<id>", "/api/<model>/<id>/<action>"]


class APIController(http.Controller):
    def __init__(self):
        self._model = "ir.model"
