provider "aws" {
  region = "eu-north-1"
}

resource "aws_instance" "coordinator" {
  ami                    = "ami-0705383d0b3ee1b10"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.laba_sg.id]

  tags = {
    Name = "Sharding-Coordinator"
  }
}

resource "aws_instance" "shards" {
  count                  = 2
  ami                    = "ami-0705383d0b3ee1b10"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.laba_sg.id]

  tags = {
    Name = "Shard-Node-${count.index + 1}"
  }
}