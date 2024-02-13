from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Temps d'attente entre les requêtes consécutives

    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def book(self):
        # Remplacez 'CompetitionName' et 'ClubName' par les noms réels de la compétition et du club
        self.client.get("/book/Spring%20Festival/Simply%20Lift")

    @task
    def purchase_places(self):
        # Remplacez 'CompetitionName' et 'ClubName' par les noms réels de la compétition et du club
        response = self.client.post("/purchasePlaces", data={"competition": "Spring Festival", "club": "Simply Lift", "places": "2"}, allow_redirects=False)
        if response.status_code == 302:  # Si la redirection est détectée
            # Extraire l'URL de redirection depuis l'en-tête 'Location'
            redirect_url = response.headers.get("Location")
            if redirect_url:
                # Effectuer une nouvelle requête GET pour suivre la redirection
                self.client.get(redirect_url)
