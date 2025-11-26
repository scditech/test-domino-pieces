from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import pandas as pd
from pathlib import Path
from docx import Document


class FetchSolargisDataPiece(BasePiece):
    
    def piece_function(self, input_data: InputModel):

        print(f"[INFO] Fetching data from {input_data.input_path} → {input_data.output_path}")

        csv_data = []
        csv_started = False

        # Read the Word document
        input_data_file = Path(input_data.input_path)
        doc = Document(input_data_file)
        csv_data = []
        csv_started = False
    
        # Process each paragraph in the document
        for paragraph in doc.paragraphs:
            line = paragraph.text.strip()
            # Check if we've reached the CSV data section
            if "#Data:" in line:
                csv_started = True
                continue

            # If we're in the CSV section, store the line
            if csv_started and line:
                csv_data.append(line)

        # Convert to DataFrame and write to CSV
        if csv_data:
            df = pd.DataFrame(csv_data)
            message = f"Doc with data readed successfully, {len(df)} rows found."
            print(f"[SUCCESS] {message}")
            output_data_file = Path(input_data.output_path) 
            df.to_csv(output_data_file, index=False, header=False)
            
        # Set display result
        self.display_result = {
            "file_type": "csv",
            "file_path": str(output_data_file)
            
        }

        # Return output
        return OutputModel(
            message=message,
            file_path=str(output_data_file)
        )

# import boto3
# import os
# from urllib.parse import urlparse
# from models import InputModel, OutputModel

# def main(input_model: InputModel) -> OutputModel:
#     print(f"[INFO] Fetching data from {input_model.s3_path} → {input_model.output_path}")
    
#     # Parse S3 path
#     parsed = urlparse(input_model.s3_path, allow_fragments=False)
#     if parsed.scheme == "s3":
#         bucket = parsed.netloc
#         key = parsed.path.lstrip('/')
        
#         # Initialize S3 client
#         s3 = boto3.client('s3')
        
#         # Create output directory if not exists
#         os.makedirs(os.path.dirname(input_model.output_path), exist_ok=True)
        
#         # Download file
#         s3.download_file(bucket, key, input_model.output_path)
#         print(f"[SUCCESS] Downloaded {input_model.s3_path}")
        
#         return OutputModel(
#             message=f"Successfully downloaded {input_model.s3_path}",
#             downloaded_file=input_model.output_path
#         )
#     else:
#         raise ValueError("Only S3 paths are supported")

# if __name__ == "__main__":
#     # For testing purposes
#     input_data = InputModel(
#         s3_path="s3://bucket/data.csv",
#         output_path="/mnt/artifacts/data.csv"
#     )
#     result = main(input_data)
#     print(result)