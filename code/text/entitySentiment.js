async function quickstart() {
// Imports the Google Cloud client library
const language = require('@google-cloud/language');

// Creates a client
const client = new language.LanguageServiceClient();

for (let i = 1; i < 82; i++) {

  console.log(i)

const bucketName = 'sentiment-classification-test/outputSmall';
const fileName = `${i}.txt`;

// Prepares a document, representing a text file in Cloud Storage
const document = {
  gcsContentUri: `gs://${bucketName}/${fileName}`,
  type: 'PLAIN_TEXT',
};

// Detects sentiment of entities in the document
const [result] = await client.analyzeEntitySentiment({document});
const entities = result.entities;

console.log('Entities and sentiments:');
entities.forEach(entity => {
  console.log(`  Name: ${entity.name}`);
  console.log(`  Type: ${entity.type}`);
  console.log(`  Score: ${entity.sentiment.score}`);
  console.log(`  Magnitude: ${entity.sentiment.magnitude}`);
});


}
}

quickstart()