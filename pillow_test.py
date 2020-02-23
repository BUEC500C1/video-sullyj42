from PIL import Image, ImageDraw, ImageFont
# get an image
filename = './output/2020_02_20/brabbott42_3_iter30/twitter_brabbott42_20180108_20170125.png'
base = Image.open(filename).convert('RGBA')

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255,255,255,0))
print(f'Image size: {base.size}')
# get a font
N = base.size[1]/8
fnt = ImageFont.truetype('fonts/OpenSans-Italic.ttf', round(N))
# get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((base.size[0]/5,base.size[1]/4), "Hello World", font=fnt, fill=(255,255,255,210))
# draw text, full opacity
#d.text((2*N,200), "World", font=fnt, fill=(255,255,255,255))

out = Image.alpha_composite(base, txt)
out.show()
