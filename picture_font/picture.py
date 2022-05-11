from PIL import Image, ImageDraw


def create(users, type):
    im = Image.open(f'../photo/{type}.png')
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        (100, 100),
        'Test Text',
        fill=('#FFFFFF')
    )
    im.show()


create('ew', 'start')