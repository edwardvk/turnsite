import gtk
import webkit
import gobject
import time
import os
import sys
import datetime
import ctypes
import onlyoneprocess
import settings
onlyoneprocess.onlyoneprocess("news24")
gobject.threads_init()


try: 
	libgobject = ctypes.CDLL('/usr/lib/i386-linux-gnu/libgobject-2.0.so.0')
	libsoup = ctypes.CDLL('/usr/lib/i386-linux-gnu/libsoup-2.4.so.1')
except: 
	libgobject = ctypes.CDLL('/usr/lib/x86_64-linux-gnu/libgobject-2.0.so.0')
	libsoup = ctypes.CDLL('/usr/lib/x86_64-linux-gnu/libsoup-2.4.so.1')

libwebkit = ctypes.CDLL('/usr/lib/libwebkitgtk-1.0.so.0')
session = libwebkit.webkit_get_default_session()

generic_cookiejar_type = libgobject.g_type_from_name('SoupCookieJar')
libsoup.soup_session_remove_feature_by_type(session, generic_cookiejar_type)

#add a new persistent cookie jar
cookiejar = libsoup.soup_cookie_jar_text_new('/tmp/cookies.txt',False)
libsoup.soup_session_add_feature(session, cookiejar)

websites = settings.websites




#proxy_uri = libsoup.soup_uri_new('http://www.in24.co.za:8888') # set your proxy url
#libgobject.g_object_set(session, "proxy-uri", proxy_uri, None)


win = list()
window = list()
lastreload = list()
starthtml = os.path.join(os.path.dirname(os.path.abspath( __file__ )),"start.html")



def check_reload(windowid):
	ago = 300 #seconds
	if lastreload[windowid] < time.time()-ago:
		print 'Opening '+websites[windowid]
		window[windowid].open(websites[windowid])
		lastreload[windowid] = time.time() #set to new time
	print "No need to reload"

for website in websites:
	win.append(gtk.Window(type=gtk.WINDOW_TOPLEVEL))
	window.append(webkit.WebView())
	window[-1].open(starthtml)

	win[-1].add(window[-1])
	win[-1].fullscreen()
	win[-1].set_decorated(gtk.FALSE) 
	win[-1].show_all()
	lastreload.append(0)
	
for x in range(len(websites)):
	check_reload(x)

activewindow = [0]


def toggle():
	print "Toggle: "+datetime.datetime.today().isoformat();
	windowid = activewindow[0]
	nextwindow = windowid
	
	while True:
		nextwindow += 1
		if nextwindow >= len(websites):
			nextwindow = 0
		
		try:
			if "error" not in str(window[nextwindow].get_property("title")).lower():
				print "Presenting page %s" % (nextwindow,)
				try:	
					print "URI", window[nextwindow].get_property("uri"), " ", window[nextwindow].get_property("title")
				except Exception, e:
					print repr(e)
				win[nextwindow].unfullscreen()

				win[nextwindow].present()
				time.sleep(1) 
				win[nextwindow].fullscreen()
				activewindow[0] = nextwindow
				check_reload(windowid) # Reload old window.
				


				return True
				
			else:
				print "Page %s not ready: %s" % (nextwindow, websites[nextwindow]), str(window[nextwindow].get_load_status()), str(window[nextwindow].get_property("title")).lower()
				sys.stdout.flush()
				time.sleep(1)
		except Exception, e:
			print "Problem", repr(e)
				

gobject.timeout_add(5*1000, toggle) 
#check_reload(0)
#toggle()

gtk.main()

