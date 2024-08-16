# from celery import shared_task
# import pandas as pd
# from .models import Company

# @shared_task
# def import_csv(file_path):
#     df = pd.read_csv(file_path)
#     for index, row in df.iterrows():
#         Company.objects.create(
#             name=row['name'],
#             domain=row['domain'],
#             year_founded=row['year_founded'],
#             industry=row['industry'],
#             size_range=row['size_range'],
#             locality=row['locality'],
#             country=row['country'],
#             linkedin_url=row['linkedin_url'],
#             current_employee_estimate=row['current_employee_estimate'],
#             total_employee_estimate=row['total_employee_estimate']
#         )



import pandas as pd
from celery import shared_task
from django.conf import settings
from sqlalchemy import create_engine
import os

@shared_task
def import_csv(file_path):
    # Database connection details from Django settings
    DATABASE = settings.DATABASES['default']
    engine = create_engine(
        f"postgresql://{DATABASE['USER']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['NAME']}"
    )
    
    # Chunk size for large files
    chunk_size = 100000

    # Read and insert data in chunks
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunk.to_sql(
            name='catalyst_count_db',  # Replace with your table name
            con=engine,
            if_exists='append',       # Append to the existing table
            index=False               # Don't write DataFrame index as a column
        )

    # Remove the file after processing
    os.remove(file_path)

    return 'Data import complete.'
