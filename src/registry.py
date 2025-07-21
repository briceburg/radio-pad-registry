import connexion
from api import create_app
from connexion.resolver import RestyResolver
from connexion.options import SwaggerUIOptions
from api.players import set_app_instance

app = create_app()

# Set the app instance for the players module to access
set_app_instance(app)

# Add RestyResolver to automatically map endpoints to functions
options = SwaggerUIOptions(swagger_ui_path="/api-docs")
app.add_api("openapi.yaml", resolver=RestyResolver("api"), swagger_ui_options=options)

if __name__ == "__main__":
    from pathlib import Path

    app.run(f"{Path(__file__).stem}:app", port=8080)
