import io
import paramiko


def ssh_cmd(host=None, port=None, username=None, private_key=None, cmd=None):
    file_pk = io.StringIO(private_key)
    loaded_private_key = paramiko.RSAKey.from_private_key(file_pk)

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_client.connect(
        hostname=host, port=port, username=username, pkey=loaded_private_key
    )
    channel = ssh_client.get_transport().open_session()

    channel.exec_command(cmd)

    exit_code = channel.recv_exit_status()
    output = channel.recv(1000000000)

    return {"exit_code": exit_code, "output": output}


def task(**kwargs):
    default_timeout = 30  # seconds
    default_expected_exit_code = 0

    body = kwargs.get("body")
    params = body.get("params")

    username = params.get("username")
    host = params.get("host")
    port = params.get("port")
    command = params.get("command")
    private_key = params.get("private_key")

    timeout = params.get("timeout") or default_timeout
    expected_exit_code = params.get("expected_exit_code") or default_expected_exit_code

    try:
        result = ssh_cmd(
            host=host, port=port, username=username, private_key=private_key, cmd=command
        )

        exit_code = result.get("exit_code")

        if exit_code == expected_exit_code:
            return {"exit_code": exit_code}
        else:
            raise Exception({"exit_code": exit_code})
    except Exception as e:

        raise e

    return {}
