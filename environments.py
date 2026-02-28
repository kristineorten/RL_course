import grid_env as env

def env1():
    e = env.GridEnv(4,5, 0,0, 3,4)
    return e

def env2():
    e = env.GridEnv(4,5, 0,0, 3,4)
    e.add_wall(2,0)
    return e