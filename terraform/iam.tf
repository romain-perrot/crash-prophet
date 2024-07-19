resource "aws_iam_user" "pink_twins_admin" {
	name = format("%s-admin", var.project_name)
}

resource "aws_iam_user" "pink_twins_provider" {
	name = format("%s-provider", var.project_name)
}

resource "aws_iam_user_policy" "pink_twins_admin_policy" {
  name   = "pink_twins_admin_policy"
  user   = aws_iam_user.pink_twins_admin.name
  policy = data.aws_iam_policy_document.pink_twins_admin_policy.json
}

resource "aws_iam_user_policy" "pink_twins_provider_policy" {
  name   = "pink_twins_provider_policy"
  user   = aws_iam_user.pink_twins_provider.name
  policy = data.aws_iam_policy_document.pink_twins_push_only_policy.json
}

resource "aws_iam_access_key" "pink_twins_admin_access_key" {
  user    = aws_iam_user.pink_twins_admin.name
}

resource "aws_iam_access_key" "pink_twins_provider_access_key" {
  user    = aws_iam_user.pink_twins_provider.name
}
