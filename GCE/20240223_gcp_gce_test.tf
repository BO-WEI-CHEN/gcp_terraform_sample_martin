# 定義 GCP 提供者
provider "google" {
  credentials = file("/Users/chenbowei/Downloads/cloud-sa-sandbox-1-81756389a7fb.json") # 請將路徑替換為您的 GCP 服務帳戶(可以直接使用 GCE 的 SA -> 請妥善保存) JSON 憑證文件的路徑
  project     = "cloud-sa-sandbox-1"                                                    # 將 project 替換為您的 GCP porj ID -> 可以進入 console 首頁查看
  region      = "asia-east1"                                                            # 將 region 替換為您想要使用的 GCP 區域
}

# 定義一個 GCE unmanaged instance -> 一般的 VM
resource "google_compute_instance" "example_instance" {
  name         = "martin-2024-gce-iac-test" # GCE 的名稱
  machine_type = "n1-standard-1"            # GCE 的機器類型
  zone         = "asia-east1-a"             # GCE 的區域和區域中的區域
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10" # GCE 的啟動磁盤映像
    }
  }
  network_interface {
    network    = "martin-vpc" # GCE 的網路 config -> GEC 會在哪一個 VPC 中
    subnetwork = "martin-2024-subnet-2"
    access_config {} # GCE 的 access IP config -> Ephemeral public IP
  }
}

output "ip" {
  value = google_compute_instance.example_instance.network_interface[0].access_config[0].nat_ip
}
