import json
from pathlib import Path

import boto3 # type: ignore
from botocore.exceptions import ClientError # type: ignore
from mypy_boto3_textract.type_defs import DetectDocumentTextResponseTypeDef # type: ignore

def extract_content() -> None:
    # Create a Textract client
    try:
      textract = boto3.client('textract')

      # Read the material list from the image file
      #file_path = str(Path(__file__).parent / "images" / "lista-material-escolar.jpeg")
      file_path = str(Path(__file__).parent / "images" / "cloud-formation.png")
      with open(file_path,"rb") as file:
            response = textract.detect_document_text(
                Document={
                    'Bytes': file.read(),
                }
            )
      with open("content.json", "w") as content_file:
            content_file.write(json.dumps(response))    
    except ClientError as error:
         print(f"Error occurred in processing file: {error}")
         return

def filter_content() -> list[str]:    
    # Parse the detected text and extract the required information
    try:
       with open("content.json", "r") as content_file:
          response: DetectDocumentTextResponseTypeDef = json.loads(content_file.read())
          blocks = response['Blocks']
          return [block["Text"] for block in blocks if block["BlockType"] == "LINE"]

    except IOError:
         extract_content()
    return []     
def get_content() -> None:
    for line in filter_content():
        print(line)       

if __name__ == "__main__":
   get_content() # print information extracted from file
