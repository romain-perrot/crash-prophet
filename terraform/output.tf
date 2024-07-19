output "pink_twins_bucket_name" {
	value = aws_s3_bucket.pink_twins_bucket.id
}

output "pink_twins_admin_access_key_id" {
  value = aws_iam_access_key.pink_twins_admin_access_key.id
	sensitive = true
}

output "pink_twins_admin_access_key_secret" {
  value = aws_iam_access_key.pink_twins_admin_access_key.secret
	sensitive = true
}

output "pink_twins_provider_access_key_id" {
  value = aws_iam_access_key.pink_twins_provider_access_key.id
	sensitive = true
}

output "pink_twins_provider_access_key_secret" {
  value = aws_iam_access_key.pink_twins_provider_access_key.secret
	sensitive = true
}
