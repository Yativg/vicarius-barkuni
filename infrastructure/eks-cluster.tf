provider "aws" {
  region  = var.region
  profile = "barkuni-profile"
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = "1.30"
  subnet_ids      = var.subnet_ids

  enable_irsa = true

  tags = var.tags

  vpc_id = var.vpc_id

  eks_managed_node_group_defaults = {
    ami_type               = "AL2_x86_64"
    instance_types         = ["t3.medium"]
    vpc_security_group_ids = ["sg-00f92ba6cbd006d63"]
  }

  eks_managed_node_groups = {

    node_group = {
      min_size     = 2
      max_size     = 6
      desired_size = 2
    }
  }
}
