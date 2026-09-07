"""Locust load-test scenario for the DevHub API.

Run with:  docker compose -f docker-compose.stress.yml up --build
Then open http://localhost:8089  (or `make stress-headless` for a CLI run).

The scenario authenticates as the seeded demo user and exercises a
read-heavy mix of the public + authenticated endpoints, plus a couple of
writes (job application, payment transaction) to stress the DB layer too.
"""

import random

from locust import HttpUser, between, task

API = "/api/v1"
DEMO_EMAIL = "demo@devhub.app"
DEMO_PASSWORD = "demo12345"


class DevHubUser(HttpUser):
    wait_time = between(0.3, 1.5)

    def on_start(self):
        self.token = None
        resp = self.client.post(
            f"{API}/auth/login",
            json={"email": DEMO_EMAIL, "password": DEMO_PASSWORD},
            name="login",
        )
        if resp.status_code == 200:
            self.token = resp.json().get("access_token")
        self.headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(6)
    def list_jobs(self):
        self.client.get(f"{API}/jobs", headers=self.headers, name="GET /jobs")

    @task(6)
    def list_products(self):
        self.client.get(f"{API}/market/products", headers=self.headers, name="GET /market/products")

    @task(4)
    def list_roadmaps(self):
        self.client.get(f"{API}/roadmaps", headers=self.headers, name="GET /roadmaps")

    @task(4)
    def list_courses(self):
        self.client.get(f"{API}/learning/courses", headers=self.headers, name="GET /learning/courses")

    @task(3)
    def search_jobs(self):
        self.client.get(
            f"{API}/jobs?search=Engineer&type=full_time",
            headers=self.headers,
            name="GET /jobs?search",
        )

    @task(3)
    def my_profile(self):
        self.client.get(f"{API}/users/me", headers=self.headers, name="GET /users/me")

    @task(2)
    def apply_to_job(self):
        resp = self.client.get(f"{API}/jobs", headers=self.headers, name="GET /jobs")
        if resp.status_code != 200:
            return
        jobs = resp.json()
        if jobs:
            job_id = random.choice(jobs)["id"]
            self.client.post(
                f"{API}/jobs/{job_id}/apply",
                json={"cover_letter": "Load test application"},
                headers=self.headers,
                name="POST /jobs/{id}/apply",
            )

    @task(1)
    def create_transaction(self):
        self.client.post(
            f"{API}/payments/transactions",
            json={"amount": 9.99, "description": "load test"},
            headers=self.headers,
            name="POST /payments/transactions",
        )
