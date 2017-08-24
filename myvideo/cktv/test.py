# -*- coding: utf-8 -*-
import tushare as ts

if __name__ == '__main__':
    ts.set_token('f1e3b370fb569c6ca125fcd80e67af3850ea71f10dce45f18be15cc0d709b3df')
    datas = ts.inst_tops()
    print datas