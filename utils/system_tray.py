import pystray

from PIL import Image, ImageDraw


def creat_image(width, height, color1, color2):
    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)

    dc.rectangle(
        (0, height // 2, width // 2, height),
    fill=color2)

    return image

status = False

from pystray import MenuItem as item, Icon as icon, Menu as menu

def on_clicked():
    global status
    status = not item.checked

icon(
    'test', creat_image(64, 64, 'red', 'white'), menu=menu(
        item(
            'Auto Deletar',
            on_clicked,
            checked=lambda item: status))).run()

if __name__ == "__main__":
    icon.run()