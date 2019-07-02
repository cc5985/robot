import sys
sys.path.append("..")
from sshtunnel import SSHTunnelForwarder
#
# def UserMysql(db):
#
#     server = SSHTunnelForwarder(
#         ssh_address_or_host=('39.108.7.164', 22),
#         ssh_username='root',
#         ssh_password='Caichong416',
#         remote_bind_address=('127.0.0.1', 3306))
#     server.start()
#     myConfig = pymysql.connect(
#         user="root",
#         passwd="caichong",
#         host="127.0.0.1",
#         db=db,
#         port=server.local_bind_port)
#     sql_string='select count(*) from depth_OKEx_itc_btc_0102'
#     cursor =myConfig.cursor()
#     cursor.execute(sql_string)
#     print(cursor.fetchall())
#     myConfig.commit()
#     cursor.close()
#     myConfig.close()
#     server.stop()
#
# UserMysql('okex')
class SSHServer():
    def __init__(self,ssh_address_or_host=('39.108.7.164', 22), ssh_username='root', ssh_password='Caichong416', remote_bind_address=('127.0.0.1', 3306)):
        self.ssh_address_or_host=ssh_address_or_host
        self.ssh_username=ssh_username
        self.ssh_password=ssh_password
        self.remote_bind_address=remote_bind_address
        self.server=SSHTunnelForwarder(ssh_address_or_host=self.ssh_address_or_host,ssh_username= self.ssh_username, ssh_password=self.ssh_password, remote_bind_address=self.remote_bind_address)

    def start(self):
        self.server.start()
        self.local_bind_port=self.server.local_bind_port

    def stop(self):
        self.server.stop()