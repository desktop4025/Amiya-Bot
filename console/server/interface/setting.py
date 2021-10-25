import os
import yaml

from flask import Flask, request
from core.config import func_setting_path
from core.database.models import ReplaceText
from core.database.manager import select_for_paginate

from ..response import response


def setting_controller(app: Flask):
    @app.route('/getFunctionSetting', methods=['POST'])
    def get_function_setting():
        if os.path.exists(func_setting_path):
            with open(func_setting_path, mode='r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return response(data)
        return response(message='文件尚未创建')

    @app.route('/saveFunctionSetting', methods=['POST'])
    def save_function_setting():
        params = request.json
        with open(func_setting_path, mode='w+', encoding='utf-8') as f:
            f.write(yaml.dump(params))
        return response(message='保存成功')

    @app.route('/setting/getReplaceTextByPages', methods=['POST'])
    def get_replace_text_by_pages():
        params = request.json
        equal = {}
        contains = {}

        if params['search']:
            equal = {}
            contains = {}

        data, count = select_for_paginate(ReplaceText,
                                          equal,
                                          contains,
                                          page=params['page'],
                                          page_size=params['pageSize'])

        return response({'count': count, 'data': data})

    @app.route('/setting/changeReplaceTextStatus', methods=['POST'])
    def change_replace_text_status():
        params = request.json
        replace_id = params['replace_id']

        ReplaceText \
            .update(is_global=params['is_global'], is_active=params['is_active']) \
            .where(ReplaceText.replace_id == replace_id) \
            .execute()

        return response(message='设置成功')