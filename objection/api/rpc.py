from flask import Blueprint, jsonify, request, abort

from objection.state.connection import state_connection
from ..utils.helpers import to_snake_case

bp = Blueprint('rpc', __name__, url_prefix='/rpc')


@bp.route('/invoke/<string:method>', methods=('GET', 'POST'))
def invoke(method):
    """
        将呼叫桥接到Frida RPC。端点可以来自代理的RPC导出。

响应默认为JSON编码，但通过添加?json=false作为查询字符串参数，可以是原始格式

        :param method:
        :return:
    """

    method = to_snake_case(method)

    # post requests require a little more validation, so do that
    if request.method == 'POST':

        # ensure we have some JSON formatted post data
        post_data = request.get_json(force=True, silent=True)
        if not post_data:
            return abort(jsonify(message='POST request without a valid body received'))

    try:

        rpc = state_connection.get_api()

    except Exception as e:
        return abort(jsonify(message='Failed to talk to the Frida RPC: {e}'.format(e=str(e))))

    try:

        # invoke the method based on the http request type
        if request.method == 'POST':
            response = getattr(rpc, method)(*post_data.values())

        if request.method == 'GET':
            response = getattr(rpc, method)()

        if 'json' in request.args and request.args.get('json').lower() == 'false':
            return response

    except Exception as e:
        return abort(jsonify(message='Failed to call method: {e}'.format(e=str(e))))

    return jsonify(response)
