import fastapi
import uvicorn
import art_data

#from service.models.art_model import SPARQLModel

app = fastapi.FastAPI()


@app.get('/')
def index():
    return {
        "message":"Bonjour!!!!",
        "usage":"Call /api/artwork/{title} to use API"
    }

#@app.get('/api/artwork/{title}', response_model=SPARQLModel)
@app.get('/api/artwork/{title}')
async def artwork_search(title: str):
    artwork = await art_data.get_artwork(title)
    if not artwork:
        raise fastapi.HTTPException(status_code=404)

    return artwork

if __name__ == '__main__':
    uvicorn.run(app)
