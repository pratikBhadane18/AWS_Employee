import boto3
import json
import os

bucket = os.environ["S3_BUCKET"]
image = "employee.jpg"

s3 = boto3.client("s3")

rekognition = boto3.client(
    "rekognition",
    region_name=os.environ["AWS_REGION"]
)

# Upload image
s3.upload_file(image, bucket, image)

print("Image uploaded successfully")

# Detect faces
response = rekognition.detect_faces(
    Image={
        "S3Object": {
            "Bucket": bucket,
            "Name": image
        }
    },
    Attributes=["ALL"]
)

faces = response["FaceDetails"]

print(f"Number of faces: {len(faces)}")

result = {
    "number_of_faces": len(faces),
    "faces": []
}

for i, face in enumerate(faces, start=1):
    confidence = face["Confidence"]

    print(f"Face {i} Confidence: {confidence:.2f}")

    result["faces"].append({
        "face": i,
        "confidence": confidence
    })

with open("result.json", "w") as f:
    json.dump(result, f, indent=4)

print("result.json created")