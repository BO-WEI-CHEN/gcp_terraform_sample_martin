provider "google" {
  credentials = file("/Users/chenbowei/Downloads/cloud-sa-sandbox-1-81756389a7fb.json") # 請將路徑替換為您的 GCP 服務帳戶(可以直接使用 GCE 的 SA -> 請妥善保存) JSON 憑證文件的路徑
  project     = "cloud-sa-sandbox-1"                                                    # 將 project 替換為您的 GCP porj ID -> 可以進入 console 首頁查看
  region      = "asia-east1"                                                            # 將 region 替換為您想要使用的 GCP 區域
}

##################################################################################
# RESOURCE
##################################################################################
# 創建 VPC 虛擬私人網路
resource "google_compute_network" "custom_network" {
  name                    = "martin-vpc"
  auto_create_subnetworks = false
}

# 創建子網域
resource "google_compute_subnetwork" "martin_subnet_1" {
  name          = "martin-2024-subnet-1"
  network       = google_compute_network.custom_network.self_link
  ip_cidr_range = "10.0.0.0/20"
  secondary_ip_range {
    range_name    = "martin-pods-range"
    ip_cidr_range = "10.14.0.0/20"
  }
  secondary_ip_range {
    range_name    = "martin-services-range"
    ip_cidr_range = "10.18.0.0/20"
  }
  region = "asia-east1"
}

resource "google_compute_subnetwork" "martin_subnet_2" {
  name          = "martin-2024-subnet-2"
  network       = google_compute_network.custom_network.self_link
  ip_cidr_range = "10.1.0.0/24"
  region        = "asia-east1"
}

# 創建防火牆
resource "google_compute_firewall" "ssh_https_firewall" {
  name    = "martin-ssh-https-firewall"
  network = google_compute_network.custom_network.self_link

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
}
