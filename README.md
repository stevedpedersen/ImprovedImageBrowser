# ImprovedImageBrowser

[![N|Solid](https://www.python.org/static/opengraph-icon-200x200.png)](https://www.python.org)[![N|Solid](https://avatars0.githubusercontent.com/u/159455?v=4&s=200)](https://www.riverbankcomputing.com/software/pyqt)

ImageBrowser is a simple GUI that displays images in thumbnail and fullscreen mode. Navigation with keys and mouse. Add tags to images and save them. Search the Flickr database for images to add to the image browser. Safe Mode gives confirmation on exit/delete as well as limits number of search results.. **This is a class project written by Steve Pedersen at San Francisco State University CSc 690: Interactive Multimedia Application Development**

# How to run

Run with default settings:
```sh
$ python3 ImageBrowser.py
```
Run with optional parameters:
```sh
$ python3 ImageBrowser.py <Window Width>
$ python3 ImageBrowser.py 800

$ python3 ImageBrowser.py <Window Width> <Safe Mode>
$ python3 ImageBrowser.py 800 1
```
Window Width defaults to 800 
Safe Mode defaults to 0

---
### Installation / Dependenices

ImprovedImageBrowser requires [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5) and [Requests](https://github.com/requests/requests) to run.

Install the dependencies then run the program

```sh
$ pip3 install PyQt5
$ pip3 install requests
```

### Todos

 - Improve GUI
 - Testing & QA

License
----

MIT


**This is a class project written by Steve Pedersen at San Francisco State University CSc 690: Interactive Multimedia Application Development**
