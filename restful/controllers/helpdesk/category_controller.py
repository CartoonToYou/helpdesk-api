
from odoo.addons.restful.common import (
    make_json_response,
    make_json_err_response,
    get_attachment,
    _att
)
from odoo.http import request
from odoo import http
from odoo.addons.restful.controllers.main import validate_token


class CategoryController(http.Controller):
    @validate_token
    @http.route('/api/helpdesk/categories', auth='none', methods=['GET'])
    
    def index(self):
        categories = self._all()
        rows = []
        res = {
            'count': len(categories),
            'rows': rows
        }

        for category in categories:
            rows.append(self._to_json(category))

        return make_json_response(res)

    def _get(self, _id):
        return request.env['helpdesk.ticket.category'].browse(_id)

    def _all(self, limit=None):
        if limit is not None:
            return request.env['helpdesk.ticket.category'].search([], limit=limit)
        return request.env['helpdesk.ticket.category'].search([])

    def _to_json(self, category):
        attachments = get_attachment(
            'helpdesk.ticket.category', category.id)
        res = {
            'id': category.id,
            'name': category.name,
        }

        if attachments:
            for att in attachments[0]:
                res['attachments'] = _att(att)
        else:
            res['attachments'] = ''

        return res
