from fastapi import FastAPI

from api.views import products

app = FastAPI(title='Учебный проект Магазин на MongoDB', docs_url='/')
app.include_router(products.router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
