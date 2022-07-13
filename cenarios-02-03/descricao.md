# Descrição

## Cenario 02

Cenário de carga de dados em um banco de dados. Este ocorrerá através da leitura de um CSV com escrita no influxdb.

A quantidade de dados é pequena pois é apenas uma demonstração.

    extract_from_csv >> load_into_db

## Cenário 03

Este cenário engloba também um processo de ETL, com coleta/extração de dados de um CSV, transformação e, por fim, carregamento dos dados em um bucket do InfluxDB.
