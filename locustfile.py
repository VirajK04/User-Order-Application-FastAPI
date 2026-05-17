import random
import string
from locust import HttpUser, task, between

def random_string(length=10):
    """Generates a random string to ensure unique emails."""
    return ''.join(random.choices(string.ascii_letters, k=length))

class APIUser(HttpUser):
    # Simulate a user pausing for 1 to 2 seconds between clicks
    wait_time = between(1, 2)
    
    def on_start(self):
        """
        Runs once per simulated user when they spawn.
        We create a base user here so we have a valid user_id for order tasks.
        """
        self.user_id = None
        email = f"{random_string()}@loadtest.com"
        
        with self.client.post("/api/users/", json={"name": "Locust User", "email": email}, catch_response=True) as response:
            if response.status_code == 200:
                self.user_id = response.json().get("id")
            else:
                response.failure(f"Failed to create setup user: {response.text}")

    @task(3)
    def create_order(self):
        """Simulates placing an order (Weighted heavier, runs 3x more often)"""
        if self.user_id:
            self.client.post("/api/orders/", json={
                "user_id": self.user_id,
                "product_name": f"Product-{random.randint(1, 100)}",
                "quantity": random.randint(1, 5)
            })

    @task(4)
    def fetch_user_dashboard(self):
        """
        Simulates a user loading their profile to see all their orders.
        THIS IS THE CRITICAL TEST for your `selectinload` N+1 optimization!
        """
        if self.user_id:
            # We group the URL under a generic name so the Locust dashboard doesn't 
            # create thousands of separate rows for every unique ID.
            self.client.get(f"/api/users/{self.user_id}/orders", name="/api/users/[id]/orders")

    @task(1)
    def create_new_user(self):
        """Simulates a brand new user signing up."""
        email = f"{random_string()}@loadtest.com"
        self.client.post("/api/users/", json={
            "name": "New Signup",
            "email": email
        })