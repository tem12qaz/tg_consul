from PIL import Image, ImageDraw, ImageFont


# class E:
#     def __init__(self, name):
#         self.username = name


def create(users, type):
    im = Image.open(f'../photo/{type}_name.png')
    draw_text = ImageDraw.Draw(im)
    font = ImageFont.truetype('../photo/font.ttf', size=17)

    def draw(a, b, text):
        draw_text.text(
            (a, b),
            text,
            fill=('#CCCCCC'),
            font=font
        )

    # users = {
    #     'donors': [
    #         E('tem12qaz'),
    #         E('HBewfwefwefwef'),
    #         E('Alexander2112'),
    #         E('fwewefwefwef'),
    #
    #     ],
    #     'partners': [
    #         E('HBewfwefwefwef'),
    #         E('Alexander2112'),
    #         E('fwewefwefwef'),
    #         E('0000000eee'),
    #     ],
    #     'mentors': [
    #         E('Alexander2112'),
    #         E('0000000eee'),
    #     ],
    #     'master': E('Alexander2112'),
    # }

    if type != 'start':
        donors = [
            (122, 128),
            (122, 305),
            (122, 399),
            (122, 566),
            (1076, 129),
            (1070, 302),
            (1070, 396),
            (1076, 567),
        ]
        partners = [
            (310, 218),
            (310, 484),
            (837, 218),
            (837, 480),
        ]
        mentors = [
            (255, 354),
            (940, 350)
        ]
        master_ = (551, 480)
        for donor in users['donors']:
            if donor:
                if len(donor.username) > 9:
                    name = donor.username[:9] + '...'
                else:
                    name = donor.username
                draw(*donors[users['donors'].index(donor)], name)

        for partner in users['partners']:
            font = ImageFont.truetype('../photo/font.ttf', size=19)
            if len(partner.username) > 11:
                name = partner.username[:11] + '...'
            else:
                name = partner.username
            draw(*partners[users['partners'].index(partner)], name)

        for mentor in users['mentors']:
            font = ImageFont.truetype('../photo/font.ttf', size=18)
            if len(mentor.username) > 8:
                name = mentor.username[:8] + '...'
            else:
                name = mentor.username
            draw(*mentors[users['mentors'].index(mentor)], name)

        master = users['master']
        font = ImageFont.truetype('../photo/font.ttf', size=19)
        if len(master.username) > 15:
            name = master.username[:15] + '...'
        else:
            name = master.username
        draw(*master_, name)

        im.show()
    else:
        donors = [
            (311, 218),
            (311, 485),
            (836, 218),
            (836, 481),
        ]
        mentors = [
            (255, 353),
            (942, 350)
        ]
        master_ = (544, 495)

        for donor in users['donors']:
            if donor:
                if len(donor.username) > 15:
                    name = donor.username[:15] + '...'
                else:
                    name = donor.username
                draw(*donors[users['donors'].index(donor)], name)

        for mentor in users['mentors']:
            font = ImageFont.truetype('../photo/font.ttf', size=18)
            if len(mentor.username) > 8:
                name = mentor.username[:8] + '...'
            else:
                name = mentor.username
            draw(*mentors[users['mentors'].index(mentor)], name)

        master = users['master']
        font = ImageFont.truetype('../photo/font.ttf', size=19)
        if len(master.username) > 15:
            name = master.username[:15] + '...'
        else:
            name = master.username
        draw(*master_, name)

    return im.tobytes()


