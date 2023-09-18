import os
import DATA.common_globals as cg
from COM.load import load


def config():

    if not os.path.isdir(f'{cg.PATH}/VIDS/TEMP'):
        os.makedirs(f'{cg.PATH}/VIDS/TEMP')

    fs_api_path = f'{cg.PATH}/DATA/fs_api'
    cfg_path = f'{cg.PATH}/DATA/config'

    if os.path.isfile(fs_api_path):
        fs_api = load(fs_api_path)
        cg.lives_url = fs_api['lives_url']
        cg.links_url = fs_api['links_url']
        cg.user_url = fs_api['user_url']
        cg.follow_url = fs_api['follow_url']
        cg.host = fs_api['host']
        cg.main_page_id = fs_api['main_page_id']
        cg.user_page_id = fs_api['user_page_id']
        cg.referer = fs_api['referer']

    if os.path.isfile(cfg_path):
        cfg = load(cfg_path)
        cg.config = cfg
        cg.fs_user_token = cfg['fs_user_token']
        cg.fs_user_uid = cfg['fs_user_uid']
        cg.target = cfg['target']
        cg.errors = cfg['errors']
        cg.refresh_freq = cfg['refresh_freq']
        cg.MASTER = cfg['MASTER']
        cg.admins = cfg['admins']
        cg.notify_users = cfg['notify_users']
        cg.notify_users.add(cg.MASTER)
        cg.notify_users.add(-1001732942884)
        cg.admins.add(cg.MASTER)
