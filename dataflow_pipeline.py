import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

class ParseEventFn(beam.DoFn):
    def process(self, element):
        import json
        data = json.loads(element.decode('utf-8'))
        yield {
            'user_id': data['user_id'],
            'event_type': data['event_type'],
            'timestamp': data['timestamp']
        }

def run():
    options = PipelineOptions(
        streaming=True,
        project='airy-actor-457907-a8',
        region='us-central1',
        job_name='user-activity-streairy-actor-457907-a8am',
        temp_location='gs://sample-data-storage-1/temp',
        runner='DataflowRunner'
    )

    with beam.Pipeline(options=options) as p:
        (p
         | 'Read from PubSub' >> beam.io.ReadFromPubSub(topic='projects/airy-actor-457907-a8/topics/user-events')
         | 'Parse JSON' >> beam.ParDo(ParseEventFn())
         | 'Write to BQ' >> beam.io.WriteToBigQuery(
                            table='airy-actor-457907-a8.sample_dataset.user_events',  # Use your actual dataset name
                            schema='user_id:STRING, event_type:STRING, timestamp:TIMESTAMP',
                            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
                        )
        )

if __name__ == '__main__':
    run()