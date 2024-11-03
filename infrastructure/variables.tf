variable "region" {
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  type        = string
  default     = "barkuni-stg-cluster"
}

variable "vpc_id" {
  type        = string
  default     = "vpc-0621d00529c603ade"
}

variable "subnet_ids" {
  type    = list(string)
  default = [
    "subnet-09953b604a2b9e977",
    "subnet-061ae542e3f8fe03f"
  ]
}

variable "desired_capacity" {
  type        = number
  default     = 2
}

variable "instance_type" {
  type        = string
  default     = "t3.medium"
}

variable "key_name" {
  type        = string
  default     = "vica-key-pair-1"
}

variable "tags" {
  type    = map(string)
  default = {
    cluster_name = "barkuni-eks-cluster"
    version      = "1.30"
    environment  = "test"
    owner        = "yativ"
    terraform    = "true"
  }
}