from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from fastai.vision import *

import uvicorn
import aiohttp

PORT=5080

app = Starlette(debug=True)

learner = load_learner(Path('./'))

async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


@app.route("/classify-url", methods=["GET"])
async def classify_page(request):
    bytes = await get_bytes(request.query_params["url"])
    img = open_image(BytesIO(bytes))
    res, _, losses = learner.predict(img)
    return HTMLResponse('<html>' +
                            '<body>' +
                                '<h3>Prediction:</h3>' +
                                '<p>'+ str(res) +'</p>' +
                                '<b>Details:</b>' +
                                '<p>' +  str(sorted(
                                            zip(learner.data.classes, map(float, losses)),
                                            key=lambda p: p[1],
                                            reverse=True)) +
                                '</p>' +
                            '</body>' +
                        '</html>'
                        )

@app.route('/')
async def homepage(request):
    return JSONResponse({'go to classify-url and give the url of the':'image'})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=PORT)
