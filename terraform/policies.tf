data "aws_iam_policy_document" "pink_twins_admin_policy" {
  statement {
    effect    = "Allow"
    actions   = ["s3:*"]
    resources = [
			  format("arn:aws:s3:::%s", aws_s3_bucket.pink_twins_bucket.id),
        format("arn:aws:s3:::%s/*", aws_s3_bucket.pink_twins_bucket.id)
		]
  }
}

data "aws_iam_policy_document" "pink_twins_push_only_policy" {
  statement {
    effect    = "Allow"
    actions   = ["s3:PutObject"]
    resources = [
      format("arn:aws:s3:::%s/%s", aws_s3_bucket.pink_twins_bucket.id, var.image_folder),
      format("arn:aws:s3:::%s/%s/*", aws_s3_bucket.pink_twins_bucket.id, var.image_folder)
		]
  }
}
