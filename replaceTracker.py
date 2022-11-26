import qbittorrentapi
from transmission_rpc import Client
from configparser import ConfigParser
import os

if not os.path.exists('config.ini'):
    print('未检测到配置文件，请填写生成的config.ini')
    with open('config.ini', 'w') as cf:
        print('[replace]', file=cf)
        print('from: azusa.ru', file=cf)
        print('to: azusa.wiki', file=cf)
        print('', file=cf)
        print('[qb]', file=cf)
        print('ip: 192.168.1.2', file=cf)
        print('port: 9001', file=cf)
        print('username: admin', file=cf)
        print('password: adminadmin', file=cf)
        print('', file=cf)
        print('[tr]', file=cf)
        print('ip: 192.168.1.2', file=cf)
        print('port: 9002', file=cf)
        print('username: admin', file=cf)
        print('password: adminadmin', file=cf)
        input('按回车退出')
    exit()

# 使用前先安装qbittorrentapi，使用以下命令：
# pip install qbittorrent-api transmission-rpc

config = ConfigParser()
config.read('config.ini')

src = config['replace']['from']
dest = config['replace']['to']

qb = qbittorrentapi.Client( # 客户端信息
    host=config['qb']['ip'],
    port=config['qb']['port'],
    username=config['qb']['username'],
    password=config['qb']['password']
)

try:
    qb.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

print('正在获取qb种子信息...')
for torrent in qb.torrents_info():
    if src in torrent.tracker:
        print('正在替换种子tracker：' + torrent.name)
        new_tracker = torrent.tracker.replace(src, dest, 1)
        torrent.edit_tracker(torrent.tracker, new_tracker)

tr = Client(
    host=config['tr']['ip'],
    port=config['tr']['port'],
    username=config['tr']['username'],
    password=config['tr']['password']
    )

print('正在获取tr种子信息...')
for torrent in tr.get_torrents():
    for tracker in torrent.trackers:
        if src in tracker['announce']:
            print('正在替换种子tracker：' + torrent.name)
            new_tracker = tracker['announce'].replace(src, dest, 1)
            tr.change_torrent(torrent.id, trackerReplace=(tracker['id'], new_tracker))

input('按回车退出')