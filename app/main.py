from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers.cars_router import router as cars_router

app = FastAPI(
    title="Oficial Car Dealership API",
    version="1.0.0",
)

app.include_router(cars_router)


@app.get("/scalar", include_in_schema=False)
def scalar_docs():
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Oficial Car Dealership API - Scalar</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
        </head>
        <body>
            <script id="api-reference" data-url="/openapi.json"></script>
            <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
        </body>
        </html>
        """
    )
