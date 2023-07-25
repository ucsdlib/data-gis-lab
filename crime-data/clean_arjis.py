import polars as pl

detention_dict = {
    'EMDF': '446 ALTA RD., STE. 5200',
    'GBDF': '446 ALTA RD. STE. 5300',
    'LCDF': '451 RIVERVIEW PARKWAY',
    'RMDF': '446 ALTA ROAD, STE. 5400',
    'SDCJ': '1173 FRONT STREET',
    'SBDF': '500 THIRD AVE.',
    'VDF': '325 S. MELROSE DR., #200',
}

# Read in the downloaded csv here
df = pl.read_csv('data/ARJIS_Public_Crime_Data_w__Day_of_Week_20230720.csv')

df2 = df.with_columns(
    pl.col('Date').str.to_datetime('%m/%d/%Y %I:%M:%S %p'),
    pl.col('Time of Day').str.to_time('%H:%M'),
    pl.when(pl.col('Block Address').str.contains(r'(^\d+)'))
            .then(pl.col('Block Address').str.extract(r'(^\d+)').cast(pl.Int64).add(50).cast(pl.Utf8).alias('number'))
            .otherwise(None),
    pl.when(pl.col('Block Address').str.contains('BLOCK'))
            .then(pl.col('Block Address').str.replace(' BLOCK ', '').str.split(by=' ').list.slice(1, None).alias('street'))
            .otherwise(None)
  ).with_columns(
        pl.when(pl.col('number').is_not_null())
                .then(pl.col('number') + ' ' + pl.col('street').list.join(' '))
                .otherwise(pl.col('Block Address'))
                .alias('new_address'),
  ).with_columns(
        pl.when(pl.col('number').is_null() & pl.col('street').list.lengths() == 1)
                .then(pl.col('street').list.get(0))
                .otherwise(pl.col('new_address'))
                .alias('new_address')
  ).with_columns(
        pl.when(pl.col('Block Address').str.contains('&'))
                .then(pl.col('Block Address'))
                .otherwise(pl.col('new_address'))
                .alias('new_address'),
  ).with_columns(
        pl.when((pl.col('street').list.lengths() == 1) & (pl.col('street').list.first().str.lengths().is_in([3, 4])))
                .then(pl.col('street').list.first().map_dict(detention_dict))
                .otherwise(pl.col('new_address'))
                .alias('remapped')
  ).drop(['number', 'street'])

df2.write_csv('arjis_cleaned_output.csv')

# Can use this to check new addresses and final mapping - leaving here as a tool
# num = 30
# with pl.Config(fmt_str_lengths=100, tbl_rows=num):
#     print(df2.select(pl.col(['Block Address', 'new_address', 'remapped'])).sample(num))