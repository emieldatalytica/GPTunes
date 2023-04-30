resource "google_secret_manager_secret" "spotify_client_id" {
  secret_id = "SPOTIFY_CLIENT_ID"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "spotify_client_id_version" {
  secret      = google_secret_manager_secret.spotify_client_id.name
  secret_data = var.spotify_client_id_version
}

resource "google_secret_manager_secret" "spotify_client_secret" {
  secret_id = "SPOTIFY_CLIENT_SECRET"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "spotify_client_secret_version" {
  secret      = google_secret_manager_secret.spotify_client_secret.name
  secret_data = var.spotify_client_secret_version
}

resource "google_secret_manager_secret" "spotify_redirect_uri" {
  secret_id = "SPOTIFY_REDIRECT_URI"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "spotify_redirect_uri_version" {
  secret      = google_secret_manager_secret.spotify_redirect_uri.name
  secret_data = var.spotify_redirect_uri_version
}
