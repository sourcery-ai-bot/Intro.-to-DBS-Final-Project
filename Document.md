# 分工
- 爬蟲 : 俞柏帆
- APP 主體 : 翁宇弘
- SQL + AWS : 陳奎元
- chart : 賴柏允
- video : 周子揚

# Request
### Must
- DBMS on AWS
- App on local environment
### Optional
- App on AWS
- price prediction
- GUI
- indicators of chart

# Report

### Motivations - 周子揚
1. Why we need a DB for this App ?

### Application Description - 翁宇弘

### Data Collection - 俞柏帆 & 陳奎元
1. source : investing.com
2. how we collect the data
    - strategy
    - code
3. how we import the data
    - strategy
    - code
4. how we update the data
    - strategy
    - code

### Database Schema - 陳奎元
1. schema (visualization tool in DBMS) + constaints
2. NF
4. index
5. NF v. performance trade-off

### Function Description & SQL - 翁宇弘 & 陳奎元
#### print records (with constraints)
- coin type ( default : all types )
- date interval ( default : within 1 month )
- sorted by any selected attributes ( default : 'date' )
#### make chart