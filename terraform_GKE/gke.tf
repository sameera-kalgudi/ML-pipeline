
# loading the gcp variables from the google cloud SDK 
variable "project_id" {
  description = "project id"
}

variable "region" {
  description = "region"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "gke_username" {
  default     = ""
  description = "gke username"
}

variable "gke_password" {
  default     = ""
  description = "gke password"
}

variable "gke_num_nodes" {
  default     = 1
  description = "number of gke nodes"
}

# GKE cluster
resource "google_container_cluster" "primary" {
  name     = "test-cluster"
  location = var.region

  remove_default_node_pool = false
  initial_node_count       = 1

  # network    = google_compute_network.vpc.name
  # subnetwork = google_compute_subnetwork.subnet.name

  master_auth {
    username = var.gke_username
    password = var.gke_password

    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

# # Separately Managed Node Pool
# resource "google_container_node_pool" "primary_nodes" {
#   name       = "test-cluster"
#   location   = var.region
#   cluster    = google_container_cluster.primary.name
#   node_count = var.gke_num_nodes

#   node_config {
#     oauth_scopes = [
#       "https://www.googleapis.com/auth/logging.write",
#       "https://www.googleapis.com/auth/monitoring",
#     ]

#     labels = {
#       env = var.project_id
#     }

#     # preemptible  = true
#     machine_type = "n1-standard-1"
#     tags         = ["gke-node", "test-cluster"]
#     metadata = {
#       disable-legacy-endpoints = "true"
#     }
#   }
# }