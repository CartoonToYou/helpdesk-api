import json

from odoo.addons.restful.common import (
    make_json_response,
    make_json_err_response,
    get_attachment,
    _att
)
from datetime import datetime
from odoo.http import request
from odoo import http
from odoo.addons.restful.controllers.main import validate_token
from urllib.request import urlopen,urlretrieve
from urllib.parse import urlparse
from odoo.tools import config

class ScheduleController(http.Controller):
    @validate_token
    @http.route('/api/helpdesk/schedules/', auth='none', methods=['GET'])
    
    def index(self):
        schedules = self._all()
        rows = []
        res = {
            'count': len(schedules),
            'rows': rows,
            }
        for schedule in schedules:
            rows.append(self._to_json(schedule))
        return make_json_response(res)

    def _all(self, limit=None):
        if limit is not None:
            return request.env['maintenance.request'].search([], limit=limit)
        return request.env['maintenance.request'].search([])
    
    def _to_json(self, equipment):
        res = {
            'id': equipment.id,
            'name': equipment.name,
            'start_date': equipment.schedule_date,
            'end_date': equipment.end_date,
        }

        if equipment.equipment_id:
            attachments = get_attachment('maintenance.equipment',equipment.equipment_id.id)
            res_category = {
                'id': equipment.equipment_id.id,
                'name': equipment.equipment_id.name,
            }
            res['category'] = res_category
            if attachments:
              for att in attachments:
                res_category['attachments'] = _att(att)
            else:
                res_category['attachments'] = ''
        else:
            res['cateory'] = ''

        return res

    @validate_token
    @http.route('/api/helpdesk/schedule', auth='none', type='json', methods=['POST'], csrf=False)
    def store(self, **params):
        schedule = request.env["maintenance.request"].create(params)
        return self._to_json(schedule)

        # ========================
        # ** create loop params **
        # ========================
        # schedules = params["schedules"]
        # for schedule in schedules:
        #     recordSchedule = request.env['maintenance.request'].create(schedule)
        # return schedules

    @validate_token
    @http.route('/api/helpdesk/schedule/<int:_id>', auth='none', type='json', methods=['PUT'], csrf=False)
    def put(self,_id, **params):
        schedule = request.env['maintenance.request'].browse(_id)
        if not schedule.exists():
            return make_json_err_response('Not found', 404)
        else:
            schedule.write(params)
        return params


        # ========================
        # ** write loop params **
        # ========================
        # schedules = params["schedules"]
        # paramSchedule = request.env['maintenance.request'].browse(_id)
        # for schedule in schedules:
        #     if not paramSchedule.exists():
        #         return make_json_err_response('Not found', 404)
        #     else:
        #         selectedSchedule = request.env['maintenance.request'].browse(schedule["id"])
        #         selectedSchedule.write(schedule)
        # return schedules
   
