
"""Utilities, misc methods, etc."""

def create_file(path, f=None, createpath=True):
    "Utility that creates files and path's.  Files are timestamp internally."
    import os, os.path, time

    if createpath:
        if not os.path.exists(path):
            os.makedirs(path)

    if f and path:
        fp = "/".join([path, f])
        if not os.path.isfile(fp):
            f = open(fp, 'w')
            f.write("# Created " + time.strftime("%Y%m%d-%H:%M") + "\n")
            f.close()
    else:
        return 'You must specify both path and filename.'

    if not f and not createpath:
        raise AttributeError

def md5sum(f):
    """Create a hash of given file."""
    try:
        from hashlib import md5
    except ImportError:
        from md5 import new as md5

    def _sumfile(fobj):
        """Return an md5 hash for an object"""
        m = md5()
        while True:
            d = fobj.read(8096)
            if not d:
                break
            m.update(d)
        return m.hexdigest()

    try:
        fo = file(f, 'rb')
    except:
        return 'Failed to open file'
    ret = _sumfile(fo)
    fo.close()
    return ret

def sendmail(server, to_address, from_address, subject, message):
    """A method to send mail with."""
    import smtplib

    smtpserver = smtplib.SMTP(server)
    headers = {
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain',
        'From': from_address,
        'To': ", ".join(to_address),
        'Subject': subject
    }
    message = ('\n'.join(['%s: %s' % x for x in headers.iteritems()]) + "\n\n" + message)
    smtpserver.sendmail(from_address, to_address, message)
    smtpserver.quit()


# subnetmask from CIDR
from socket import inet_ntoa
from struct import pack
def calc_netmask(mask):
	"""Example:
	>>> calc_netmask(24)
	'255.255.255.0'
	"""
    bits = 0xffffffff ^ (1 << 32 - mask) - 1
    return inet_ntoa(pack('>I', bits))

# Another version:
from socket import inet_ntoa
from struct import pack
def calc_netmask(mask):
	"""Convert CIDR to netmask

	>>> calc_netmask(24)
	'255.255.255.0'
	"""

	bits = 0
	for i in xrange(32-mask, 32):
		bits |= (1 << i)
	return inet_ntoa(pack('>I', bits))
