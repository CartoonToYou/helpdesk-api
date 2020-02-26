
from odoo.addons.restful.common import (
    make_json_response,
    make_json_err_response,
    get_attachment,
    _att
)
from odoo.http import request
from odoo import http
from odoo.addons.restful.controllers.main import validate_token
from .category_controller import CategoryController


class AreaController(http.Controller):
    @validate_token
    @http.route('/api/helpdesk/areas', auth='none', methods=['GET'])
    def index(self):
        # print(request.httprequest.method, request.session)
        areas = self._all()
        rows = []
        res = {
            'count': len(areas),
            'rows': rows
        }
        # print(areas)
        for area in areas:
            rows.append(self._to_json(area))

        return make_json_response(res)

    def _get(self, _id):
        return request.env['helpdesk.ticket.team'].browse(_id)

    def _all(self, limit=None):
        if limit is not None:
            return request.env['helpdesk.ticket.team'].sudo().search([], limit=limit)
        return request.env['helpdesk.ticket.team'].sudo().search([])

    def _to_json(self, area):
        attachments = get_attachment('helpdesk.ticket.team', area.id)
        rows_category = [None] * len(area.category_ids)
        rows_category_index = len(area.category_ids) - 1

        res = {
            'id': area.id,
            'name': area.name,
            'categories': rows_category
        }

        if attachments:
            for att in attachments[0]:
                res['attachments'] = _att(att)
        else:
            res['attachments'] = ''
        
        if area.category_ids.exists():
            for category in area.category_ids:
                rows_category[rows_category_index] = CategoryController._to_json(self, category)
                rows_category_index -= 1

        return res
