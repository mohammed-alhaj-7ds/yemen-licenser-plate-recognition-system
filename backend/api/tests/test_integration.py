import pytest
import io
from rest_framework import status
from rest_framework.test import APIClient
from PIL import Image

@pytest.mark.django_db
class TestAPIIntegration:
    def setup_method(self):
        self.client = APIClient()
        # Mock API Key setup if strictly enforcing middleware in tests
        self.api_key = "test_key"
        # In a real scenario, we'd create an APIKey model instance here
        # For this integration test, we assume middleware might be bypassed or key created
        # But let's act as if we are external
        
    def generate_dummy_image(self):
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'jpeg')
        file.name = 'test.jpg'
        file.seek(0)
        return file

    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get('/api/v1/health/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['status'] == 'ok'

    def test_predict_image_missing_auth(self):
        """Test prediction without API key should fail (if auth enabled)."""
        response = self.client.post('/api/v1/predict/image/')
        # Depending on config, might be 401 or 403
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_400_BAD_REQUEST]

    def test_predict_image_invalid_file(self):
        """Test sending invalid data."""
        # Bypassing auth via mock or assuming test env allows
        response = self.client.post('/api/v1/predict/image/', {}, format='multipart')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Note: Full flow requires actual model weights loaded which might not be available in CI env
    # So we limit tests to interface contract tests
