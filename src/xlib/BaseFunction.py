#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

# from gevent import Greenlet, queue
# import gevent

import threading



class Singleton(type):
    """Singleton Metaclass"""

    def __init__(self, name, bases, dic):
        super(Singleton, self).__init__(name, bases, dic)
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.instance


class DelayCall:
    """延迟调用对象\n
    """

    def __init__(self, f, *args, **kw):
        """
        @param f: function f是一个function对象\n
        @param args: f的必要参数\n
        @param kw: f的可选参数\n
        """
        self.f = f
        self.args = args
        self.kw = kw

    def call(self):
        """调用执行函数，并且返回结果\n
        """
        return self.f(*self.args, **self.kw)


class Timer(threading.Thread):
    """
    threading._Timer
    t = Timer(30.0, f, args=[], kwargs={})
    t.start()
    t.cancel()     # stop the timer's action if it's still waiting

    timer = threading.Timer(2.0, hello, ["Hawk"])
    timer.start()

    def __init__(self, interval, function, args=[], kwargs={}):

    """

    def __init__(self, interval, function, *args, **kwargs):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = threading.Event()

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()


# class Timer(Greenlet):
# 	def __init__(self, seconds, f, *args, **kw):
# 		"""以一个微线程的方式实现一个定时器\n
# 		"""
# 		Greenlet.__init__(self)
# 		self.seconds = seconds
# 		self.delay_call = DelayCall(f, *args, **kw)
#
# 	def cancel(self):
# 		"""取消定时器\n
# 		特别注意：
# 		1，block = True的情况，在自己的回调函数中kill,一定会阻塞
# 		2，block = True的情况，在自己的回调函数，kill自己之后，使用其他线程相关的，也一定会阻塞，如使用redis的操作
# 		"""
# 		# self.kill(block=False)  # block设置为False, 避免再自己的回调函数中kill,导致阻塞
# 		self.kill()
#
# 	def _run(self):
# 		"""通过sleep进行延迟调用注册的函数,这里的sleep与线程的sleep不同，他是基于微线程的\n
# 		"""
# 		gevent.sleep(self.seconds)
# 		return self.delay_call.call()


def callLater(seconds, f, *args, **kw):
    """添加一个定时器\n
    @param seconds: float 定时器设定的时间\n
    @param f: func 定时器执行的方法\n
    @param args: 魔法参数，定时器调用方法所需的参数\n
    @param kw: 魔法默认参数，定时器调用方法所需的默认参数\n
    """
    assert callable(f), "%s is not callable" % f
    assert seconds >= 0, "%s is not greater than or equal to 0 seconds" % (seconds,)
    t = Timer(seconds, f, *args, **kw)
    t.start()
    return t
