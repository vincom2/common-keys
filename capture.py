# the imports are a mess because tbh I haven't read the Xlib docs (well, not much) so I have no idea what is where
import Xlib
from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq
import sys

local_dpy = display.Display()
record_dpy = display.Display()

SHIFT_KEYCODE = 50 #wow such portable
is_shifted = False

def set_shift(oo):
    global is_shifted
    if is_shifted == oo:
        print("wow shift state is so wrong", file=sys.stderr)
        sys.exit(1)

    is_shifted = not is_shifted

# only detects shift so far. also
def interpret_keypress(keypress, type):
    k = XK.keysym_to_string(local_dpy.keycode_to_keysym(keypress, 0))
    if k == None and keypress == 50:
        if type == X.KeyPress:
            set_shift(True)
        else:
            set_shift(False)
        k = SHIFT_KEYCODE
    return k

def shift_input(c):
    if is_shifted:
        return c.upper()
    else:
        return c

# it's not giving names for modifier keys and stuff :o
# it also doesn't detect shifted keys. please fix
def record_callback(reply):
    # omg this is atrocious. the fucking function is called "callback" and you're doing this.
    # can you actually code? kill yourself now.

    try:
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            # heh I still have no idea what this does. such copy from example code.
            print("received swapped protocol data, ignored", file=sys.stderr)
            return
        if not len(reply.data) or reply.data[0] < 2: # not an event
            return

        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None) # wut

            if event.type == X.KeyPress:
                # print("press event is", event.detail)
                # keysym = local_dpy.keycode_to_keysym(event.detail, 0)
                # if not keysym: #this doesn't seem to do anything...
                    # print("KeyCode", event.detail)
                # else:
                c = interpret_keypress(event.detail, X.KeyPress)
                if c == SHIFT_KEYCODE:
                    continue
                print("KeyStr", shift_input(c))
            elif event.type == X.KeyRelease:
                # print("release event is", event.detail)
                interpret_keypress(event.detail, X.KeyRelease)

    except KeyboardInterrupt:
        # I have no idea whether this cleanup part actually works lol
        # maybe make it die on esc or some other clever idea like that instead
        print("bye")
        record_dpy.record_disable_context(rec_context)
        record_dpy.flush()
        local_dpy.flush()
        record_dpy.record_free_context(rec_context)
        return



def main():
    """just grabs all keystrokes and logs them before passing them through
       where 'logs' means prints to console >.> find out how logging works plz"""
    if not record_dpy.has_extension('RECORD'):
        print("RECORD extension not found!")
        sys.exit(1)

    # create a recording context
    # we only want keyboard events
    global rec_context
    rec_context = record_dpy.record_create_context(
                   0,
                   [record.AllClients],
                   [{
                        'core_requests': (0, 0),
                        'core_replies': (0, 0),
                        'ext_requests': (0, 0, 0, 0),
                        'ext_replies': (0, 0, 0, 0),
                        'delivered_events': (0, 0),
                        # I believe this specifies a range in [KeyPress, KeyRelease, ButtonPress, ButtonRelease, MotionNotify]
                        # and all we want to grab is KeyPress (or KeyRelease would work too, I guess?)
                        'device_events': (X.KeyPress, X.KeyRelease),
                        'errors': (0, 0),
                        'client_started': False,
                        'client_died': False,
                    }])
    # enable the context
    record_dpy.record_enable_context(rec_context, record_callback)

if __name__ == '__main__':
    main()
