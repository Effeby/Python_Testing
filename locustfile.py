from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        self.client.get('/')

    @task
    def show_summary(self):
        self.client.post('/showSummary', data={'email': 'example@example.com'})

    @task
    def book_ticket(self):
        self.client.get('/book/competition_name/club_name')

    @task
    def purchase_places(self):
        data = {
            'competition': 'competition_name',
            'club': 'club_name',
            'places': 2  # Adjust the number of places as needed
        }
        self.client.post('/purchasePlaces', data=data)
