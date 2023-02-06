import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

SCHEMA = ",".join(
    [
        "message:STRING",
        "age:INTEGER",
        "salary:FLOAT",
        "timestamp:TIMESTAMP",
    ]
)

ERROR_SCHEMA = ",".join(
    [
        "message:STRING",
        "timestamp:TIMESTAMP",
    ]
)


class Parser(beam.DoFn):
    ERROR_TAG = 'error'

    def process(self, subs_message_data):
        try:
            row = json.loads(subs_message_data.decode("utf-8"))

            yield {
                "message": row["message"],
                "age": int(row["age"]),
                "salary": float(row["salary"]),
                "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            }
        except Exception as error:
            error_row = {
                "message": str(error),
                "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            }
            yield beam.pvalue.TaggedOutput(self.ERROR_TAG, error_row)


def run(options, input_subscription, output_table, output_error_table):

    with beam.Pipeline(options=options) as pipeline:
        rows, error_rows = \
            (pipeline | 'Read from PubSub' >> beam.io.ReadFromPubSub(subscription=input_subscription)
             | 'Parse JSON messages' >> beam.ParDo(Parser()).with_outputs(Parser.ERROR_TAG,
                                                                                main='rows')
             )

        _ = (rows | 'Write data to BigQuery'
             >> beam.io.WriteToBigQuery(output_table,
                                        create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                                        schema=SCHEMA
                                        )
             )

        _ = (error_rows | 'Write errors to BigQuery'
             >> beam.io.WriteToBigQuery(output_error_table,
                                        create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                                        schema=ERROR_SCHEMA
                                        )
             )


# if __name__ == '__main__':
parser = argparse.ArgumentParser()
parser.add_argument(
    '--input_subscription',
    default="/subscriptions/cf-task/cf_pubsub_subs1",
    required=True,
    help='Input PubSub subscription of the form "/subscriptions/<PROJECT>/<SUBSCRIPTION>".'
)
parser.add_argument(
    '--output_table_success_messages',
    default="cf-task:task_df_dataset.output_table_success_messages",
    required=True,
    help='Output BigQuery table for normal data'
)
parser.add_argument(
    '--output_table_error_messages',
    default="cf-task:task_df_dataset.output_table_error_messages",
    required=True,
    help='Output BigQuery table for errors'
)
known_args, pipeline_args = parser.parse_known_args()
pipeline_options = PipelineOptions(pipeline_args)
pipeline_options.view_as(SetupOptions).save_main_session = True
run(
    pipeline_options,
    known_args.input_subscription,
    known_args.output_table_success_messages,
    known_args.output_table_error_messages
)
