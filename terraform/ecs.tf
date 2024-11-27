resource "aws_ecr_repository" "mlflow_repo" {
  name = "ecs-repo"
}

resource "aws_ecs_cluster" "mlflow_cluster" {
  name = "mlflow-cluster"
}

resource "aws_ecs_task_definition" "mlflow_task" {
  family                   = "mlflow-task"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([{
    name      = "mlflow"
    image     = "${aws_ecr_repository.mlflow_repo.repository_url}:latest"
    essential = true
    portMappings = [
      {
        containerPort = 5000  # Default MLflow port
        hostPort      = 5000
        protocol      = "tcp"
      }
    ]
  }])
}

resource "aws_ecs_service" "mlflow_service" {
  name            = "mlflow-service"
  cluster         = aws_ecs_cluster.mlflow_cluster.id
  task_definition = aws_ecs_task_definition.mlflow_task.arn
  desired_count   = 1

  network_configuration {
    subnets          = [aws_subnet.subnet_id]  # Replace with your subnet
    assign_public_ip = true
    security_groups = [aws_security_group.mlflow_sg.id]
  }
}


resource "aws_lb" "mlflow_lb" {
  name               = "mlflow-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.mlflow_sg.id]
  subnets            = [aws_subnet.subnet_id]  # Replace with your subnet
}

resource "aws_lb_target_group" "mlflow_target_group" {
  name     = "mlflow-target-group"
  port     = 5000
  protocol = "HTTP"
  vpc_id   = aws_vpc.vpc_id  # Replace with your VPC ID
}

resource "aws_lb_listener" "mlflow_listener" {
  load_balancer_arn = aws_lb.mlflow_lb.arn
  port              = "80"
  default_action {
    type             = "fixed-response"
    fixed_response {
      status_code = 200
      content_type = "text/plain"
      message_body = "MLflow is up and running!"
    }
  }
}

output "mlflow_url" {
  value = aws_lb.mlflow_lb.dns_name
}
