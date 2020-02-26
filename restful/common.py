"""Common methods"""
import ast
import logging
import json
from datetime import date
import werkzeug.wrappers
from werkzeug.exceptions import BadRequest, NotFound
from odoo.http import request, Response
from odoo.tools import config

_logger = logging.getLogger(__name__)

def make_json_response(data, headers=None, cookies=None, status=200):
    data_json = json.dumps(data)
    if headers is None:
        headers = {}
    headers['Content-Type'] = 'application/json'
    # headers['Cache-Control'] = 'no-store'
    return Response(data_json, headers=headers)


def make_json_err_response(msg, status):
    data = {'error': msg, 'status': status}
    result = json.dumps(data)
    return Response(result, content_type='application/json', status=status)


def make_err_response(msg, status):
    return Response(msg, content_type='text/html', status=status)

def invalid_response(typ, message=None, status=401):
    """Invalid Response
    This will be the return value whenever the server runs into an error
    either from the client or the server."""
    # return json.dumps({})
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(
            {
                "type": typ,
                "message": str(message)
                if str(message)
                else "wrong arguments (missing validation)",
            }
        ),
    )

def header_check(request):
    if request.httprequest.headers['Accept'] != 'application/json':
        raise NotFound()

def get_attachment(model, id):
    attachments = request.env['ir.attachment'].search(
        [('res_model', '=', model), ('res_id', '=', id)])
    return attachments

def get_mail_message(model, id):
    messages = request.env['mail.message'].search(
        [('model', '=', model), ('res_id', '=', id)]
    )
    return messages

def _att(att):
    res = {
        'id': att.id,
        'url': config.get('host') + '/web/content/' + str(att.id)
    }
    return res

def _log(message):
    stages = request.env['mail.tracking.value'].search(
        [('mail_message_id', '=', message.id), ('field', 'like', 'stage')]
    )
    if stages:
        rows = {}
        for stage in stages:
            rows.update({
                'id': stage.id,
                'stage_id': stage.new_value_integer,
                'stage_name': stage.new_value_char,
                'created': stage.create_date
            })
    else:
        rows = ''
    return rows


