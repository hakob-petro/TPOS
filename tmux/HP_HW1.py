import os
import libtmux
import argparse
from tqdm import trange
from datetime import datetime


def get_args():
    parser = argparse.ArgumentParser(prog="python ./HP_HW1.py",
                                     description="Linux & Tmux homework.",
                                     usage='%(prog)s [options] arguments')
    parser.add_argument("command", type=str,
                        help="Pass which command you whant to run.\nAvaiable commands: [start, stop, stop_all].")
    parser.add_argument("params", nargs="*",
                        help="Pass the number of env, that you whant to start if the command is start, "
                             "else the name of session and the number of env which you whant to delete.")
    return parser.parse_args()


def start(num_users: str, base_dir: str = './', name: str = None, ports: str = "ports.txt"):
    """
    Запустить $num_users ноутбуков. У каждого рабочай директория $base_dir+$folder_num
    """

    server = libtmux.Server()
    tpos_session = server.new_session(session_name=name)
    curr_window = tpos_session.attached_window
    curr_window.rename_window("0")

    with open(ports, 'r') as f:
        ports = f.read().split()

    pbar = trange(int(num_users), desc="Creating jupyter notebook environment...")
    for user_num in pbar:
        curr_pane = curr_window.attached_pane

        jupyter_dir = os.path.join(base_dir, str(user_num))
        curr_pane.send_keys(f"mkdir {jupyter_dir}", enter=True)
        # I can install manually all third-party modules to venv, but I
        # don't do that to econom memory, that's why I will inhertiate from gloabal site-packages.
        venv_dir = os.path.join(jupyter_dir, 'tpos_venv')
        curr_pane.send_keys(f"python3 -m venv {venv_dir}", enter=True)
        curr_pane.send_keys(f"source {venv_dir}/bin/activate", enter=True)
        curr_pane.send_keys("pip install jupyter", enter=True)

        # Here I can use modules secrets or tokenize or uuid modules, but I decided to use date as unique token.
        now = datetime.now()
        token = str(user_num) + now.strftime("%Y_%m_%d_%H_%M_%S_%f")
        curr_pane.send_keys(f"jupyter notebook --port {ports[user_num]} --no-browser"
                            f" --NotebookApp.token='{token}' --NotebookApp.notebook_dir={jupyter_dir} &", enter=True)
        pbar.write(f"Started environment {user_num} with token {token} on {ports[user_num]} port!")
        pbar.update()
        pbar.refresh()

        if user_num + 1 != int(num_users):
            curr_window = tpos_session.new_window(attach=True, window_name=str(user_num + 1))


def stop(session_name, num):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    @:param num: номер окружения, кот. можно убить
    """
    server = libtmux.Server()
    session = server.find_where({"session_name": session_name})
    win_from_del = session.select_window(num)
    curr_pane = win_from_del.attached_pane
    curr_pane.send_keys(f"PID=$! && kill $PID", enter=True)


def stop_all(session_name):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    """
    server = libtmux.Server()
    session = server.find_where({"session_name": session_name})
    for window in session.list_windows():
        curr_pane = window.attached_pane
        curr_pane.send_keys(f"PID=$! && kill $PID", enter=True)


def main():
    args = vars(get_args())

    if args["command"] == "start":
        now = datetime.now()
        name = "tpos_" + now.strftime("%Y_%m_%d_%H_%M_%S")
        os.mkdir(name)
        start(args["params"][0], base_dir=name, name=name)
    elif args["command"] == "stop":
        stop(args["params"][0], args["params"][1])
    elif args["command"] == "stop_all":
        stop_all(args["params"][0])
    else:
        raise ValueError("Passed wrong command.\nAvaiable commands: [start, stop, stop_all].")


if __name__ == "__main__":
    main()
