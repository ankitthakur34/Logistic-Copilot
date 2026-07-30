from app.agents.sql_agent.schema.sql_answer_result import (
    SQLAnswerResult,
)
from app.agents.sql_agent.sql_normalizer import SQLNormalizer


class SQLAgent:

    def __init__(

        self,

        schema_builder,

        sql_generator,

        validator,

        executor,

        answer_generator,

    ):

        self.schema_builder = (
            schema_builder
        )

        self.sql_generator = (
            sql_generator
        )

        self.validator = (
            validator
        )

        self.executor = (
            executor
        )

        self.answer_generator = (
            answer_generator
        )

    def run(

        self,

        question: str,

    ):

        #
        # schema
        #

        schema = (

            self.schema_builder.build()

        )

        #
        # sql generation
        #

        generated_sql = (

            self.sql_generator.generate(

                question=question,

                schema=schema,

            )

        )
      
       

        


        #
        # normalize and validate
        #
        normalized_sql = SQLNormalizer.normalize(generated_sql)

        self.validator.validate(
            normalized_sql
        )

        #
        # execute
        #

        rows = (

            self.executor.execute(
                normalized_sql
            )

        )

        #
        # answer
        #

        answer = (

            self.answer_generator.generate(

                question=question,

                sql=normalized_sql,

                rows=rows,

            )

        )

        return SQLAnswerResult(

            question=question,

            sql=generated_sql,
            normalized_sql=normalized_sql,


            answer=answer,

            rows=rows,

        )