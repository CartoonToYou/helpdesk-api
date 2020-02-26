from odoo.addons.restful.common import (
    make_json_response,
    make_json_err_response,
    get_attachment,
    _att
)
from odoo.http import request
from odoo import http
from odoo.addons.restful.controllers.main import validate_token

class EquipmentController(http.Controller):
    @validate_token
    @http.route('/api/helpdesk/equipments/', auth='none', methods=['GET'])
    
    def index(self):
        equipments = self._all()
        rows = []
        res = {
            'count': len(equipments),
            'rows': rows,
            }
        for equipment in equipments:
            rows.append(self._to_json(equipment))
        return make_json_response(res)

    def _all(self, limit=None):
        if limit is not None:
            return request.env['maintenance.equipment'].search([], limit=limit)
        return request.env['maintenance.equipment'].search([])

    def _to_json(self, equipment):
        attachments = get_attachment('maintenance.equipment',equipment.id)

        res = {
            'id': equipment.id,
            'name': equipment.name,
        }

        if attachments:
            rows = []
            for att in attachments:
                rows.append(_att(att))
            res['attachments'] = rows
        else:
            res['attachments'] = ''
        return res       
        