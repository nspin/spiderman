

if __name__ == '__main__':
    import tornado.ioloop
    app = mk_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
