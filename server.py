import tornado.ioloop
import tornado.web
import os, uuid

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")
define("dir", default="/tmp/", help="Video content directory")

class FileHandler(tornado.web.RequestHandler):

    def post(self):
        movie_info = self.request.files['movie'][0]

        name = movie_info['filename']

        fh = open(options.dir+name, "w")
        fh.write(movie_info['body'])
        self.set_status(201)
        self.finish({
            'url': 'rtmp://10.0.3.227:1935/vod2/'+name
        })

    def delete(self, *args, **kwargs):
        movie_name = self.get_argument('movie_name')
        os.remove(options.dir+movie_name)
        self.set_status(204)
        self.finish({
            'message': 'movie file has been removed'
        })

def main():
    parse_command_line()
    application = tornado.web.Application(
        [
            (r"/movie", FileHandler)
        ],
        debug=options.debug
    )
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()