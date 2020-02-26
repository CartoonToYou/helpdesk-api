
from odoo.addons.restful.common import (
    make_json_response,
    make_json_err_response,
    get_attachment,
    _att
)
from odoo.http import request
from odoo import http
from odoo.addons.restful.controllers.main import validate_token


class StageController(http.Controller):

    @validate_token
    @http.route('/api/helpdesk/stages', auth='none', methods=['GET'])
    def index(self):
        stages = self._all()
        rows = []
        res = {
            'count': len(stages),
            'rows': rows
        }

        for stage in stages:
            rows.append(self._to_json(stage))

        return make_json_response(res)

    # def _get(self, _id):
    #     return request.env['helpdesk.ticket.stage'].browse(_id)

    def _all(self, limit=None):
        if limit is not None:
            return request.env['helpdesk.ticket.stage'].search([], limit=limit)
        return request.env['helpdesk.ticket.stage'].search([])

    def _to_json(self, stage):
        attachments = get_attachment(
            'helpdesk.ticket.stage', stage.id)
        res = {
            'id': stage.id,
            'name': stage.name,
        }

        if attachments:
            for att in attachments[0]:
                res['attachments'] = _att(att)
        else:
            res['attachments'] = ''

        return res
