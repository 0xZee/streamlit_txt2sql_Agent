def dataset_to_bq(dataset, project_id, dataset_name, table_name):
  client = bigquery.Client()
  table_id = f"{project_id}.{dataset_name}.{table_name}"
  # upload df to table BigQuery
  dataset.to_gbq(destination_table=table_id, project_id=project_id, if_exists='replace',  credentials=None)
  table = client.get_table(table_id)
  print(f"# Loaded {table.num_rows} rows to Table : {table_id}")
  print(f"# Table Schema : {table.schema}")

# usage example
dataset_to_bq(dataset, GOOGLE_PROJ_ID, "ds_stx", "stocks_202412")
