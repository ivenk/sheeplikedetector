from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn

PORT=8080


app = Starlette(debug=True)

@app.route('/')
async def homepage(request):
    return JSONResponse({'hello':'world'})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=PORT)
