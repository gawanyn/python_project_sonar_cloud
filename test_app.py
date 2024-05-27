import unittest
from unittest.mock import patch
from app import app, create_product, get_product_by_id, update_product, delete_product
from db import ProductModel

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        ProductModel.delete().execute()

    def test_create_product(self):
        product = create_product("Test Product", 50)
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 50)

    def test_get_product_by_id(self):
        create_product("Test Product", 50)
        product = get_product_by_id(1)
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 50)

    def test_update_product(self):
        create_product("Test Product", 50)
        updated_product = update_product(1, name="Updated Product", price=100)
        self.assertIsNotNone(updated_product)
        self.assertEqual(updated_product.name, "Updated Product")
        self.assertEqual(updated_product.price, 100)

    def test_delete_product(self):
        create_product("Test Product", 50)
        success = delete_product(1)
        self.assertTrue(success)
        product = get_product_by_id(1)
        self.assertIsNone(product)

    @patch('app.get_product_by_id')
    def test_product_not_found(self, mock_get_product_by_id):
        mock_get_product_by_id.return_value = None
        response = self.app.get('/api/products/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Product not found."})

if __name__ == '__main__':
    unittest.main()
