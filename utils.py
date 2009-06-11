
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


"""
The following prime generators were taken from this thread:
	http://groups.google.com/group/comp.lang.python/browse_thread/thread/77cc9764f9d5a072#
"""
def prime_gen():
	"""Generate a list of primes.
	Faster version would be to move prime_list outside of the function.
	"""
    prime_list = [2]
    for p in prime_list: yield p
    for n in itertools.count(prime_list[-1] + 1):
        for p in prime_list:
            if p * p > n:
                prime_list.append(n)
                yield n
                break
            elif n % p == 0:
                break
        else:
            raise Exception("Shouldn't have run out of primes!") 

def prime_gen2():
	"Faster version."
    yield 2
    n = 3
    yield n
    prime_list = [(2, 4), (3, 9)]
    it = itertools.count(4)
    for n in it:
        n = it.next()
        for p,p2 in prime_list:
            if n % p == 0:
                break
            elif p2 > n:
                prime_list.append((n, n*n))
                yield n
                break
        else:
            raise RuntimeError("Shouldn't have run out of primes!") 

"""
Another poc for generating primes, thought it looked pretty.
"""
from itertools import count
from math import sqrt

g = (lambda primes = []:
        (n for n in count(2) if
            (lambda x, primes:
                (primes.append(x) or True
                     if all(x % p for p in primes if p <= sqrt(x))
                     else False)
            )(n, primes)
        )
    )()

for i in range(500):
    print g.next()


"""
Here is another speedup (from my prime pair hunt days):
Check only 2 of every 6 integers.
[6N + 0, 6N + 2, 6N + 4] are divisible by 2, [6N + 0, 6N + 3] by 3.
	- Scott David Daniels
"""

 def prime_gen3():
	 check_list = [(5, 25)]
	 yield 2
	 yield 3
	 yield 5
	 n = 5
	 for incr in itertools.cycle((2, 4)):
	     n += incr
	     for p, p_squared in check_list:
	         if p_squared > n:
	             check_list.append((n, n * n))
	             yield n
	             break
	         elif n % p == 0:
	             break
	     else:
	         raise Exception("Shouldn't have run out of primes!") 
	
