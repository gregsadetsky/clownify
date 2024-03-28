import random
from io import BytesIO

from flask import Flask, request, send_file
from PIL import Image

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # if method is get, return index.html
    if request.method == "GET":
        return send_file("index.html")

    # load the image received in the form data
    img = Image.open(request.files["image"])
    # convert img to rgba
    img = img.convert("RGBA")

    clown1 = Image.open("secretclown1.png")
    clown2 = Image.open("secretclown2.png")

    # alphify the clowns
    for clown in [clown1, clown2]:
        # extract alpha channel
        a_channel = clown.getchannel("A")
        # reduce values by half
        a_channel = a_channel.point(lambda x: x * 0.66)
        clown.putalpha(a_channel)

    # paste clown somewhere on the original image
    for _ in range(random.randint(1, 500)):
        for clown in [clown1, clown2]:
            img.paste(
                clown,
                (
                    random.randint(0, int(img.size[0] * 0.9)),
                    random.randint(0, int(img.size[1] * 0.9)),
                ),
                clown,
            )

    # de-rgba'ify
    img = img.convert("RGB")

    # send as jpeg
    img_io = BytesIO()
    img.save(img_io, "JPEG", quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
