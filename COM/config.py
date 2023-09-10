import os
import DATA.common_globals as cg
from COM.load import load


def config():

    if not os.path.isdir(f'{cg.PATH}/VIDS/TEMP'):
        os.makedirs(f'{cg.PATH}/VIDS/TEMP')

    rfq_path = f'{cg.PATH}/DATA/refresh_freq'
    err_path = f'{cg.PATH}/DATA/errors'
    tgt_path = f'{cg.PATH}/DATA/target'
    fs_api_path = f'{cg.PATH}/DATA/fs_api'
    cfg_path = f'{cg.PATH}/DATA/config'

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
        cg.refresh_freq = cfg['refresh_freq']
        cg.MASTER = cfg['MASTER']
        cg.admins = cfg['admins']
        cg.notify_users.add(cg.MASTER)
