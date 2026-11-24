"""Unit tests for AGYOS FastAPI Backend."""
from __future__ import annotations

import unittest
from fastapi.testclient import TestClient

from app.main import app


class TestAGYOSBackendAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_root_endpoint(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "operational")
        self.assertEqual(data["version"], "3.2.0")

    def test_health_check(self) -> None:
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "agyos-api")
        self.assertIn("uptime_seconds", data)

    def test_list_roles(self) -> None:
        response = self.client.get("/api/v1/roles")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        # Filter by department
        eng_response = self.client.get("/api/v1/roles?department=Engineering")
        self.assertEqual(eng_response.status_code, 200)
        eng_data = eng_response.json()
        for r in eng_data:
            self.assertEqual(r["department"], "Engineering")

    def test_list_skills(self) -> None:
        response = self.client.get("/api/v1/skills?limit=10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_decide_endpoint(self) -> None:
        # Backend task query
        response = self.client.post("/api/v1/decide", json={"task": "Build FastAPI endpoint with Pydantic"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["selected_skill"], "fastapi-pro")

        # Frontend task query
        fe_response = self.client.post("/api/v1/decide", json={"task": "Create Next.js App Router layout"})
        self.assertEqual(fe_response.status_code, 200)
        fe_data = fe_response.json()
        self.assertEqual(fe_data["selected_skill"], "nextjs-best-practices")

    def test_decide_empty_query_fails(self) -> None:
        response = self.client.post("/api/v1/decide", json={"task": "   "})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
