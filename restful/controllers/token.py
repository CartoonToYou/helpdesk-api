# Part of odoo. See LICENSE file for full copyright and licensing details.
import json
import logging

import werkzeug.wrappers

from odoo import http
from odoo.addons.restful.common import make_json_err_response, make_json_response
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

expires_in = "restful.access_token_expires_in"


class AccessToken(http.Controller):
    """."""

    def __init__(self):

        self._token = request.env["api.access_token"]
        self._expires_in = request.env.ref(expires_in).sudo().value

    @http.route(
        "/api/auth/token", methods=["OPTIONS", "POST"], type="json", auth="none", csrf=False, cors="*"
    )
    def token(self, **params):
        _token = request.env["api.access_token"]
        db, username, password = (
            params['db'],
            params['username'],
            params['password']
        )

        # Login in odoo database:
        try:
            request.session.authenticate(db, username, password)
        except Exception as e:
            # Invalid database:
            info = "The database name is not valid {}".format((e))
            error = "invalid_database"
            Response.status = '401'
            _logger.error(info)
            res = {"error": error}
            return res

        uid = request.session.uid
        # odoo login failed:
        if not uid:
            info = "authentication failed"
            error = "authentication failed"
            _logger.error(info)
            Response.status = '401'
            res = {"error": error}
            return res
        # Generate tokens
        access_token = _token.find_one_or_create_token(
            user_id=uid, create=True)
        # Successful response:
        Response.status = '200'

        groups = []
        group_roles = request.env.user.groups_id
        for group in group_roles:
            groups.append(self._role_group(group))
            
        res = {"uid": uid,
               "user_context": request.session.get_context() if uid else {},
               "company_id": request.env.user.company_id.id if uid else None,
               "name": request.env.user.name,
               "phone_number": request.env.user.partner_id.mobile,
               "room_number": request.env.user.partner_id.street,
               "access_token": access_token,
               "expires_in": self._expires_in,
               "role_group": groups
               }
        return res

    @http.route(
        "/api/auth/token", methods=["DELETE"], type="http", auth="none", csrf=False
    )
    def delete(self, **post):
        """."""
        _token = request.env["api.access_token"]
        access_token = request.httprequest.headers.get("Authorization")
        access_token = _token.search([("token", "=", access_token)])
        if not access_token:
            info = "No access token was provided in request!"
            error = "no_access_token"
            _logger.error(info)
            return make_json_err_response(error, 401)
        for token in access_token:
            token.unlink()
        # Successful response:
        return make_json_response({"desc": "token successfully deleted", "delete": True}, 200)
    
    def _role_group(self, group):
        res = {
        'id': group.id,
        'name': group.name,
        }

        return res

