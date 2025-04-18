# /// script
# dependencies = [
#   "duckdb",
#   "boto3"
# ]
# ///

import os
import zipfile
from pathlib import Path
from typing import Iterable

import boto3
import duckdb


BUCKET = "cmu-95797-23m6"
paths = [
    "data/bike/",
    "data/taxi/"
]
output_dir_name = "sampled-data"
sample_as_int = 10
output_format = "parquet"
zip_filename = f"{output_dir_name}.zip"


def list_files(bucket, path: str) -> Iterable[str]:
    return map(lambda fn: fn.key, bucket.objects.filter(Prefix=path))

def run():
    this_dir = Path(__file__).resolve().parent
    output_dir = this_dir / output_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    con.execute("""
        install httpfs; 
        load httpfs;
        set s3_region='us-east-1';    
        set enable_progress_bar=false;
        set memory_limit='10GB';
    """)
    bucket = boto3.resource('s3').Bucket(BUCKET)

    for path in paths:
        print(f"--- Starting {path}...") 
        for s3_key in list_files(bucket, path):
            if ('csv' not in s3_key and 'parquet' not in s3_key): 
                continue
            base_name = os.path.basename(s3_key).split('.')[0]
            output_file = os.path.join(output_dir, f"{base_name}_sampled.{output_format}")
            file_key = f"https://{BUCKET}.s3.us-east-1.amazonaws.com/{s3_key}"
            
            print(f"Sampling from: {file_key}")
            if file_key.endswith('csv'):
                con.execute(f"""
                    COPY (
                        SELECT *
                        FROM read_csv('{file_key}', all_varchar=1)
                        USING SAMPLE {int(sample_as_int)} PERCENT
                    )
                    TO '{output_file}' (FORMAT {output_format.upper()});
                """)
            else:
                con.execute(f"""
                    COPY (
                        SELECT *
                        FROM read_parquet('{file_key}')
                        USING SAMPLE {int(sample_as_int)} PERCENT
                    )
                    TO '{output_file}' (FORMAT {output_format.upper()});
                """)

        print(f"--- Finished {path}...") 

    # Zip the output directory
    print(f"Zipping {output_dir} to {zip_filename}")
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, output_dir)
                zipf.write(full_path, arcname)


if __name__ == "__main__":
    run()
