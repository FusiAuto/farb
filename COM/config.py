import os
import DATA.common_globals as cg
from COM.load import load


def config(path):
    rfq_path = f'{path}/DATA/refresh_freq'
    err_path = f'{path}/DATA/errors'
    tgt_path = f'{path}/DATA/target'
    fs_api_path = f'{path}/DATA/fs_api'
    cfg_path = f'{path}/DATA/config'

    if os.path.isfile(rfq_path):
        cg.refresh_freq = load(rfq_path)

    if os.path.isfile(err_path):
        cg.errors = load(err_path)

    if os.path.isfile(tgt_path):
        cg.target = load(tgt_path)

    if os.path.isfile(fs_api_path):
        fs_api = load(fs_api_path)
        cg.lives_url = fs_api['lives_url']
        cg.links_url = fs_api['links_url']
        cg.host = fs_api['host']
        cg.page_id = fs_api['page_id']
        cg.referer = fs_api['referer']

    if os.path.isfile(cfg_path):
        cfg = load(cfg_path)
        cg.fs_user_token = cfg['fs_user_token']
        cg.fs_user_uid = cfg['fs_user_uid']
        cg.target = cfg['target']
        cg.errors = cfg['errors']
        cg.MASTER = cfg['MASTER']
        cg.admins = cfg['admins']
