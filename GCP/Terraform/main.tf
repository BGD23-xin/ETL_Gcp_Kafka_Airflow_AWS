##configure the provider of bigquery, the percision of provider 
##(https://registry.terraform.io/providers/hashicorp/google/latest/docs)


terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.23.0"
    }
  }
}

##connect to the google cloud provider
provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}




##create a vm instance

resource "google_compute_instance" "default" {
  machine_type = var.instance_type
  name         = var.instance_name
  zone         = var.instance_zone


  boot_disk {
    auto_delete = true

    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20250213"
      size  = 30
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false


  labels = {
    goog-ec-src = "vm_add-tf"
  }

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    queue_count = 1
    stack_type  = "IPV4_ONLY"
    subnetwork  = var.subnetwork
  }
  service_account {
    email  = "230078498060-compute@developer.gserviceaccount.com"
    scopes = ["cloud-platform"]
  }


  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }
}