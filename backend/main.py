import sys
import traceback

sys.path.append("./verieql")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from verieql.constants import DIALECT
from verieql.environment import Environment
from verieql.errors import *

import google.generativeai as genai
import psycopg2
import os
import time

my_API = os.environ.get('GOOGLE_API')
genai.configure(api_key=my_API)
model = genai.GenerativeModel("gemini-1.5-flash")


app = FastAPI()

origins = [
    'http://localhost:3000',
    'http://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Benchmark(BaseModel):
    query1: str
    query2: str
    bound: int
    table_schema: dict = Field(default=None, alias='schema')
    constraints: list
    dialect: str
    
class sampleQuery(BaseModel):
    query1: str


@app.post("/verify")
async def verify(benchmark: Benchmark):
    if benchmark.dialect == 'MySQL':
        dialect = DIALECT.MYSQL
    elif benchmark.dialect == 'MariaDB':
        dialect = DIALECT.MARIADB
    elif benchmark.dialect == 'PostgreSQL':
        dialect = DIALECT.POSTGRESQL
    elif benchmark.dialect == 'Oracle':
        dialect = DIALECT.ORACLE
    else:
        dialect = DIALECT.ALL

    ret = {}
    try:
        with Environment(generate_code=True, timer=False, show_counterexample=True, dialect=dialect) as env:
            for k, v in benchmark.table_schema.items():
                env.create_database(attributes=v, bound_size=benchmark.bound, name=k)
            env.add_constraints(benchmark.constraints)
            env.save_checkpoints()
            if env._script_writer is not None:
                env._script_writer.save_checkpoints()

            try:
                result = env.analyze(benchmark.query1, benchmark.query2, out_file='tmp/smt.py')

                if not result:
                    ret['decision'] = 'NEQ'
                    if env.counterexample:
                        ret['counterexample'] = dict(env.counterexample_dict)
                        ret['counterexample_sql'] = env.sql_code.replace('`', '')
                    else:
                        ret['counterexample'] = {}
                        ret['counterexample_sql'] = ''
                elif result == -1:
                    raise NotEquivalenceError
                else:
                    ret['decision'] = 'EQU'

                with open('tmp/smt.py', 'r') as smt_file:
                    ret['pysmt_formula'] = smt_file.read().replace('`', '')
            except NotEquivalenceError:
                ret['decision'] = 'NEQ'
                ret['counterexample'] = {}
                ret['counterexample_sql'] = ''
                ret['pysmt_formula'] = ''

                # with open('tmp/smt.py', 'r') as smt_file:
                #     ret['pysmt_formula'] = smt_file.read().replace('`', '')
            except TimeoutError:
                ret['decision'] = 'TMO'
    except Exception as e:
        print(''.join(traceback.format_tb(e.__traceback__)) + str(e))
        ret['decision'] = 'ERR'

    return ret

def extract_string(text, start_char, end_char):
    start_index = text.find(start_char) +len(start_char)
    end_index = text.find(end_char, start_index)
    return text[start_index:end_index]


@app.post("/askai")
async def askai(query: sampleQuery):
    gptprompt=f'''Optimize the following SQL query for performance. Prioritize reducing the number of rows scanned by the database engine, using efficient join strategies, and minimizing subquery complexity. Focus on leveraging indexing, partitioning, and appropriate filtering to reduce execution time. Ensure that the query remains semantically identical to the original and adheres to best practices for SQL performance optimization. Specify the optimized query beginning with && and ending with &&.

    Here is the query to optimize:
    {query.query1}

    Ensure the optimized query:
    0. Do not alter coloumn names.
    1. Utilizes window functions like `ROW_NUMBER()` or `RANK()` or `NTILE()`for efficient subquery replacements.
    2. Minimizes redundant table joins and reduces the number of nested subqueries.
    3. Makes use of joins instead of correlated subqueries where appropriate.
    4. Reduces data scanned by applying filters earlier in the query execution.
    5. Orders the results by the relevant fields efficiently without introducing extra computation costs.
    '''
    response = model.generate_content(gptprompt)
    result = extract_string(str(response.text), "&&", "&&")
    return result

@app.post("/excquery")
async def askai(query: sampleQuery):
    connection = psycopg2.connect(database="tpch", user="postgres", password="test123", host="localhost", port=5432)
    cursor = connection.cursor()
    ret_data = {}
    # with cProfile.Profile() as pr:
    start = time.time()
    cursor.execute(query.query1)
    end = time.time()
    record = cursor.fetchall()
    print("Data from Database:- ", len(record))
    ret_data['record'] = record
        # query_res_list.append(record)
    ret_data['time'] = end - start
    return ret_data