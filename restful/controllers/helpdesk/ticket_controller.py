from odoo.addons.restful.common import (
    make_json_response,
    make_json_err_response,
    invalid_response,
    get_attachment,
    get_mail_message,
    _att,
    _log
)
from odoo.http import request
from odoo import http
from odoo.addons.restful.controllers.main import validate_token
from mimetypes import guess_extension
from urllib.request import urlretrieve
import time


class TicketController(http.Controller):
    @validate_token
    @http.route('/api/helpdesk/tickets', auth='none', methods=['GET'])
    def index(self):
        tickets = self._all()
        rows = []
        res = {
            'count': len(tickets),
            'rows': rows,
        }

        for ticket in tickets:
            rows.append(self._to_json(ticket))

        return make_json_response(res)

    @validate_token
    @http.route('/api/helpdesk/ticket', auth='none', type='json', methods=['POST'], csrf=False)
    def store(self, **params):
        channel = request.env['helpdesk.ticket.channel'].search(
            [['name', '=', 'API']])
        user = request.env['res.users'].search(
            [['id', '=', request.session['uid']]])
        assigned_group = request.env['res.groups'].search(
            [['name', '=', 'Helpdesk Manager']])
        # print(params['attachments'])
        # print(channel)
        if params['attachments']:
            file_attachements = params['attachments']
        else:
            file_attachements = []

        params.pop('attachments')

        params['channel_id'] = channel.id
        params['partner_id'] = user.partner_id.id
        params['partner_name'] = user.partner_id.name
        params['group_id'] = assigned_group.id

        ticket = request.env['helpdesk.ticket'].create(params)

        if file_attachements:
            for file in file_attachements:
                file_name, mime_type = urlretrieve(file['data'])
                file_name = 'ticket' + \
                    time.strftime('%Y-%m-%d.%H:%M:%S') + \
                    guess_extension(mime_type.get_content_type())
                data = file['data'].split(',')
                files = request.env['ir.attachment'].create(
                    {'name': file_name, 'datas': data[1], 'datas_fname': file_name, 'res_model': 'helpdesk.ticket', 'res_id': ticket.id, })

        return self._to_json(ticket)

    @validate_token
    @http.route('/api/helpdesk/stage/<int:_id>', auth="none", type='json', methods=['PUT'], csrf=False)
    def put(self,_id, **params):
        ticket = self._get(_id)
        if not ticket.exists():
            return make_json_err_response('Not found', 404)
        else:
            user = request.env['res.users'].search(
                [['id', '=', request.session['uid']]])
            params['id'] = ticket.id
            params['partner_id'] = user.partner_id.id
            params['partner_name'] = user.partner_id.name
            ticket.write(params)
        return params

    @validate_token
    @http.route('/api/helpdesk/ticket/<int:_id>', auth='none', methods=['GET'] )
    def show(self, _id):
        ticket = self._get(_id)
        if not ticket.exists():
            return make_json_err_response('Not found', 404)
        return make_json_response(self._to_json(ticket))

    def _get(self, _id):
        return request.env['helpdesk.ticket'].browse(_id)

    def _all(self, limit=None):
        if limit is not None:
            tickets = request.env['helpdesk.ticket'].search([], limit=limit)
            return tickets
        else:
            tickets = request.env['helpdesk.ticket'].search([])
            return tickets

    def _to_json(self, ticket):
        
        attachments = get_attachment(
            'helpdesk.ticket', ticket.id)

        messages = get_mail_message(
            'helpdesk.ticket',ticket.id)

        res = {
            'id': ticket.id,
            'stage_name': ticket.stage_id.name,
            'stage_id': ticket.stage_id.id,
            'number': ticket.number,
            'name': ticket.name,
            'priority': ticket.priority,
            'description': ticket.description,
            'created': ticket.create_date
        }

        if attachments:
            rows = []
            for att in attachments:
                rows.append(_att(att))
            res['attachments'] = rows
        else:
            res['attachments'] = ''

        if messages:
            rows = []
            for message in messages:
                rows.append(_log(message))
            res['stages'] = rows
        else:
            res['stages'] = ''

        if ticket.team_id:
            res['area'] = {
                'id': ticket.team_id.id,
                'name': ticket.team_id.name
            }
        else:
            res['area'] = ''

        if ticket.partner_id:
            res['partner'] = {
                'id': ticket.partner_id.id,
                'name': ticket.partner_id.name,
                'room_number': ticket.partner_id.street,
                'phone_number': ticket.partner_id.mobile,
            }
        else:
            res['partner'] = ''

        if ticket.category_id:
            attachments = get_attachment('helpdesk.ticket.category', ticket.category_id.id)
            res_category = {
                'id': ticket.category_id.id,
                'name': ticket.category_id.name,
            }
            if attachments:
              for att in attachments[0]:
                res_category['attachments'] = _att(att)
            else:
                res_category['attachments'] = ''
            res['category'] = res_category
        else:
            res['category'] = ''

        return res
