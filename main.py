import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import users


class Greeting(db.Model):
    """Models a Guestbook entry with an author, content, avatar, and date."""
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    avatar = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True)


def guestbook_key(guestbook_name=None):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        self.response.out.write("""
              <form action="/resize" enctype="multipart/form-data" method="post">
                <div><label>Upload your image:</label></div>
                <div><input type="file" name="img"/></div>
                <div>Height : <input type="text" name="height"/></div>
                <div>Width : <input type="text" name="width"/></div>
                <div>
                <select name="image_type">
                    <option value="PNG">PNG</option>
                    <option value="JPEG">JPG/JPEG</option>
                </select>
                </div>
                <div><input type="checkbox" name="enhance_color" value="true">Enhance Color/brightness??</div>

                <div><input type="submit" value="Upload"></div>
              </form>
             <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
             <form action="/crop" enctype="multipart/form-data" method="post">
                <div><label>Crop your image:</label></div>
                <div><input type="file" name="img"/></div>
                <div>Left X cordinate : <input type="text" name="left_x"/></div>
                <div>Top Y cordinate : <input type="text" name="top_y"/></div>
                <div>Right X cordinate : <input type="text" name="right_x"/></div>
                <div>Bottom Y cordinate : <input type="text" name="bottom_y"/></div>
                <div>
                <select name="image_type">
                    <option value="PNG">PNG</option>
                    <option value="JPEG">JPG/JPEG</option>
                </select>
                </div>
                <div><input type="checkbox" name="enhance_color" value="true">Enhance Color/brightness??</div>
                <div><input type="submit" value="Upload"></div>
             </form>
            </body>
          </html>""")


class Image(webapp2.RequestHandler):
    def get(self):
        greeting = db.get(self.request.get('img_id'))
        if greeting.avatar:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(greeting.avatar)
        else:
            self.response.out.write('No image')


class ResizeImage(webapp2.RequestHandler):
    def post(self):
        photo = self.request.get('img')
        image_type = self.request.get('image_type')
        print(image_type)
        request_width = self.request.get('width')
        request_hieght = self.request.get('height')
        encoding_type = images.JPEG
        if image_type == "PNG":
            encoding_type = images.PNG
        print(str(encoding_type))
        photo = images.resize(photo,width=int(request_width),height=int(request_hieght),quality=100,output_encoding=encoding_type)
        if self.request.get('enhance_color') == "true":
            photo = images.im_feeling_lucky(photo,output_encoding=encoding_type,quality=100)
            print("Yes enhancing")

        #photo = images.execute_transforms(photo,output_encoding=images.JPEG,quality=100)
        self.response.headers['Content-Type'] = 'image/'+str(image_type).lower()
        self.response.out.write(photo)


class CropImage(webapp2.RequestHandler):
    def post(self):
        photo = self.request.get('img')
        image_type = self.request.get('image_type')
        print(image_type)
        request_left_x = self.request.get('left_x')
        request_top_y = self.request.get('top_y')
        request_right_x = self.request.get('right_x')
        request_bottom_y = self.request.get('bottom_y')
        encoding_type = images.JPEG
        if image_type == "PNG":
            encoding_type = images.PNG
        print(str(encoding_type))
        photo = images.crop(photo,left_x=float(request_left_x),top_y=float(request_top_y),right_x=float(request_right_x),bottom_y=float(request_bottom_y),quality=100,output_encoding=encoding_type)
        
        if self.request.get('enhance_color') == "true":
            photo = images.im_feeling_lucky(photo,output_encoding=encoding_type,quality=100)
            print("Yes enhancing")

        #photo = images.execute_transforms(photo,output_encoding=images.JPEG,quality=100)
        self.response.headers['Content-Type'] = 'image/'+str(image_type).lower()
        self.response.out.write(photo)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/img', Image),
                               ('/resize', ResizeImage),
                                ('/crop',CropImage)],
                              debug=True)
