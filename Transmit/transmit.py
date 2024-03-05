import paramiko
from paramiko.proxy import ProxyCommand

# 设置代理服务器的参数
proxy_server = 'proxy.huawei.com'
proxy_port = 8080
proxy_username = 'y00801659'
# proxy_private_key = 'qwER12#$12'
proxy_password = 'qwER12#$12'

# 设置目标SSH服务器的参数
ssh_server = '120.46.207.204'
ssh_port = 22
ssh_username = 'ossuser'
# ssh_private_key = 'Huawei@Cloud8#'
ssh_password = 'Huawei@Cloud8#'

# 创建SSH客户端
proxy = paramiko.SSHClient()
proxy.load_system_host_keys()
# proxy_key = paramiko.RSAKey(filename=proxy_private_key)
# proxy.connect(proxy_server, port=proxy_port, username=proxy_username, pkey=proxy_key)
proxy.connect(proxy_server, port=proxy_port, username=proxy_username, password=proxy_password)

# 设置SSH连接的代理
# transport = ProxyCommand('ssh -W %s:%s %s@%s' % (ssh_server, ssh_port, ssh_username, ssh_server))
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(ssh_server, port=ssh_port, username=ssh_username, pkey=ssh_private_key, sock=transport)
print('nc -x %s:%d %s %d' % (proxy_server, proxy_port, ssh_server, ssh_port))
transport = ProxyCommand('nc -x %s:%d %s %d' % (proxy_server, proxy_port, ssh_server, ssh_port))
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ssh_server, port=ssh_port, username=ssh_username, password=ssh_password, sock=transport)


# 执行远程命令
stdin, stdout, stderr = ssh.exec_command('ls -l')

# 获取命令执行结果
for line in stdout:
    print(line.strip())

# 关闭SSH连接
ssh.close()
proxy.close()