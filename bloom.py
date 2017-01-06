import hashlib
import string
import random
import math
from bitstring import BitArray


class Bloom():

	def __init__(self, size):
		self.size = size
		self.bits = BitArray(self.size)

	def _generate_hashes(self, item):
		for algorithm in hashlib.algorithms:
			alg = getattr(hashlib, algorithm)()
			alg.update(item)
			yield int(alg.hexdigest(), 16) % self.size

	def add(self, item):
		for h in self._generate_hashes(item):
			self.bits[h] = True

	def check(self, item):
		return all([self.bits[h] for h in self._generate_hashes(item)])

	def write_filter(self, outfile):
		with file(outfile, 'w') as f:
			f.write(self.bits.bin)

if __name__ == '__main__':
	b = Bloom(600000000)
	for i in range(100):
		s = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
		b.add(s)
		print b.check(s)

	for i in range(100):
		s = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
		print b.check(s)

	b.write_filter('out.txt')