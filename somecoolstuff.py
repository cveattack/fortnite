from PIL import Image, ImageDraw, ImageFont
import urllib.request


class stuff:
    @staticmethod
    def makeapic(arr: list[str], nametosave: str) -> None:
        background_color = (0, 0, 0)
        image_width = 1000  # adjust as needed
        image_height = (150*((len(arr)//8)+1))+100  # adjust as needed
        image = Image.new('RGB', (image_width, image_height), background_color)

        # set up constants for image placement
        padding = 30
        thumbnail_width = (image_width - padding * 9) // 8
        thumbnail_height = thumbnail_width + 30  # adjust as needed
        font_size = 14  # adjust as needed
        font = ImageFont.truetype('arial.ttf', font_size)

        # loop through the array of arrays and add each photo and name
        current_row = 0
        current_column = 0

        sortarray = ['mythic', 'legendary', 'dark', 'slurp', 'starwars', 'marvel', 'lava',
                     'frozen', 'gaminglegends', 'shadow', 'icon', 'dc', 'epic', 'rare', 'uncommon', 'common']
        
        arr.sort(key=lambda x: sortarray.index(x[2]))

        for skin in arr:
            # load the image
            urllib.request.urlretrieve(
                skin[1],
                '{}/skintemp.png'.format(nametosave.split('/')[0]))
            photo = Image.open('{}/skintemp.png'.format(nametosave.split('/')[0])).convert('RGBA')
            new_img = Image.open(
                f'rarities/rarity_{skin[2].lower()}.png').convert('RGBA').resize(photo.size)
            new_img.paste(photo, mask=photo)
            photo = new_img
            # resize the image
            photo.thumbnail((thumbnail_width, thumbnail_height))
            # calculate the position of the image and name
            x = padding + (thumbnail_width + padding) * current_column
            y = padding + (thumbnail_height + padding) * current_row
            # add the photo to the image
            image.paste(photo, (x, y))
            # add the name of the skin below the photo
            draw = ImageDraw.Draw(image)
            name = skin[0]
            name_width, name_height = draw.textsize(name, font=font)
            draw.text((x + (thumbnail_width - name_width) // 2, y +
                      thumbnail_height-20), name, font=font, fill=(255, 255, 255))
            # update the current row and column
            current_column += 1
            if current_column >= 8:
                current_row += 1
                current_column = 0
            draw.text((image_width//2, image_height-80), 'Total: {}'.format(len(arr)),
                      font=ImageFont.truetype('arial.ttf', 40), fill=(255, 255, 255))
        image.save(nametosave)
