from drf_yasg import openapi

schema_view = openapi.Info(
    title="My API",
    default_version='v1',
    description="API for managing books",
    contact=openapi.Contact(email="contact@myapi.local"),
    license=openapi.License(name="MIT License"),
)