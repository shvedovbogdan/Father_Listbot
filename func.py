from random import randint, choice
def make_captcha():
	cchoicce = ["Plus", "Minus"]
	s = choice(cchoicce)
	if s == "Plus":
		a = randint(1,50)
		b = randint(1,50)
		result = a + b
		znak = "+"
		return [a, b, result, znak]
	elif s == "Minus":
		ma = randint(1,50)
		mb = randint(1,50)
		minus = ma - mb
		mznak = "-"
		return [ma, mb, minus, mznak]
		#print(make_captcha())