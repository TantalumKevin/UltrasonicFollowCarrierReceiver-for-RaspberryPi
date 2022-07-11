class Motor:
    '''
    电机类，包含
    当前调速信息（变量）
    pid（参数）
    pid（函数）
    运动（函数）

    归一

    串
    out=p(in)+i(in)+d(in)

    并
    out=d(i(p(in)))
    '''
    def __init__(self):
        self.speed = 0
        self.
