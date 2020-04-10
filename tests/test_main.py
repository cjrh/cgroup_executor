import os
import pwd
import time
from concurrent.futures import ProcessPoolExecutor as Executor

from cgroups import Cgroup
from cgroups.user import create_user_cgroups


# TODO: include attribution to here:
#  https://gist.github.com/tonybaloney/00c93a38bce4417262339793ae713584


def test_hello():
    print('hello')


def setup_cgroup(name):
    user = pwd.getpwuid(os.getuid())[0]
    print(user)
    create_user_cgroups(user)
    cg = Cgroup(name)
    print('cgroup', cg)
    cg.set_cpu_limit(100)
    print('memory limit', cg.memory_limit)
    cg.set_memory_limit(600)
    print('memory limit', cg.memory_limit)


def mem_grower():
    x = []
    for i in range(20):
        x.extend(list(range(2000000)))
        print(len(x))
        time.sleep(1)


def test_exe():
    cgroup_name = 'test_cgroup_executor'
    setup_cgroup(cgroup_name)
    print('after setup_cgroup')

    def dummy(cgroup_name):
        pid = os.getpid()
        print('My pid: ', pid)
        cg = Cgroup(cgroup_name)
        print(cg.pids)
        print('dummy groups', cg.cgroups)
        print('dummy user', cg.user)
        print('dummy cpu limit', cg.cpu_limit)
        print('dummy memory limit', cg.memory_limit)
        cg.add(pid)
        print('leaving dummy')

    executor = Executor(max_workers=1, initializer=dummy, initargs=(cgroup_name,))

    with executor as exe:
        f = exe.submit(mem_grower)
        # exe.submit(time.sleep, 25)
        # exe.shutdown(wait=True)


    print(f.result())
