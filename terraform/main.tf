resource "aws_s3_bucket" "pink_twins_bucket" {
   bucket = format("%s-bucket", var.project_name)
}

resource "aws_s3_bucket_ownership_controls" "pink_twins_bucket_ownership_controls" {
  bucket = aws_s3_bucket.pink_twins_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "image_bucket" {
  depends_on = [aws_s3_bucket_ownership_controls.pink_twins_bucket_ownership_controls]

  bucket = aws_s3_bucket.pink_twins_bucket.id
  acl    = "private"
}

resource "aws_s3_object" "image_folder" {
    bucket = "${aws_s3_bucket.pink_twins_bucket.id}"
    key    = format("%s/", var.image_folder)
}
